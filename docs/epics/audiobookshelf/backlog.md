# Audiobookshelf — Backlog

## Child Issue Graph

This is the ordered list of executable child issues for the Audiobookshelf epic. Issues follow the dependency order defined in `README.md`. GitHub Issues track execution; this document is the authoritative ordering.

### Status Legend

- **DONE** — closed, merged, verified.
- **IN PROGRESS** — active implementation.
- **OPEN** — requirements defined, awaiting execution.
- **BLOCKED** — waiting on dependency.
- **PLANNED** — identified, not yet specified in GitHub.

## Completed Issues

### GH-58: Docker Service on Pi5

| Field | Value |
|---|---|
| **Status** | DONE — closed, merged |
| **Source PR** | Homelab/Architecture PR #63 |
| **Scope** | Compose file, persistent volumes, healthcheck, resource limits, test library |
| **Key Results** | Container running, healthy (~8 s), config/metadata on SSD, no host ports |
| **Docs** | `architecture.md`, `requirements.md` (R-070 — R-075, R-090 — R-095), `interfaces.md` §4 |

### GH-59: Reverse Proxy & TLS

| Field | Value |
|---|---|
| **Status** | DONE — closed, merged |
| **Source PRs** | Homelab/Architecture PRs #68, #70 |
| **Scope** | VIRTUAL_HOST, LETSENCRYPT, vhost.d, WebSocket, 27 contract tests |
| **Key Results** | `audiobookshelf.hl.maier.wtf` reachable via HTTPS, HTTP→HTTPS redirect, unlimited uploads, WebSocket working |
| **Docs** | `architecture.md`, `requirements.md` (R-110 — R-114), `interfaces.md` §2, `ci.md` |

## In Progress

### GH-60: Keycloak OIDC & SSO

