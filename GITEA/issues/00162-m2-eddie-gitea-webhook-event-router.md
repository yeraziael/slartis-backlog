---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#162
state: closed
updated_at: 2026-07-13T09:43:21+02:00
is_epic: false
labels:
  - "ready"
  - "sub-task"
publication: sanitized
---

# M2: Eddie Gitea-Webhook + Event-Router

**Parent:** #157
**Repo:** lydia/home-repo
**Milestone:** M2: Scheduler & Events

Gitea-Event-Verarbeitung:
- Webhook-Endpoint `POST /api/v1/events` für Gitea
- Event-Typ erkennen (issue.opened, push, etc.)
- Event → Job-Mapping (z.B. issue mit label lydia-task → Job vom Typ gitea-task)
- Validierung, Duplikatserkennung
- Tests: Gitea-Webhook erzeugt korrekten Job, unbekannte Events werden ignoriert
