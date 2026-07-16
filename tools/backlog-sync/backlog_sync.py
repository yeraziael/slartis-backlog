#!/usr/bin/env python3
"""Deterministic bidirectional synchronization for GitHub files and Gitea issues."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

EXIT_NO_CHANGE = 0
EXIT_CHANGED = 10
EXIT_INVALID = 20
EXIT_CONFLICT = 30
EXIT_REMOTE = 40
EXIT_INTERNAL = 50
EXIT_LOCKED = 60

UTC = dt.timezone.utc


class SyncError(RuntimeError):
    exit_code = EXIT_INTERNAL


class ValidationError(SyncError):
    exit_code = EXIT_INVALID


class RemoteError(SyncError):
    exit_code = EXIT_REMOTE


class LockError(SyncError):
    exit_code = EXIT_LOCKED


def now_iso() -> str:
    return dt.datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value: str | None) -> dt.datetime:
    if not value:
        return dt.datetime.min.replace(tzinfo=UTC)
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def atomic_json(path: pathlib.Path, value: Any) -> bool:
    rendered = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == rendered:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(rendered)
        temporary = pathlib.Path(handle.name)
    temporary.replace(path)
    return True


class FileLock:
    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.fd: int | None = None

    def __enter__(self) -> "FileLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise LockError(f"sync already running: {self.path}") from exc
        os.write(self.fd, f"{os.getpid()}\n".encode())
        return self

    def __exit__(self, *_: Any) -> None:
        if self.fd is not None:
            os.close(self.fd)
        self.path.unlink(missing_ok=True)


@dataclass(frozen=True)
class Epic:
    epic_id: str
    path: pathlib.Path
    title: str
    body: str
    source_hash: str
    control: dict[str, Any]


@dataclass
class Config:
    repo_root: pathlib.Path
    epics_dir: pathlib.Path
    state_file: pathlib.Path
    lock_file: pathlib.Path
    commit_message: str
    gitea_url: str
    owner: str
    repository: str
    token: str
    labels: dict[str, str]
    timeout: int
    marker_start: str
    marker_end: str


def load_config(path: pathlib.Path) -> Config:
    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    gh = raw["github"]
    gt = raw["gitea"]
    sync = raw.get("sync", {})
    root = pathlib.Path(gh.get("repo_root", ".")).expanduser().resolve()
    token_env = gt.get("token_env", "GITEA_TOKEN")
    token = os.environ.get(token_env, "")
    if not token:
        raise ValidationError(f"required environment variable is missing: {token_env}")
    return Config(
        repo_root=root,
        epics_dir=root / gh.get("epics_dir", "EPICS"),
        state_file=root / gh.get("state_file", ".sync/backlog-sync-state.json"),
        lock_file=root / gh.get("lock_file", ".sync/backlog-sync.lock"),
        commit_message=gh.get("commit_message", "status: synchronize Gitea backlog"),
        gitea_url=gt["base_url"].rstrip("/"),
        owner=gt["owner"],
        repository=gt["repository"],
        token=token,
        labels={
            "epic": gt.get("epic_label", "type/epic"),
            "managed": gt.get("managed_label", "sync/managed"),
            "blocked": gt.get("blocked_label", "status/blocked"),
        },
        timeout=int(sync.get("request_timeout_seconds", 20)),
        marker_start=sync.get("managed_marker_start", "<!-- backlog-sync:managed:start -->"),
        marker_end=sync.get("managed_marker_end", "<!-- backlog-sync:managed:end -->"),
    )


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def load_control(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": "1.0", "state": "planned", "blocked_reason": None, "updated_at": None}
    control = json.loads(path.read_text(encoding="utf-8"))
    state = control.get("state", "planned")
    if state not in {"planned", "active", "blocked"}:
        raise ValidationError(f"unsupported state in {path}: {state}")
    control.setdefault("schema_version", "1.0")
    control.setdefault("blocked_reason", None)
    control.setdefault("updated_at", None)
    return control


def scan_epics(epics_dir: pathlib.Path) -> dict[str, Epic]:
    if not epics_dir.is_dir():
        raise ValidationError(f"Epic directory does not exist: {epics_dir}")
    epics: dict[str, Epic] = {}
    for directory in sorted(p for p in epics_dir.iterdir() if p.is_dir() and not p.name.startswith(".")):
        markdown = sorted(p for p in directory.glob("*.md") if p.name.lower() not in {"status.md"})
        if not markdown:
            raise ValidationError(f"Epic has no top-level Markdown files: {directory}")
        sections: list[str] = []
        for item in markdown:
            text = item.read_text(encoding="utf-8").strip()
            sections.append(f"<!-- source:{item.name} -->\n{text}")
        body = "\n\n".join(sections).strip() + "\n"
        title = first_heading(body, directory.name)
        control = load_control(directory / "control.json")
        source = stable_json({"id": directory.name, "title": title, "body": body, "control": control})
        epics[directory.name] = Epic(directory.name, directory, title, body, digest(source), control)
    return epics


class GiteaClient:
    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg

    def request(self, method: str, path: str, payload: Any | None = None) -> Any:
        url = self.cfg.gitea_url + "/api/v1" + path
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, data=data, method=method)
        request.add_header("Authorization", f"token {self.cfg.token}")
        request.add_header("Accept", "application/json")
        if data is not None:
            request.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(request, timeout=self.cfg.timeout) as response:
                content = response.read()
                return json.loads(content) if content else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RemoteError(f"Gitea {method} {path} failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RemoteError(f"Gitea {method} {path} failed: {exc}") from exc

    @property
    def repo_path(self) -> str:
        return f"/repos/{urllib.parse.quote(self.cfg.owner)}/{urllib.parse.quote(self.cfg.repository)}"

    def list_issues(self) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        page = 1
        while True:
            batch = self.request("GET", f"{self.repo_path}/issues?state=all&type=issues&limit=50&page={page}")
            if not batch:
                return issues
            issues.extend(batch)
            if len(batch) < 50:
                return issues
            page += 1

    def list_labels(self) -> dict[str, int]:
        result: dict[str, int] = {}
        page = 1
        while True:
            batch = self.request("GET", f"{self.repo_path}/labels?limit=50&page={page}")
            if not batch:
                return result
            result.update({label["name"]: int(label["id"]) for label in batch})
            if len(batch) < 50:
                return result
            page += 1

    def ensure_labels(self) -> dict[str, int]:
        labels = self.list_labels()
        colors = {"epic": "5319e7", "managed": "1d76db", "blocked": "b60205"}
        for key, name in self.cfg.labels.items():
            if name not in labels:
                created = self.request("POST", f"{self.repo_path}/labels", {"name": name, "color": colors[key]})
                labels[name] = int(created["id"])
        return labels

    def create_issue(self, title: str, body: str, label_ids: list[int]) -> dict[str, Any]:
        return self.request("POST", f"{self.repo_path}/issues", {"title": title, "body": body, "labels": label_ids})

    def update_issue(self, number: int, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("PATCH", f"{self.repo_path}/issues/{number}", payload)

    def comment(self, number: int, body: str) -> None:
        self.request("POST", f"{self.repo_path}/issues/{number}/comments", {"body": body})


def managed_body(cfg: Config, epic: Epic) -> str:
    metadata = {
        "source_repository": "yeraziael/slartis-backlog",
        "source_path": f"EPICS/{epic.epic_id}",
        "work_item_id": epic.epic_id,
        "source_hash": epic.source_hash,
    }
    return (
        f"{cfg.marker_start}\n"
        f"```json\n{json.dumps(metadata, indent=2, sort_keys=True)}\n```\n\n"
        f"{epic.body.rstrip()}\n"
        f"{cfg.marker_end}"
    )


def replace_managed(existing: str, replacement: str, cfg: Config) -> str:
    start = existing.find(cfg.marker_start)
    end = existing.find(cfg.marker_end)
    if start < 0 or end < 0 or end < start:
        suffix = existing.strip()
        return replacement + ("\n\n" + suffix if suffix else "")
    end += len(cfg.marker_end)
    return existing[:start].rstrip() + ("\n\n" if existing[:start].strip() else "") + replacement + existing[end:]


def label_names(issue: dict[str, Any]) -> set[str]:
    return {str(label.get("name")) for label in issue.get("labels", [])}


def load_state(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": "1.0", "items": {}, "last_run": None}
    state = json.loads(path.read_text(encoding="utf-8"))
    state.setdefault("schema_version", "1.0")
    state.setdefault("items", {})
    return state


def git_command(root: pathlib.Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *arguments], cwd=root, text=True, capture_output=True, check=False)


def commit_and_push(cfg: Config, push: bool) -> str | None:
    status = git_command(cfg.repo_root, "status", "--porcelain", "--", str(cfg.epics_dir.relative_to(cfg.repo_root)))
    if status.returncode != 0:
        raise RemoteError(status.stderr.strip())
    if not status.stdout.strip():
        return None
    add = git_command(cfg.repo_root, "add", str(cfg.epics_dir.relative_to(cfg.repo_root)))
    if add.returncode != 0:
        raise RemoteError(add.stderr.strip())
    commit = git_command(cfg.repo_root, "commit", "-m", cfg.commit_message)
    if commit.returncode != 0:
        raise RemoteError(commit.stderr.strip())
    sha = git_command(cfg.repo_root, "rev-parse", "HEAD")
    if sha.returncode != 0:
        raise RemoteError(sha.stderr.strip())
    if push:
        pushed = git_command(cfg.repo_root, "push")
        if pushed.returncode != 0:
            raise RemoteError(pushed.stderr.strip())
    return sha.stdout.strip()


def synchronize(cfg: Config, dry_run: bool, commit: bool, push: bool) -> tuple[dict[str, Any], int]:
    epics = scan_epics(cfg.epics_dir)
    state = load_state(cfg.state_file)
    client = GiteaClient(cfg)
    labels = client.ensure_labels()
    issues = client.list_issues()
    issues_by_number = {int(issue["number"]): issue for issue in issues}
    result: dict[str, Any] = {
        "schema_version": "1.0",
        "started_at": now_iso(),
        "status": "success",
        "created": 0,
        "updated": 0,
        "closed_from_source_deletion": 0,
        "github_status_updates": 0,
        "unchanged": 0,
        "findings": [],
    }
    changed = False

    for epic_id, epic in epics.items():
        record = state["items"].get(epic_id, {})
        issue = issues_by_number.get(int(record["issue_number"])) if record.get("issue_number") else None
        desired_blocked = epic.control.get("state") == "blocked"
        desired_label_names = {cfg.labels["epic"], cfg.labels["managed"]}
        if desired_blocked:
            desired_label_names.add(cfg.labels["blocked"])

        if issue is None:
            if dry_run:
                issue = {"number": -1, "state": "open", "title": epic.title, "body": managed_body(cfg, epic), "labels": [], "updated_at": now_iso(), "html_url": None}
            else:
                issue = client.create_issue(epic.title, managed_body(cfg, epic), [labels[name] for name in sorted(desired_label_names)])
            record = {"issue_number": int(issue["number"]), "last_source_hash": epic.source_hash, "last_blocked": desired_blocked}
            state["items"][epic_id] = record
            result["created"] += 1
            changed = True
        else:
            existing_labels = label_names(issue)
            source_changed = record.get("last_source_hash") != epic.source_hash
            control_time = parse_time(epic.control.get("updated_at"))
            issue_time = parse_time(issue.get("updated_at"))
            gitea_blocked = cfg.labels["blocked"] in existing_labels

            # Blocked is bidirectional. The newest explicit side wins.
            if gitea_blocked != desired_blocked and issue_time > control_time:
                new_state = "blocked" if gitea_blocked else "active"
                control = dict(epic.control)
                control["state"] = new_state
                control["updated_at"] = issue.get("updated_at") or now_iso()
                if not gitea_blocked:
                    control["blocked_reason"] = None
                if not dry_run and atomic_json(epic.path / "control.json", control):
                    result["github_status_updates"] += 1
                    changed = True
                desired_blocked = gitea_blocked
                epic = Epic(epic.epic_id, epic.path, epic.title, epic.body, epic.source_hash, control)
            elif gitea_blocked != desired_blocked:
                desired_label_names = {cfg.labels["epic"], cfg.labels["managed"]}
                if desired_blocked:
                    desired_label_names.add(cfg.labels["blocked"])

            payload: dict[str, Any] = {}
            if source_changed:
                payload["title"] = epic.title
                payload["body"] = replace_managed(str(issue.get("body") or ""), managed_body(cfg, epic), cfg)
            if existing_labels != desired_label_names:
                payload["labels"] = [labels[name] for name in sorted(desired_label_names)]
            if payload:
                if not dry_run:
                    issue = client.update_issue(int(issue["number"]), payload)
                    if desired_blocked != bool(record.get("last_blocked")):
                        reason = epic.control.get("blocked_reason") or "No reason supplied in GitHub control.json."
                        client.comment(int(issue["number"]), f"Backlog sync changed blocked state to **{desired_blocked}**. Reason: {reason}")
                result["updated"] += 1
                changed = True
            else:
                result["unchanged"] += 1
            record["last_source_hash"] = epic.source_hash
            record["last_blocked"] = desired_blocked
            state["items"][epic_id] = record

        runtime_state = "done" if issue.get("state") == "closed" else ("blocked" if desired_blocked else "active")
        status_doc = {
            "schema_version": "1.0",
            "epic_id": epic_id,
            "state": runtime_state,
            "progress_source": "gitea",
            "gitea": {
                "issue_number": issue.get("number"),
                "issue_url": issue.get("html_url") or issue.get("url"),
                "state": issue.get("state"),
                "updated_at": issue.get("updated_at"),
            },
            "synchronized_at": now_iso(),
        }
        # synchronized_at must not create perpetual commits.
        status_path = epic.path / "status.json"
        comparable = dict(status_doc)
        if status_path.exists():
            previous = json.loads(status_path.read_text(encoding="utf-8"))
            previous.pop("synchronized_at", None)
            check = dict(comparable)
            check.pop("synchronized_at", None)
            if previous == check:
                status_doc["synchronized_at"] = json.loads(status_path.read_text(encoding="utf-8")).get("synchronized_at")
        if not dry_run and atomic_json(status_path, status_doc):
            result["github_status_updates"] += 1
            changed = True

    # A source deletion becomes an annotated Gitea closure, never a deletion.
    for epic_id in sorted(set(state["items"]) - set(epics)):
        record = state["items"][epic_id]
        issue = issues_by_number.get(int(record["issue_number"]))
        if issue and issue.get("state") != "closed":
            if not dry_run:
                client.comment(int(issue["number"]), f"Epic `{epic_id}` was removed from the canonical GitHub backlog. The issue is closed by deterministic synchronization; it was not deleted.")
                client.update_issue(int(issue["number"]), {"state": "closed"})
            record["source_removed_at"] = now_iso()
            result["closed_from_source_deletion"] += 1
            changed = True

    state["last_run"] = now_iso()
    if not dry_run:
        atomic_json(cfg.state_file, state)
    commit_sha = None
    if not dry_run and commit:
        commit_sha = commit_and_push(cfg, push)
    result["commit"] = commit_sha
    result["finished_at"] = now_iso()
    return result, EXIT_CHANGED if changed else EXIT_NO_CHANGE


def validate(repo_root: pathlib.Path, epics_dir: str) -> dict[str, Any]:
    epics = scan_epics(repo_root / epics_dir)
    return {"schema_version": "1.0", "status": "valid", "epics": len(epics), "ids": sorted(epics)}


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    check = commands.add_parser("validate")
    check.add_argument("--repo-root", default=".")
    check.add_argument("--epics-dir", default="EPICS")
    sync = commands.add_parser("sync")
    sync.add_argument("--config", type=pathlib.Path, required=True)
    sync.add_argument("--dry-run", action="store_true")
    sync.add_argument("--commit", action="store_true")
    sync.add_argument("--push", action="store_true")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "validate":
            output = validate(pathlib.Path(args.repo_root).resolve(), args.epics_dir)
            print(json.dumps(output, sort_keys=True))
            return EXIT_NO_CHANGE
        cfg = load_config(args.config)
        with FileLock(cfg.lock_file):
            output, code = synchronize(cfg, args.dry_run, args.commit, args.push)
        print(json.dumps(output, sort_keys=True))
        return code
    except SyncError as exc:
        print(json.dumps({"status": "error", "error": str(exc), "exit_code": exc.exit_code}, sort_keys=True))
        return exc.exit_code
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc), "exit_code": EXIT_INTERNAL}, sort_keys=True))
        return EXIT_INTERNAL


if __name__ == "__main__":
    raise SystemExit(main())
