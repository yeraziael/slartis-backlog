---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#163
state: closed
updated_at: 2026-07-13T11:43:33+02:00
is_epic: false
labels:
  - "ready"
  - "sub-task"
publication: sanitized
---

# M3: Eddie Priority-Queue + Retry/DLQ

**Parent:** #157
**Repo:** lydia/home-repo
**Milestone:** M3: Queue & Dispatch

Queue-Management:
- Priority-Queue (0-100, Default 50)
- Retry mit exponentiellem Backoff (max 3)
- Dead Letter Queue für endgültig fehlgeschlagene Jobs
- Timeout pro Job (konfigurierbar)
- Abhängigkeiten zwischen Jobs (blocking/waiting)
- Tests: Priority wird eingehalten, Retry zählt korrekt, DLQ nach 3 Fehlern
