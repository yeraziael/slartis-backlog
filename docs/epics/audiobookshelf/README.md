# Audiobookshelf Epic

## Purpose

Deploy and operate Audiobookshelf as the authoritative audiobook and podcast serving platform in the Homelab. Serve audiobooks and podcasts to family members through a dedicated web application and mobile clients, backed by NAS-hosted media storage and Keycloak-authenticated access.

## Business and Household Value

- Centralised, self-hosted audiobook and podcast library accessible from any device.
- Family members authenticate through a single Homelab identity (Keycloak), no separate account management.
- Automated import pipeline normalises metadata, detects duplicates and quarantines uncertain matches before they reach the shared library.
- Operator-controlled break-glass access ensures recovery even when the identity provider is unavailable.

## Current Status

| Layer | Status | Source |
|-------|--------|--------|
| Docker service on Pi5 | Deployed | GH-58 (closed), Homelab/Architecture PR #63 |
| Reverse proxy & TLS | Deployed | GH-59 (closed), Homelab/Architecture PRs #68, #70 |
| Frontproxy ingress | Deployed | via nginx-proxy + acme-companion, standard Homelab pattern |
| Keycloak OIDC config | Planned, scripts versioned | GH-60 (open), Homelab/Architecture PR #76 |
| OIDC runtime execution | Pending | GH-60 (open), blocks GH-62 |
| Break-glass admin account | Planned | GH-60 (open), `break-glass-setup.sh` versioned |
| NAS media storage | Unmounted | NAS `192.168.2.141` identified, shares `audiobooks` + `podcasts` known, NFS mount not implemented |
| Import pipeline | Not started | Architecture boundary defined in GH-57 |
| Configuration & storage | Requirements defined, not implemented | GH-62 (open) |
| Monitoring | Not started | — |
| Backup & restore | Not started | — |
| Metadata normalisation | Not started | — |
| Duplicate detection | Not started | — |

## Scope

This epic covers the complete lifecycle of Audiobookshelf in the Homelab:

1. **Infrastructure**: Docker service, reverse proxy, TLS, persistent storage, NAS integration.
2. **Identity**: Keycloak OIDC authentication, authorisation, role mapping, break-glass access.
3. **Media pipeline**: Import, metadata normalisation, duplicate detection, quarantine workflow, library management.
4. **Operations**: Monitoring, health checks, backup, restore, secret rotation.
5. **Automation**: Scheduled import, library scans, cleanup, Eddie coordination.

## Non-Goals

