---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#160
state: closed
updated_at: 2026-07-13T08:23:13+02:00
is_epic: false
labels:
  - "ready"
  - "sub-task"
publication: sanitized
---

# M1: Eddie SQLite-Schema + Job-CRUD

**Parent:** #157
**Repo:** lydia/home-repo
**Milestone:** M1: Foundation

SQLite-Persistenzschicht:
- Tabellen: jobs, events, audit_log, executors, schedules
- CRUD-Operationen: create, read, list, update, delete
- Migration/Initialisierung beim ersten Start
- Tests: Job wird persistiert, nach Neustart gelesen, CRUD vollständig
