---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#161
state: closed
updated_at: 2026-07-13T08:23:13+02:00
is_epic: false
labels:
  - "ready"
  - "sub-task"
publication: sanitized
---

# M2: Eddie Cron-Engine + One-Shot-Jobs

**Parent:** #157
**Repo:** lydia/home-repo
**Milestone:** M2: Scheduler & Events

Scheduler-Kern:
- Cron-Ausdrücke parsen (Standard-5-Felder)
- Fällige Jobs erkennen und auslösen
- One-Shot-Jobs (absolute Zeit + delayed)
- Nächste Ausführung persistieren und bei Neustart neu berechnen
- Tests: Cron feuert zur richtigen Zeit, One-Shot läuft genau einmal
