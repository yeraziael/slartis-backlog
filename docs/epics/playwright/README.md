# Playwright — Homelab Browser Test Platform

## Status

**PLANNING** — Epic specification in review. No implementation started.

## Scope

Playwright provides a shared, reproducible browser-based test layer for web-facing Homelab services. It removes routine human interaction from reproducible frontend acceptance tests while preserving human responsibility for architecture, security, coverage adequacy, subjective UX and merge decisions.

### In Scope

- Shared ephemeral Playwright runner with pinned container image.
- Reusable fixtures: Keycloak OIDC login, synthetic user roles, service health prerequisites.
- Evidence manifests binding test results to source commit, service version and runtime state.
- Smoke, regression and E2E acceptance test levels.
- Audiobookshelf as the pilot consumer service.
- Jellyfin as the second planned consumer.
- Future Homelab services with browser-based UIs may opt in.
- OIDC login flows, role and permission checks, deployment smoke tests, frontend regression tests.

### Out of Scope

Playwright complements and does not replace:

- Unit tests.
- API and contract tests.
- Docker, network and storage tests.
- NFS interruption tests.
- Backup and restore tests.
- Load and performance testing.
- Malware or media-file validation.
- Subjective UX acceptance.

## Epic Dependency Graph

```
Playwright Platform Epic (this directory)
         │
         ├── Planning & Requirements ───── IN REVIEW (PR #82)
         │
         ├── Runner Foundation ──────────── PLANNED
         │
         ├── Shared Fixtures & Evidence ─── PLANNED
         │
         ├── Audiobookshelf Pilot ───────── PLANNED
         │
         ├── CI & Deployment Gating ─────── PLANNED
         │
         ├── Jellyfin Adoption ──────────── PLANNED
         │
         ├── Additional Services ────────── PLANNED
         │
         └── Reliability & Maintenance ──── PLANNED
```

The Playwright platform epic is a dependency of every adopting service epic. Each service epic defines required user journeys and acceptance criteria; the platform provides the execution infrastructure.

## Authority Boundaries

| Domain | Repository | Authority |
|---|---|---|
| Epic scope, requirements, roadmap, backlog | `yeraziael/slartis-backlog` (`docs/epics/playwright/`) | This directory |
| Runner implementation, deployed config, runtime evidence | `Homelab/Architecture` (`tests/playwright/`) | Implementation authority |
| Service-specific test coverage | `Homelab/Architecture` (per service suite) | Defined by each service epic |

`yeraziael/slartis-backlog` is authoritative for what Playwright covers, why and when. `Homelab/Architecture` is authoritative for how it runs, what it tests and which evidence it produces.

## Epic Documents

| Document | Purpose |
|---|---|
| `README.md` | This file — epic overview, scope, authority boundaries |
| `requirements.md` | Normative requirements with stable IDs |
| `architecture.md` | System architecture, trust boundaries, responsibility model |
| `interfaces.md` | Interface specifications between components |
| `contracts.md` | Normative contracts for evidence, identities, onboarding |
| `security.md` | Security model, threat analysis, secret handling |
| `operations.md` | Operational procedures, maintenance, flake handling |
| `testing.md` | Test strategy, levels, evidence validation |
| `ci.md` | CI integration, artifact retention, gating |
| `roadmap.md` | Milestone-based delivery plan |
| `backlog.md` | Ordered execution backlog with provisional issue IDs |
| `decisions.md` | Architectural decision register |
| `references.md` | Cross-references to related issues, PRs, documents |

## Delivery Sequencing

| Phase | Milestones | Risk | Value |
|---|---|---|---|
| 1: Foundation | M0 (Planning) | Low | Approved scope, shared understanding |
| 2: Platform Core | M1 (Runner), M2 (Fixtures) | Low | Reproducible execution, reusable primitives |
| 3: First Consumer | M3 (ABS Smoke), M4 (ABS Auth) | Medium | Automated smoke coverage for Audiobookshelf |
| 4: Integration | M5 (CI Gating) | Medium | Evidence in workflow, no manual clicks |
| 5: Expansion | M6 (Jellyfin), M7 (More Services) | Medium | Proved reusable |
| 6: Maturity | M8 (Reliability) | Low | Trustworthy, bounded runtime, maintained |
