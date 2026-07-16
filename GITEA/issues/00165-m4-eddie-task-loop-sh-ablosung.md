---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#165
state: closed
updated_at: 2026-07-13T18:36:00+02:00
is_epic: false
labels:
  - "ready"
  - "sub-task"
publication: sanitized
---

# M4: Eddie task_loop.sh-Ablösung

**Parent:** #157
**Repo:** lydia/home-repo
**Milestone:** M4: Integration

Letzter Schritt vor Produktivnahme:
- Eddie übernimmt Gitea-Polling (bisher task_loop.sh)
- Vekling-Dispatch läuft via Eddie statt direkt
- worker_queue.sh wird deaktiviert
- task_loop.sh wird gestoppt, Eddie übernimmt
- Dual-Run-Phase: beide Systeme parallel, Vergleich der Ergebnisse
- Tests: Gitea-Task wird via Eddie korrekt dispatched, task_loop.sh-freier Betrieb stabil
