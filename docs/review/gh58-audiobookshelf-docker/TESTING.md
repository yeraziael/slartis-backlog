# TESTING.md — GH-58 Evidence and Verification

## 1. CI Pipeline

Architecture Gitea CI — Run ID: 603 — **Status: success**

CI manifest registers `audiobookshelf-proxy` test stage:
```yaml
- id: audiobookshelf-proxy
  tool: bash
  target: pi/tests/test_audiobookshelf_proxy.sh
  quality_gate: exit_zero
  timeout: 30s
  tags: [audiobookshelf, compose, proxy, tls]
```

All source PRs (#63, #65, #66, #69, #70, #72) passed CI before merge.

## 2. Compose Validation

**Command:** `docker compose -f audiobookshelf.yml config`
**Exit code:** 0
**Result:** PASS — Valid YAML, correct structure, no warnings.

## 3. Contract Tests

**Test:** `pi/tests/test_audiobookshelf_proxy.sh`
**Result:** PASS — All 15 assertions green:
- Image pinned by immutable digest
- ARM64 platform selected
- Restart policy set
- No host ports published
- Expose port 80 only
- Proxy environment vars correct (VIRTUAL_HOST, VIRTUAL_PORT: 80, LETSENCRYPT)
- frontproxy_default network joined
- audiobookshelf_internal network declared internal
- no-new-privileges enabled
- CPU + memory limits set
- Logging size/rotation bounded
- Healthcheck configured
- No secrets or configs declared
- vhost.d contains client_max_body_size and WebSocket headers
- Architecture docs mention required terms

## 4. Runtime Evidence

### Container Status (redacted)
```
NAMES            IMAGE                                          STATUS              PORTS
audiobookshelf   ghcr.io/advplyr/audiobookshelf@sha256:1eef...   Up (healthy)        80/tcp
```

**No host ports bound.** Only `80/tcp` on internal bridge network.

### Healthcheck Status
```
Timestamp: 2026-07-20T15:09:13.648246887+02:00
Status: healthy
FailingStreak: 0
ExitCode: 0
Endpoint: http://localhost:80/ -> HTTP 200
Interval: 15s, Timeout: 10s, Retries: 5, Start Period: 60s
```

**First start:** healthy after 8 seconds
**After restart:** healthy after 8 seconds

### Restart Test
```
Action: docker restart audiobookshelf
Result: PASS
Time to healthy: 8s
Database: /config/absdatabase.sqlite (364KB) — preserved
```

### Data Persistence

| Mount | Host Path | Container Path | Content |
|-------|-----------|----------------|---------|
| audiobookshelf_config | /mnt/hardDrive/docker/audiobookshelf/config | /config | absdatabase.sqlite, migrations/ |
| audiobookshelf_metadata | /mnt/hardDrive/docker/audiobookshelf/metadata | /metadata | backups/, cache/, logs/, streams/ |
| cache (bind) | /mnt/hardDrive/docker/audiobookshelf/cache | /metadata/cache | covers/, images/, items/ |
| library (bind) | /mnt/hardDrive/docker/audiobookshelf/library | /audiobooks | empty (no NAS) |

**Verified:** All paths persist after `docker restart` and `docker compose down/up`.

### Network Isolation
```
Network: audiobookshelf_internal
Type: internal (no external access)
External networks: frontproxy_default (reverse proxy only)
Ports: expose: ["80"] — no ports: section → no host binding
```

## 5. Secret Scan

**Repository scan:** No secrets, tokens, passwords, or credentials found.
**Compose file:** No hardcoded secrets, no `secrets:` block, no `configs:` block.
**Documentation:** No credential values exposed.

> **Note on GH-59 overlap:** The source diff includes GH-59 proxy/TLS elements
> (VIRTUAL_HOST, LETSENCRYPT, frontproxy_default, vhost.d, proxy contract test)
> which are already merged on Architecture main. These are not part of GH-58
> acceptance scope. The table below only evaluates GH-58-specific criteria.
> See `manifest.json.scope_clarification` for the full breakdown.

## 6. Acceptance Criteria Mapping

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Gepinntes Image für linux/arm64 | **pass** | Digest `sha256:1eef67...`, `platform: linux/arm64` |
| 2 | Compose mit config/metadata/cache | **pass** | 4 volumes: config, metadata named + cache, library bind |
| 3 | Ressourcenlimits | **pass** | mem_limit 512m, cpus 1.0 |
| 4 | Restart-Policy | **pass** | `restart: unless-stopped` |
| 5 | Healthcheck | **pass** | HTTP GET localhost:80/ |
| 6 | docker compose config fehlerfrei | **pass** | Exit 0 |
| 7 | Container startet reproduzierbar healthy | **pass** | 8s first start, 8s after restart |
| 8 | Neustart erhält Config + DB | **pass** | absdatabase.sqlite (364KB) preserved |
| 9 | Kein unnötig öffentlicher Host-Port | **pass** | internal network only, no ports: section |
| 10 | Keine Secrets im Repository | **pass** | No secret strings in any committed file |
| 11 | Leere lokale Testbibliothek | **pass** | /audiobooks bind mount to empty /library |
| 12 | Kein NAS-Mount | **pass** | All mounts local HDD; no NFS exports |
