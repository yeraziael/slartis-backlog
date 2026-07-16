---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#159
state: closed
updated_at: 2026-07-13T08:23:13+02:00
is_epic: false
labels:
  - "ready"
  - "sub-task"
publication: sanitized
---

# M1: Eddie Docker-Container + HTTP-Server + Health

**Parent:** #157
**Repo:** lydia/home-repo
**Milestone:** M1: Foundation

Eddie als Docker-Container auf Pi5:
- Dockerfile (aarch64, slim), docker-compose.yml in deploy/docker/
- HTTP-Server auf Port 8080
- `GET /health`, `GET /api/v1/status` Endpoints
- Logging, Graceful Shutdown
- Tests: Container startet, Health antwortet 200
