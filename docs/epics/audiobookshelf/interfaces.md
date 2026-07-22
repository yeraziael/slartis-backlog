# Audiobookshelf — Interfaces

## Interface Overview

```
┌─────────────────┐     ┌──────────────────┐
│   Keycloak      │◄───►│                  │
│   (OIDC IdP)    │     │                  │
└─────────────────┘     │                  │
                         │  Audiobookshelf  │
┌─────────────────┐     │                  │
│  frontproxy      │◄───►│                  │
│  (nginx-proxy    │     └──┬───────────────┘
│   + acme)        │        │
└─────────────────┘         │
                            │
┌──────────────────┐        │
│  Docker Compose  │◄───────┘
│  Runtime         │
└──────────────────┘

(Planned interfaces below)

┌──────────────────┐     ┌──────────────────┐
│  QNAP NAS        │◄───►│  Import Pipeline │
│  (NFSv3)         │     │  (future)        │
└──────────────────┘     └──────┬───────────┘
                                │
┌──────────────────┐            │
│  Monitoring      │◄───────────┘
│  System (future) │
└──────────────────┘

┌──────────────────┐
│  Backup System   │
│  (future)        │
└──────────────────┘

┌──────────────────┐
│  Automation      │
│  (Eddie, future) │
└──────────────────┘
```

---

## 1. Interface: Keycloak (OIDC)

| Field | Value |
|---|---|
| **Direction** | Audiobookshelf → Keycloak (outbound) |
| **Protocol** | HTTPS / OIDC Authorization Code Flow |
| **Authentication** | OIDC Confidential Client with Client Secret |
| **Port** | 443 (Homelab internal, Keycloak endpoint) |

### Data Exchanged

| Data | Direction | Description |
|---|---|---|
| Authorization Request | ABS → KC | `response_type=code`, `client_id=audiobookshelf`, `redirect_uri`, `scope=openid+profile+email+groups`, `state` |
| Authorization Code | KC → Browser | Redirect to ABS callback URI |
| Token Request | ABS → KC | `code`, `client_id`, `client_secret`, `redirect_uri`, `grant_type=authorization_code` |
| Token Response | KC → ABS | `access_token`, `id_token`, `refresh_token`, `token_type=Bearer`, `expires_in` |
| Userinfo | ABS → KC | `GET /protocol/openid-connect/userinfo` (optional, if needed) |
| Logout Request | ABS → KC | `GET /protocol/openid-connect/logout?id_token_hint=...&post_logout_redirect_uri=...` |
| JWKS | ABS → KC | `GET /protocol/openid-connect/certs` for token signature validation |

### Claims Used

| Claim | Source | Purpose |
|---|---|---|
| `sub` | ID Token / Userinfo | Stable, persistent user identifier; primary key in local ABS database |
| `preferred_username` | ID Token / Userinfo | Display name |
| `email` | ID Token / Userinfo | User information (optional) |
| `groups` | ID Token (via Keycloak mapper) | `audiobookshelf-users`, `audiobookshelf-admins` for authorisation |

### Failure Behaviour

| Failure | Impact | Recovery |
|---|---|---|
| Keycloak unreachable | New logins impossible; existing sessions continue until token expiry | Restore Keycloak service |
| Invalid token | Login denied with error message | User re-authenticates |
| Token expired | Silent refresh fails; user prompted to re-login | Automatic via refresh token |
| Client secret invalid | Token request returns HTTP 401 | Rotate secret, update ABS config, restart |
| Missing `sub` claim | Login denied | Check Keycloak client mapper configuration |
| Unauthorised group | Login denied with access error | Operator grants `audiobookshelf-users` in Keycloak |

### Ownership

| Aspect | Owner |
|---|---|
| Keycloak realm configuration | Operator |
| Keycloak client `audiobookshelf` | Operator (via versioned script in Homelab/Architecture) |
| OIDC client secret | Operator (runtime secret, not in version control) |
| Audiobookshelf OIDC config | Slarti (versioned in Homelab/Architecture) |

### Current Status

**Confirmed** — OIDC integration scripts versioned in Homelab/Architecture PR #76 (`pi/audiobookshelf/scripts/setup-keycloak.sh`). Runtime execution pending (GH-60 open).

---

## 2. Interface: Reverse Proxy (frontproxy)

