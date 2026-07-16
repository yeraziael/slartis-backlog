---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#166
state: closed
updated_at: 2026-07-13T18:29:00+02:00
is_epic: false
labels:
  - "ready"
  - "sub-task"
publication: sanitized
---

# M4: Eddie Lydia-Messenger-Anbindung

**Parent:** #157, #158
**Repo:** lydia/home-repo
**Milestone:** M4: Integration

Lydia-Prozessor ruft Eddie-API für async-Kommandos auf:
- Processor erkennt async-Command (/prompt, /generate)
- Sendet `POST /api/v1/jobs` an Eddie
- Ergebnis-Rückweg: Polling oder Callback (muss vorher festgelegt werden)
- /status integriert Eddie-Health
- Fallback bei Eddie-Ausfall
- Tests: Async-Command erzeugt Eddie-Job, Ergebnis kommt zurück, Status zeigt Eddie
