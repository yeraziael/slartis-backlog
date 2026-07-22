# Audiobookshelf — Roadmap

## Milestone Overview

```
M0: Architecture & Planning ──── DONE
M1: Docker Deployment ────────── DONE
M2: Reverse Proxy & TLS ──────── DONE
M3: Identity & Access ────────── IN PROGRESS (GH-60)
M4: Storage & Configuration ──── PLANNED (GH-62)
M5: NAS Integration ──────────── PLANNED
M6: Import Pipeline ──────────── PLANNED
M7: Operations & Monitoring ──── PLANNED
M8: Backup & Restore ─────────── PLANNED
M9: Automation & Scheduler ───── PLANNED
```

## Milestone Details

### M0: Architecture & Planning (DONE)

| Item | Status | Source |
|---|---|---|
| Architecture baseline document (AUDIOBOOKSHELF.md) | Done | GH-57, Homelab/Architecture PR #61 |
| Child-issue dependency graph (18 issues) | Done | GH-57 |
| ACP Pilot 1 review | Approved | GH-57 |
| Epic migration to Plan-as-Code | Done | This directory |

### M1: Docker Deployment (DONE)

| Item | Status | Source |
|---|---|---|
| Compose file with pinned image | Deployed | GH-58, PR #63 |
| Persistent config volume | Deployed | GH-58 |
| Persistent metadata volume | Deployed | GH-58 |
| Test library volume | Deployed | GH-58 |
| Healthcheck configured | Deployed | GH-58, GH-65 |
| Resource limits (512 MB, 1 CPU) | Deployed | GH-58 |
| Internal network isolation | Deployed | GH-58 |

### M2: Reverse Proxy & TLS (DONE)

| Item | Status | Source |
|---|---|---|
| VIRTUAL_HOST configured | Deployed | GH-59, PR #68, #70 |
| Let's Encrypt TLS | Deployed | GH-59 |
| vhost.d with unlimited uploads | Deployed | GH-59 |
| WebSocket support | Deployed | GH-59 |
| 27 contract tests passing | Verified | GH-59, Run #613 |

### M3: Identity & Access (IN PROGRESS)

| Item | Status | Source |
|---|---|---|
| Keycloak OIDC Confidential Client | Scripts versioned | GH-60, PR #76 |
| Authorization Code Flow | Scripts versioned | GH-60 |
| Group-based access (users/admins) | Scripts versioned | GH-60 |
| `sub`-based identity binding | Scripts versioned | GH-60 |
| Auto-provisioning | Scripts versioned | GH-60 |
| RP-Initiated Logout | Scripts versioned | GH-60 |
| Break-glass `admin` setup | Scripts versioned | GH-60 |
| Secret rotation | Scripts versioned | GH-60 |
| **Runtime execution** | **Pending** | **GH-60** |
| **Login/Logout verification** | **Pending** | **GH-60** |
| **Negative security tests** | **Pending** | **GH-60** |

**Blocker:** GH-60 must be completed before M4 can begin.

### M4: Storage & Configuration (PLANNED)

| Item | Status | Source |
|---|---|---|
| Persistent volume layout finalised | Requirements defined | GH-62 |
| Environment variables (non-secret) documented | Requirements defined | GH-62 |
| Backup strategy defined | Requirements defined | GH-62 |
| Restore procedure documented | Requirements defined | GH-62 |
| OIDC secret handling & env vars | Requirements defined | GH-62 (blocks on GH-60) |
| **Implementation** | **Not started** | **GH-62** |

**Depends on:** GH-58 (Docker volumes exist). OIDC-specific items block on GH-60; storage layout and backup design can proceed independently.

### M5: NAS Integration (PLANNED)

| Item | Status |
|---|---|
| NFS mount `audiobooks` from NAS | Not started |
| NFS mount `podcasts` from NAS | Not started |
| fstab entry for auto-mount | Not started |
| Container bind mount for NAS paths | Not started |
| Read-only volume verification | Not started |
| NFS availability monitoring | Not started |

**Details:** NAS 192.168.2.141, NFSv3, shares `audiobooks` + `podcasts`. Mount to `/mnt/ro/nas_audiobooks` and `/mnt/ro/nas_podcasts`.

### M6: Import Pipeline (PLANNED)

| Item | Status |
|---|---|
| Import service design | Not started |
| Metadata normalisation | Not started |
| Duplicate detection (content-based) | Not started |
| Quarantine workflow | Not started |
| Replacement workflow (9-step) | Not started |
| Library scan trigger | Not started |
| Retention policy | Not started |

### M7: Operations & Monitoring (PLANNED)

| Item | Status |
|---|---|
| Homelab monitoring integration | Not started |
| Container health alerts | Not started |
| Disk usage alerts | Not started |
| NFS mount alerts | Not started |
| Import pipeline monitoring | Not started |

### M8: Backup & Restore (PLANNED)

| Item | Status |
|---|---|
| Automated config backup | Not started |
| Automated metadata backup | Not started |
| Backup integrity verification | Not started |
| Restore procedure documented | Not started |
| Restore test (quarterly) | Not started |

### M9: Automation & Scheduler (PLANNED)

| Item | Status |
|---|---|
| Scheduled import jobs (Eddie) | Not started |
| Scheduled library scans | Not started |
| Quarantine cleanup scheduling | Not started |
| Metadata refresh scheduling | Not started |

## Dependency Graph

```
Foundation (Layer 1):
  M0 ──→ M1 ──→ M2

Layer 2 (parallel):
  M2 ──→ M3 (OIDC, blocks only secret items)
  M1 ──→ M4 (storage & config, independent of M3)
            │
Layer 3:     └──→ M5 (NAS mount, needs M4 paths)
                     │
Layer 4:              ├──→ M6 (import pipeline, needs mounted media)
                      ├──→ M7 (monitoring, adds NFS alerts)
                      │
Layer 5:              └──→ M8 (backup, needs documented layout from M4)
                              └──→ M9 (automation, needs defined ops)
```

M3 (OIDC) blocks only identity-dependent items across all milestones. Storage layout, backup design, and basic monitoring can start before OIDC is deployed.

## Delivery Sequencing

| Phase | Milestones | Risk | Value |
|---|---|---|---|
| 1: Foundation (DONE) | M0, M1, M2 | Low | Service running, externally accessible |
| 2: Identity (NOW) | M3 | Medium | SSO, family access, security |
| 3: Storage (NEXT) | M4, M5 | Medium | Persistent data, media available |
| 4: Media Pipeline | M6 | High | Data integrity, normalisation |
| 5: Operations | M7, M8, M9 | Low | Reliability, automation |

## Status Legend

- **DONE** — implemented, deployed, verified.
- **Deployed** — running in production.
- **IN PROGRESS** — active implementation.
- **Scripts versioned** — code ready, not yet executing.
- **PLANNED** — requirements defined, not started.
- **Not started** — no implementation work done.