| Field | Value |
|---|---|
| **Direction** | frontproxy → Audiobookshelf (inbound) |
| **Protocol** | HTTP (Docker internal network) |
| **Authentication** | None at proxy level; authentication at application level |
| **Port** | 80 (Audiobookshelf container, internal only) |

### Configuration

| Parameter | Value |
|---|---|
| VIRTUAL_HOST | `audiobookshelf.hl.maier.wtf` |
| VIRTUAL_PORT | `80` |
| LETSENCRYPT_HOST | `audiobookshelf.hl.maier.wtf` |
| LETSENCRYPT_EMAIL | `webmaster@maier.wtf` |
| expose | `["80"]` |
| networks | `audiobookshelf_internal`, `frontproxy_default` |
| vhost.d | `client_max_body_size 0` (unlimited uploads) |
| vhost.d | WebSocket `Upgrade` and `Connection` proxy headers |

### Data Exchanged

| Data | Direction | Description |
|---|---|---|
| HTTP requests | Proxy → ABS | Proxied user requests (browser, mobile app) |
| HTTP responses | ABS → Proxy | Audiobookshelf pages, API responses, media streams |
| WebSocket connections | Proxy → ABS | Upgraded WebSocket connections (playback sync) |
| Health check responses | ABS → Proxy | HTTP 200 on `/status` (used by Docker, not proxy) |

### Failure Behaviour

| Failure | Impact | Recovery |
|---|---|---|
| ABS container unhealthy | Proxy returns 502 Bad Gateway | Restart ABS container, verify health |
| Proxy network misconfiguration | Service unreachable externally | Correct compose network config, recreate container |
| TLS certificate expired | Browser shows certificate warning | Verify acme-companion functioning, check DNS |
| VIRTUAL_PORT mismatch | Proxy routes to wrong port → 502 | Correct VIRTUAL_PORT in compose |

### Ownership

| Aspect | Owner |
|---|---|
| nginx-proxy + acme-companion | Lydia (deployed, operational) |
| Compose configuration (proxy env vars) | Slarti (versioned in Homelab/Architecture) |
| vhost.d configuration | Slarti (versioned in Homelab/Architecture) |
| DNS record | Operator (via STRATO) |
| Domain maier.wtf | Operator |

### Current Status

**Deployed** — GH-59 closed. PRs #68 and #70 merged. Effective configuration verified.

---

## 3. Interface: DNS and Hostname Registry

| Field | Value |
|---|---|
| **Direction** | Audiobookshelf → DNS (resolved by clients) |
| **Protocol** | DNS (via STRATO, public resolution) |
| **Authentication** | N/A |
| **Port** | 53 (standard DNS) |

### Registry Entry

| Field | Value | Status |
|---|---|---|
| FQDN | `audiobookshelf.hl.maier.wtf` | Confirmed |
| Short name | `audiobookshelf` | Confirmed |
| Service | Audiobookshelf | Confirmed |
| Category | Public | Confirmed |
| Status | Production | Deployed |
| DNS record type | CNAME or A | Open question |
| DNS target | Pi5 public IP via frontproxy | Assumption |
| TLS | Let's Encrypt (acme-companion) | Confirmed |
| SSO | Keycloak OIDC | Configuration pending runtime |
| Source reference | GH-59, GH-77 | Confirmed |

### Ownership

| Aspect | Owner |
|---|---|
| DNS zone (maier.wtf) | Operator (STRATO) |
| Hostname registry | Operator (GH-77) |

### Current Status

**Confirmed** — FQDN in use. Registry being established (GH-77 open).

---

## 4. Interface: Docker Compose Runtime

| Field | Value |
|---|---|
| **Direction** | Compose file → Docker Engine (declarative) |
| **Protocol** | Docker Compose (YAML), Docker Engine API |
| **Authentication** | Docker socket (local, Unix domain socket) |
| **Port** | N/A (local) |

### Data Exchanged

| Data | Direction | Description |
|---|---|---|
| Container specification | Compose → Docker | Image, resources, networks, volumes, env vars |
| Container status | Docker → Operator | Health, logs, restart count |
| Volume mounts | Compose → Docker | Bind mount config/ and metadata/ from SSD |

### Parameters

