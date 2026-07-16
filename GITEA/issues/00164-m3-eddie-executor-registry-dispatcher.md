---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#164
state: closed
updated_at: 2026-07-13T12:03:40+02:00
is_epic: false
labels:
  - "ready"
  - "sub-task"
publication: sanitized
---

# M3: Eddie Executor-Registry + Dispatcher

**Parent:** #157
**Repo:** lydia/home-repo
**Milestone:** M3: Queue & Dispatch

Executor-Verwaltung und Job-Dispatch:
- Executor-Registry: Lydia, Vekling registrieren sich mit Capabilities
- Dispatcher wählt Executor basierend auf Job-Typ + Capabilities
- HTTP-Aufruf an Executor (POST /execute)
- Result-Handling (completed/failed), Timeout-Überwachung
- Tests: Dispatch an Lydia funktioniert, fehlgeschlagener Job geht in Retry
