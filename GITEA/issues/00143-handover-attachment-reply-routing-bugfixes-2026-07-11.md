---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#143
state: closed
updated_at: 2026-07-14T00:32:26+02:00
is_epic: false
labels:
  []
publication: sanitized
---

# Handover: Attachment/Reply/@-Routing Bugfixes (2026-07-11)

## Session 2026-07-11: Attachment/Reply/@-Routing Bugfixes

### Erledigt

1. **SSH Fallback für Gitea Content-API** (`runtime/processor/handlers/attachments.sh`)
   - Bei "branch does not exist"-Fehler der Content-API → git clone/commit/push per SSH
   - Workaround für Gitea Branch-Cache-Bug

2. **@-Routing verschiebt gesamtes Issue** (`runtime/processor/processor.sh:174-224`)
   - Reply mit @-directive zu anderem Repo → Original-Issue (Titel+Body+Attachments) wird ins Ziel-Repo kopiert
   - Original wird geschlossen, Reply als Kommentar
   - `attach_copy_from_body()` extrahiert Attachment-URLs aus Body, lädt Dateien via raw-Endpoint, lädt ins Ziel hoch

3. **Signal Picture Attachment Null-Byte-Bug** (`runtime/messenger/container_entrypoint.sh:94-111`)
   - `$()` stripped null bytes → JPEG/Binary kam nie durch
   - Fix: nc-Output in tempfile, JSON-Erkennung via `jq -e`, base64 via `< "$tmpfile"`
   - Tests CE12-CE14 (10 asserts) hinzugefügt

### Tests
- `test_processor_handlers.sh`: 179 passed
- `test_container_entrypoint.sh`: 27 passed (CE12: $() korrumpiert 300B→99B ✅)
- **Gesamt: 206 Tests, 0 failed**

### Offen / Nächste Session

1. **Gitea Branch-Cache-Bug** (cati/notizen, repo_id:70): Content-API rejected main branch obwohl ref existiert. Docker-Restart + SSH-Push half nicht. Eventuell Gitea-Datenbank-Reparatur nötig.
2. **CI/CD Pipeline** (Issue #142): ShellCheck, shfmt, bats, Deployment-Pipeline

### Deployment-Status (Pi5)
- Container `lydia-messenger`: restarted ✅
- Processor `lydia-messenger-processor.service`: active ✅
- home-repo: main auf 640f572