| Parameter | Value |
|---|---|
| Image | `ghcr.io/advplyr/audiobookshelf@sha256:1eef6716183c52abafe5405e7d6be8390248ecd59c7488c44af871757ac8fc4d` |
| Container name | `audiobookshelf` |
| Restart policy | `unless-stopped` |
| Memory limit | 512 MB |
| CPU limit | 1.0 |
| Security opt | `no-new-privileges:true` |
| Logging | json-file, max-size 10m, max-file 7 |
| Healthcheck | CMD node -e GET /status, interval 15s, timeout 10s, retries 5, start_period 60s |

### Failure Behaviour

| Failure | Impact | Recovery |
|---|---|---|
| Image digest mismatch | Container won't start | Verify image tag/digest, pull correct image |
| Volume path missing | Container won't start | Create directory on Pi5, verify permissions |
| Port conflict | Container won't start | Check no other container binds same port |
| Healthcheck failing | Container marked unhealthy | Check logs, verify application responding |

### Ownership

| Aspect | Owner |
|---|---|
| Compose file | Slarti (versioned in Homelab/Architecture) |
| Docker runtime on Pi5 | Lydia (operational) |
| Volume directory creation | Lydia (deployment) |

### Current Status

**Deployed** — Compose file working, container healthy, config/metadata persisted. GH-58 closed.

---

## 5. Interface: NAS / NFS (Planned)

| Field | Value |
|---|---|
| **Direction** | Pi5 → QNAP NAS (outbound NFS client) |
| **Protocol** | NFSv3 |
| **Authentication** | IP-based access control (assumed) |
| **Port** | 2049 (NFS) |

### Data Exchanged

| Data | Direction | Description |
|---|---|---|
| Audiobook files | NAS → Audiobookshelf | Read-only access to audiobook files |
| Podcast files | NAS → Audiobookshelf | Read-only access to podcast files |

### Mount Configuration (Planned)

| Share | Pi5 Mount Path | Container Path | Access |
|---|---|---|---|
| `audiobooks` | `/mnt/ro/nas_audiobooks` | `/media/audiobooks` | Read-only |
| `podcasts` | `/mnt/ro/nas_podcasts` | `/media/podcasts` | Read-only |

### NFS Mount Options (Planned)

```
rsize=8192,wsize=8192,hard,intr,noatime
```

### Failure Behaviour

| Failure | Impact | Recovery |
|---|---|---|
| NAS unreachable | Media unavailable; Audiobookshelf may be slow or error | Restore NAS connectivity |
| NFS permission denied | Media not visible to container | Check NAS export options and IP allowlist |
| NFS mount point empty | Media not visible | Verify NAS share contents and export path |

### Ownership

| Aspect | Owner |
|---|---|
| NAS export configuration | Operator (QNAP admin interface) |
| Pi5 NFS mount | Lydia (via versioned fstab or script) |
| Docker bind mount | Slarti (versioned in compose file) |

### Current Status

**Planned** — Architecture defined in GH-57. NAS share names confirmed. Not yet implemented.

---

## 6. Interface: Backup System (Planned)

| Field | Value |
|---|---|
| **Direction** | Audiobookshelf → Backup target |
| **Protocol** | TBD (tarball, rsync, or native ABS backup) |
| **Authentication** | TBD |
| **Port** | TBD |

### Data to Back Up

| Path | Contents | Criticality |
|---|---|---|
| `/mnt/hardDrive/audiobookshelf/config/` | SQLite database (user data, playback state, config) | Critical |
| `/mnt/hardDrive/audiobookshelf/metadata/` | Cached covers, images, items, logs, streams | Important |
| NAS media | Not part of ABS backup (NAS-level backup only) | Excluded |

### Failure Behaviour

| Failure | Impact | Recovery |
|---|---|---|
| No backup | Data loss on SSD failure | Implement backup before production use |
| Restore not tested | False sense of security | Test restore procedure |

### Ownership

| Aspect | Owner |
|---|---|
| Backup strategy | Slarti (part of GH-62) |
| Backup execution | Eddie / cron |
| Restore procedure | Operator |

### Current Status

**Not started** — Backup requirement documented in GH-62. No implementation.

---

## 7. Interface: Monitoring System (Planned)

| Field | Value |
|---|---|
| **Direction** | Monitoring system → Audiobookshelf (polling) |
| **Protocol** | HTTP health endpoint / Docker events |
| **Authentication** | None (health endpoint internal only) |
| **Port** | 80 (internal) |