| Field | Value |
|---|---|
| **Status** | IN PROGRESS — scripts versioned (PR #76), runtime execution pending |
| **Depends on** | GH-58, GH-59 |
| **Blocks** | OIDC-specific items in GH-62, ISSUE-HARDENING |
| **Scope** | OIDC Confidential Client, Authorization Code Flow, group-based access, `sub`-binding, auto-provisioning, RP-Initiated Logout, break-glass `admin`, secret rotation |
| **Docs** | `requirements.md` (R-020 — R-065, R-100 — R-104), `architecture.md` §Keycloak, `interfaces.md` §1, `contracts.md` §Keycloak OIDC, `security.md`, `testing.md` §Verification Matrix |

## Planned (Open GitHub Issues)

### GH-62: Configuration & Storage

| Field | Value |
|---|---|
| **Status** | OPEN — requirements defined |
| **Depends on** | GH-58 (storage layout). OIDC-specific env vars block on GH-60 |
| **Scope** | Persistent volume layout finalisation, environment variable documentation, backup strategy definition, restore procedure |
| **Docs** | `requirements.md` (R-090 — R-095, R-120 — R-124), `contracts.md` §Backup |

## Planned — Provisional (Not Yet in GitHub Issues)

The following issues were identified in GH-57 and `docs/epics/audiobookshelf/`. They use provisional identifiers (`ISSUE-NFS`, `ISSUE-IMPORT`, etc.) until GitHub issues are created. The count, scope and dependency ordering are subject to refinement during the corrected dependency review.

### ISSUE-NFS: NAS NFS Mount

| Field | Value |
|---|---|
| **Scope** | Mount `audiobooks` and `podcasts` NFSv3 shares from QNAP (192.168.2.141) on Pi5, configure fstab for auto-mount, bind-mount into Audiobookshelf container |
| **Depends on** | GH-62 (mount paths defined in GH-62). Does not require GH-60 |
| **Key Requirements** | R-080 — R-087 |
| **Docs** | `architecture.md` §NAS, `interfaces.md` §5, `contracts.md` §NAS/NFS, `operations.md` §NFS |

### ISSUE-IMPORT: Import Pipeline

| Field | Value |
|---|---|
| **Scope** | Design and implement the import pipeline component: ingest, analyse, normalise, duplicate detection, quarantine, library write, scan trigger |
| **Depends on** | ISSUE-NFS |
| **Key Requirements** | R-150 — R-174 |
| **Docs** | `architecture.md` §Control Flow, `interfaces.md` §8, `contracts.md` §Import Pipeline |

### ISSUE-METADATA: Metadata Enrichment

| Field | Value |
|---|---|
| **Scope** | Metadata provider integration, automatic enrichment during import, manual correction support |
| **Depends on** | ISSUE-IMPORT |
| **Key Requirements** | R-150 — R-152 |
| **Docs** | `requirements.md` §16 |

### ISSUE-BACKUP: Backup & Restore

| Field | Value |
|---|---|
| **Scope** | Automated backup of config/ and metadata/ directories, integrity verification, restore procedure |
| **Depends on** | GH-62 |
| **Key Requirements** | R-120 — R-124 |
| **Docs** | `contracts.md` §Backup, `interfaces.md` §6, `operations.md` §Backup |

### ISSUE-MONITORING: Monitoring Integration

| Field | Value |
|---|---|
| **Scope** | Health alerts, disk usage monitoring, NFS mount monitoring, container restart alerts, Homelab alerting integration (Telegram) |
| **Depends on** | GH-58 is sufficient (basic monitoring); enhanced monitoring after ISSUE-NFS |
| **Key Requirements** | R-130 — R-133 |
| **Docs** | `interfaces.md` §7, `contracts.md` §Monitoring |

### ISSUE-SCHEDULER: Automation & Scheduling

| Field | Value |
|---|---|
| **Scope** | Eddie job queue integration for scheduled imports, library scans, quarantine cleanup, metadata refresh |
| **Depends on** | ISSUE-IMPORT, ISSUE-BACKUP |
| **Docs** | `interfaces.md` §9, `roadmap.md` M9 |

### ISSUE-PODCAST-MGMT: Podcast Management

| Field | Value |
|---|---|
| **Scope** | Podcast RSS subscription management, podcast-specific import handling |
| **Depends on** | ISSUE-IMPORT |
| **Key Requirements** | R-006 |
| **Docs** | `requirements.md` §1 |

### ISSUE-HARDENING: Security Hardening & Penetration Testing

| Field | Value |
|---|---|
| **Scope** | Full security review, negative tests for OIDC token validation, network scanning, container hardening review |
| **Depends on** | GH-60 |
| **Docs** | `security.md` |

## Dependency Chain Summary

```
Layer 0: GH-57 (architecture)
             │
Layer 1:     └───→ GH-58 (Docker service)
                      │
                  ┌───┴────────────┐
                  ▼                   ▼
Layer 2:   GH-59 (proxy/TLS)    GH-62 (config/storage)
                  │                   └───────────────────┐
                  ▼                                       │
Layer 3:   GH-60 (OIDC)                                   │
                  │                                       ▼
                  │ (blocks only OIDC-specific items) ISSUE-NFS (NAS mount)
                  │                                       │
                  │             ┌─────────────────────────┼───────────────────┐
                  │             │                         │                   │
                  │             ▼                         ▼                   ▼
                  │     ISSUE-IMPORT               ISSUE-BACKUP         ISSUE-MONITORING
                  │             │                         │                   (basic: GH-58 suffices)
                  │             ▼                         ▼
                  │     ISSUE-METADATA              ISSUE-SCHEDULER
                  │             │
                  │             ▼
                  │     ISSUE-PODCAST-MGMT
                  │
                  └─────────────── ISSUE-HARDENING (requires GH-60 runtime)
```

## Total Estimated Issues

| Category | Count | Status |
|---|---|---|
| Completed (in GitHub) | 2 | #58, #59 |
| In Progress (in GitHub) | 1 | #60 |
| Planned (in GitHub) | 1 | #62 |
| Planned (not yet in GitHub) | 8 | NFS, Import, Metadata, Backup, Monitoring, Scheduler, Podcast, Hardening |
| **Total** | **12 provisional** | |

## Epic Completion Criteria

The Audiobookshelf epic is complete when:

1. All issues are closed.
2. All `MUST` requirements from `requirements.md` are verified.
3. The import pipeline operates without manual intervention.
4. Backup and restore are automated and tested.
5. Monitoring alerts reach the operator.
6. All open questions (Q-001 — Q-010) are resolved.
