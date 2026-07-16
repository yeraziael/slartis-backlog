# Bidirectional Backlog Sync

Deterministic, token-free synchronization between the file-based GitHub planning backlog and Slarti's issue-based Gitea backlog.

## Authority model

| Data | Authority |
|---|---|
| Epic title and planning content | GitHub files |
| Epic deletion | GitHub files |
| Runtime progress and completion | Gitea issue |
| Blocked state | Bidirectional, newest explicit change wins |
| Issue comments and implementation discussion | Gitea issue |
| Generated progress snapshot | GitHub `EPICS/<epic-id>/status.json` |

The synchronizer never uses an LLM and never deletes a Gitea issue. If an Epic disappears from GitHub, the mapped Gitea issue is closed with a synchronization comment.

## Repository conventions

An Epic is any direct directory below `EPICS/`. Its stable ID is the directory name. Planning content is assembled deterministically from the Markdown files directly inside that directory, in lexical filename order.

Optional GitHub control file:

```json
{
  "schema_version": "1.0",
  "state": "planned",
  "blocked_reason": null,
  "updated_at": "2026-07-17T00:00:00Z"
}
```

Store it as `EPICS/<epic-id>/control.json`. Supported states are `planned`, `active`, and `blocked`.

Generated runtime state is written to `EPICS/<epic-id>/status.json`. This file must not be edited manually.

## Tool contract

Lydia calls one command; Eddie may schedule or debounce it:

```bash
python3 tools/backlog-sync/backlog_sync.py sync \
  --config tools/backlog-sync/config.toml \
  --commit --push
```

Dry run:

```bash
python3 tools/backlog-sync/backlog_sync.py sync \
  --config tools/backlog-sync/config.toml \
  --dry-run
```

Validation only:

```bash
python3 tools/backlog-sync/backlog_sync.py validate
```

The command prints exactly one JSON result object to stdout. Logs go to stderr.

## Required environment variables

- `GITEA_TOKEN`
- `GITHUB_TOKEN` is not required when the repository is already checked out and authenticated Git push is configured.

## State

The persistent mapping database defaults to `.sync/backlog-sync-state.json` and must be stored outside ephemeral containers or mounted as a persistent volume. It records stable Epic-to-Issue mappings, hashes, and the last observed blocked state.

## Exit codes

- `0`: success, no repository change
- `10`: success, changes applied
- `20`: invalid GitHub backlog
- `30`: synchronization conflict
- `40`: remote API or Git failure
- `50`: unexpected internal error
- `60`: another synchronization run holds the lock

## Safety

- No issue is deleted.
- Planning sections in Gitea are replaced only inside managed markers.
- Manual issue comments are preserved.
- A missing GitHub Epic closes the mapped Gitea issue with a reason.
- A Gitea issue closed by Slarti updates GitHub `status.json` to `done`.
- Unchanged runs create no commit.
- No force push is used.
