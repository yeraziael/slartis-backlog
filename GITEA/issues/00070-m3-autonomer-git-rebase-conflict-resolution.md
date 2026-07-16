---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#70
state: closed
updated_at: 2026-07-01T00:29:17+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# M3: Autonomer Git-Rebase + Conflict-Resolution

## Goal
Autonomes Git-Rebase + Conflict-Resolution System für die Homelab-Agenten.

## Architektur-Plan

### Phase 1: Git-Operations-Plugin (🚧 aktuell)
Ein neues Plugin `runtime/plugins/gitops/` mit sicheren Git-Operationen:

| Handler | Funktion | Beschreibung |
|---------|----------|--------------|
| `git_clone` | Repo klonen | `git clone ssh://git@<internal-ip>:2222/{owner}/{repo}` |
| `git_rebase` | Rebase auf Target | `git rebase origin/main` mit Konflikterkennung |
| `git_commit_push` | Commit + Push | Nur in Feature-Branches, nie auf main |
| `git_status` | Status prüfen | `git status --porcelain`, Branch-Info |
| `git_diff` | Diff anzeigen | `git diff target...HEAD` für PR-Context |

**Sicherheit:**
- `git push` nur in Feature-Branches (Block auf main/develop)
- Kein `--force` ohne explizite Bestätigung
- `--dry-run` vor jeder destruktiven Operation
- Alle Operationen loggen

### Phase 2: LLM Conflict-Resolution
Ein Worker-Contract-Typ für Merge-Conflict-Auflösung:

```
contract {
  "task": "resolve merge conflict",
  "conflict_file": "/path/to/file.py",
  "context": {
    "ours": "...current branch version...",
    "theirs": "...incoming version...",
    "ancestor": "...common ancestor..."
  },
  "acceptance": ["python3 -m py_compile /path/to/file.py"]
}
```

**Ablauf:**
1. `git rebase` schlägt fehl → Konflikt-Dateien identifizieren
2. Konflikt-Marker parsen (> ours, ===, < theirs, || ancestor)
3. LLM bekommt: Kontext + beide Versionen + ancestor (optional)
4. LLM generiert aufgelöste Version
5. Acceptance-Tests bestätigen Korrektheit (Syntax, Tests)
6. `git add` + `git rebase --continue`

### Phase 3: PR-Integration
Mit Gitea API:
- PR-Status prüfen (mergeable? conflicts?)
- Automatischer Rebase bei Merge-Conflict
- PR-Merge mit Strategie (rebase-merge, squash-merge)

## Constraints
- Läuft im Homelab (LAN) — SSH: `ssh://git@<internal-ip>:2222/`
- Kein force-push ohne Bestätigung
- Dry-Run vor jeder Änderung
- SSH-Key: `lydia-agent-key` (funktioniert)
- Gitea-Token: `<credential-path-redacted>` (funktioniert)

## Referenzen
- Issue #56 (Planung): M3 = Autonomer Git-Rebase + Conflict-Resolution
- Plugin-Architektur: `runtime/plugins/echo/init.sh` als Vorlage
- Worker-Vertrag: `runtime/dispatch/worker_schema.json`
- home-repo Workflow: Branch → PR → Merge
- SSH: `ssh://git@<internal-ip>:2222/lydia/home-repo`

## Status
🚧 **Phase 1: Architektur-Plan erstellt**
⬜ Phase 1: Git-Operations-Plugin
⬜ Phase 2: LLM Conflict-Resolution
⬜ Phase 3: PR-Integration