- Audiobookshelf is **not** a general media server (no video, no music streaming — those are Jellyfin's domain).
- No modification of the Audiobookshelf upstream source code.
- No migration of other Homelab services to a different architecture.
- No changes to Keycloak beyond the Audiobookshelf client.
- No DNS, firewall or NAS configuration changes outside documented scope.

## Authority Model

Audiobookshelf planning spans three repositories. Each has a distinct authority domain:

| Domain | Authoritative Repository | Scope |
|---|---|---|
| Epic planning, requirements, roadmap, backlog, decision register | `yeraziael/slartis-backlog` (`docs/epics/audiobookshelf/`) | WHAT and WHY — epic scope, requirements, priorities, dependencies, decisions |
| Deployed architecture, Compose config, runtime scripts, hostnames, storage mappings | `Homelab/Architecture` (Gitea) | HOW — deployed infrastructure, runtime configuration, operational evidence |
| Execution state, acceptance evidence | GitHub issues (`yeraziael/slartis-backlog`) | STATUS — per-issue tracking, verification results, blockers |

**Conflict handling by domain:**
- Epic requirements in this directory prevail over implied requirements in issue comments.
- Deployed facts in `Homelab/Architecture` (actual port, image digest, mount path) prevail over planning assumptions in this directory.
- GitHub issue state (open/closed) is authoritative for execution status.

## Document Map

| Document | Domain | Purpose |
|----------|--------|---------|
| `README.md` | Epic | Entry point, status overview, authority model, document map |
| `requirements.md` | Epic | Functional and non-functional requirements |
| `architecture.md` | Epic | Service boundary, component model, trust boundaries, control/data flow |
| `interfaces.md` | Epic | Interface contracts to all external systems |
| `contracts.md` | Epic | Integration contracts, service-level agreements |
| `backlog.md` | Epic | Ordered child-issue graph for execution |
| `roadmap.md` | Epic | Milestone planning and delivery sequence |
| `ci.md` | Epic | CI/CD pipeline specification |
| `testing.md` | Epic | Test strategy and acceptance criteria |
| `security.md` | Epic | Security model, threat boundaries, secret handling |
| `operations.md` | Epic | Operational runbooks |
| `decisions.md` | Epic | Decision register |
| `references.md` | Epic | Cross-references to external documentation |

## Relationship to GitHub Issues

| GitHub Issue | State | Scope | Covers |
|---|---|---|---|
| #55 | Open | Homelab-wide | Keycloak authorisation model (Audiobookshelf is one client among many) |
| #57 | Open | Epic-level | ACP Pilot 1 — architecture baseline, component boundaries, child-issue graph |
| #58 | Closed | Infrastructure | Docker Compose service, persistent volumes, healthcheck |
| #59 | Closed | Infrastructure | Reverse proxy (VIRTUAL_HOST, LETSENCRYPT), TLS, WebSocket support |
| #60 | Open | Identity | Keycloak OIDC client, SSO, break-glass, logout |
| #62 | Open | Storage | Config layout, NFS mount planning, backup strategy |
| #77 | Open | Homelab-wide | Hostname registry, DNS baseline |

## High-Level Dependency Order

Dependencies are grouped by technical prerequisite. Items at the same level can proceed in parallel.

```
Foundation (DONE):
  GH-57 (architecture baseline)
    → GH-58 (Docker service)
      → GH-59 (reverse proxy & TLS)

Identity & Storage (parallelisable):
  GH-58 ──→ GH-59 ──→ GH-60 (Keycloak OIDC & SSO)
  GH-58 ──→ GH-62 (config & storage layout)           ← does not require GH-60 for storage design
  GH-60 blocks only OIDC-specific config in GH-62 (secrets, env vars)

Media Access:
  GH-62 ──→ NFS mount (NAS shares audiobooks + podcasts)

Media Pipeline:
  NFS mount ──→ Import pipeline (normalisation, duplicate detection, quarantine)
                     └── Metadata enrichment

Operations (parallel after prerequisites met):
  GH-58 ──→ Basic monitoring (healthcheck already deployed)
  NFS mount ──→ Enhanced monitoring (NFS mount alerts)
  GH-62 ──→ Backup & Restore design
  GH-62 ──→ Automation & Scheduler (Eddie integration)

Hardening (after OIDC runtime):
  GH-60 ──→ Security hardening & negative tests
```

GH-55 (Keycloak authorisation) and GH-77 (hostname registry) are Homelab-wide dependencies that influence but are not blocked by this epic.

## Status Legend

- **Confirmed**: Verified fact from existing source.
- **Planned**: Intended design decision, not yet verified.
- **Assumption**: Reasonable inference, not yet confirmed by any source.
- **Open question**: Required information not yet available.
- **Blocked**: Cannot proceed until a dependency is resolved.

## Migration Provenance

This documentation was created on 2026-07-22 by migrating information from:

- GitHub issues #55, #57, #58, #59, #60, #62, #77 and their comments.
- `Homelab/Architecture` repository (Gitea): `docs/AUDIOBOOKSHELF.md`, PRs #56–#63, #68, #70, #76.
- `yeraziael/slartis-backlog` EPICS/media-platform/ directory.
- `yeraziael/slartis-backlog` review packages for GH-57, GH-58, GH-59.
- `yeraziael/slartis-backlog` PROTOCOL.md, context.md.

## Authority Statement

**This Git documentation is authoritative.** GitHub Issues contain only execution scope, acceptance criteria and evidence. If a conflict exists between an issue comment and a document in this directory, the document prevails. Issues are updated to reference the document version, not the other way around.