### Health Check Endpoint

| Parameter | Value |
|---|---|
| Endpoint | `GET /status` |
| Expected status | HTTP 200 |
| Interval | 15 s |
| Timeout | 10 s |
| Retries | 5 |
| Start period | 60 s |

### Metrics to Monitor (Proposed)

| Metric | Source | Alert |
|---|---|---|
| Container health | Docker healthcheck | Unhealthy for 3 consecutive checks |
| Restart count | Docker events | > 2 restarts in 5 minutes |
| Disk usage (config/) | Pi5 filesystem | > 90% |
| NFS mount status | Pi5 mount check | Mount not present |
| Memory usage | Docker stats | > 80% of 512 MB limit |

### Ownership

| Aspect | Owner |
|---|---|
| Healthcheck script | Slarti (in compose file) |
| Monitoring integration | Open question |

### Current Status

**Not started** — Container healthcheck deployed. No Homelab monitoring integration yet.

---

## 8. Interface: Import Pipeline (Planned)

| Field | Value |
|---|---|
| **Direction** | Import service → NAS (write) + Audiobookshelf (trigger scan) |
| **Protocol** | NFS (write to NAS) + HTTP (ABS API for scan trigger) |
| **Authentication** | NFS: IP-based; ABS API: OIDC Bearer token |
| **Port** | NFS 2049, ABS API 80 (internal) |

### Data Exchanged

| Data | Direction | Description |
|---|---|---|
| Audiobook files | Import → NAS | Normalised audiobook files written to NAS library directory |
| Quarantine items | Import → Quarantine | Uncertain duplicate matches moved to quarantine directory |
| Scan trigger | Import → ABS | `POST /api/libraries/{id}/scan` to trigger library scan |
| Import status | Import → Logs | Structured import logs for audit |

### Failure Behaviour

| Failure | Impact | Recovery |
|---|---|---|
| Import fails mid-way | Partial or no files written | Idempotent retry; source material preserved |
| Duplicate not detected | Duplicate in library | Manual cleanup via ABS web UI |
| Quarantine full | Quarantine overflow | Operator review required |
| ABS unreachable for scan | New media not indexed | Manual scan or retry |

### Ownership

| Aspect | Owner |
|---|---|
| Import service design | Slarti |
| Import execution | Lydia |
| Quarantine review | Operator |

### Current Status

**Not started** — Architecture boundary defined in GH-57. 18 child issues identified. No implementation.

---

## 9. Interface: Automation / Scheduler (Planned)

| Field | Value |
|---|---|
| **Direction** | Scheduler → Import pipeline / ABS |
| **Protocol** | HTTP API / Eddie job queue |
| **Authentication** | Eddie service account |
| **Port** | TBD |

### Scheduled Tasks (Proposed)

| Task | Frequency | Actor |
|---|---|---|
| Import new media | On demand or daily | Eddie → Lydia |
| Library scan | After each import batch | Eddie → ABS API |
| Cleanup quarantined items | Weekly | Operator |
| Metadata refresh | Weekly | Import pipeline |
| Backup | Daily | Eddie |
| Health check | Every 5 minutes | Healthcheck timer |

### Ownership

| Aspect | Owner |
|---|---|
| Scheduler (Eddie) | Slarti / Operator |
| Import job creation | Lydia |

### Current Status

**Not started** — Child issue #17 (Scheduling) identified in GH-57. No implementation.

---

## 10. Interface: Human Review Workflow (Planned)

| Field | Value |
|---|---|
| **Direction** | Operator → Quarantine (manual) |
| **Protocol** | Manual (web UI, file manager) |
| **Authentication** | Operator Keycloak identity |
| **Port** | N/A |

### Workflow Steps

1. Import pipeline places uncertain matches in quarantine directory.
2. Operator receives notification (Telegram, planned).
3. Operator reviews quarantined item metadata and content.
4. Operator decides: accept (move to library) or reject (delete or return to source).
5. If accepted, library scan is triggered.

### Ownership

| Aspect | Owner |
|---|---|
| Notification | Eddie / Telegram |
| Review decision | Operator |
| Quarantine cleanup | Operator or automated sweep |

### Current Status

**Not started** — Requirement defined in GH-57. Quarantine path not created.
