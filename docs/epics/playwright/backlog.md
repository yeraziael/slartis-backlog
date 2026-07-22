# Playwright — Backlog

## Child Issue Graph

This is the ordered list of executable child issues for the Playwright epic. GitHub Issues track execution; this document is the authoritative ordering.

### Status Legend

- **IN REVIEW** — specification complete, pending merge.
- **PLANNED** — identified, not yet specified in GitHub.
- **BLOCKED** — waiting on dependency.
- **DONE** — closed, merged, verified.

## Planned Issues

### PW-01: Define Playwright Runner and Pinned-Image Contract

| Field | Value |
|---|---|
| **Status** | PLANNED |
| **Depends on** | M0 (this epic) |
| **Scope** | Select base Playwright container image, pin by digest, create runner entry point, define configuration file, verify deterministic exit codes |
| **Key Requirements** | PWR-001 — PWR-006 |
| **Docs** | `requirements.md` §1, `architecture.md` §Runtime, `contracts.md` §Browser Prerequisites |

### PW-02: Implement Evidence Manifest and Failure Artifacts

| Field | Value |
|---|---|
| **Status** | PLANNED |
| **Depends on** | PW-01 |
| **Scope** | Implement manifest generator, JUnit reporter, screenshot/trace capture on failure, evidence bundle directory structure |
| **Key Requirements** | PWR-030 — PWR-043, PWR-050 — PWR-052 |
| **Docs** | `contracts.md` §Evidence Manifest, §Screenshot, §Trace, `interfaces.md` §4 |

### PW-03: Provision Synthetic Keycloak Test Identities

| Field | Value |
|---|---|
| **Status** | PLANNED |
| **Depends on** | PW-01 (runner exists to test against) |
| **Scope** | Create Keycloak realm or group for Playwright test accounts, create `pw-e2e-abs-user`, `pw-e2e-abs-admin`, `pw-e2e-abs-denied`, document rotation procedure |
| **Key Requirements** | PWR-020 — PWR-025 |
| **Docs** | `contracts.md` §Synthetic Test Identities, `security.md` §Synthetic Identities |

### PW-04: Implement Audiobookshelf Unauthenticated Smoke Tests

| Field | Value |
|---|---|
| **Status** | PLANNED |
| **Depends on** | PW-01, PW-02 |
| **Scope** | HTTPS endpoint reachable, HTTP redirect, page renders, public endpoint check, console error capture |
| **Key Requirements** | PWR-090 — PWR-093 |
| **Docs** | `testing.md` §Smoke, `interfaces.md` §1 |

### PW-05: Implement Audiobookshelf OIDC Login and Logout

| Field | Value |
|---|---|
| **Status** | PLANNED |
| **Depends on** | PW-03, PW-04 |
| **Scope** | OIDC login fixture, authorised user login, logout, session termination verification |
| **Key Requirements** | PWR-070 — PWR-074 |
| **Docs** | `testing.md` §Smoke, `interfaces.md` §2 |

### PW-06: Add Controlled Library and Playback Smoke Flow

| Field | Value |
|---|---|
| **Status** | PLANNED |
| **Depends on** | PW-05 |
| **Scope** | Controlled test library with known test title, library navigation, title open, playback start/pause |
| **Key Requirements** | PWR-080 — PWR-082 |
| **Docs** | `testing.md` §E2E Acceptance, `contracts.md` §Service Onboarding |

### PW-07: Add Audiobookshelf Authorisation Tests

| Field | Value |
|---|---|
| **Status** | PLANNED |
| **Depends on** | PW-05, PW-06 |
| **Scope** | Denied user cannot enter, user lacks admin functions, admin has admin functions, group change affects access, negative auth flows |
| **Key Requirements** | PWR-090 — PWR-093 |
| **Docs** | `testing.md` §Regression, `testing.md` §Service Acceptance |

### PW-08: Integrate Post-Deployment Execution and ACP Evidence Handoff

| Field | Value |
|---|---|
| **Status** | PLANNED |
| **Depends on** | PW-04 (smoke exists to integrate) |
| **Scope** | Gitea Actions workflow for Playwright, post-deployment trigger, evidence artifact upload, ACP review package compatibility |
| **Key Requirements** | PWR-100 — PWR-103, PWR-110, PWR-111 |
| **Docs** | `ci.md`, `interfaces.md` §3 |

### PW-09: Add Jellyfin Pilot Coverage

| Field | Value |
|---|---|
| **Status** | PLANNED |
| **Depends on** | PW-08 (CI integration), Jellyfin epic readiness |
| **Scope** | Reuse shared fixtures, implement Jellyfin page objects, smoke tests, auth tests |
| **Key Requirements** | PWR-120 — PWR-123 |
| **Docs** | `testing.md` §Service Acceptance, `contracts.md` §Service Onboarding |

### PW-10: Define Maintenance, Flake and Upgrade Policy

| Field | Value |
|---|---|
| **Status** | PLANNED |
| **Depends on** | PW-08 (operational experience) |
| **Scope** | Flaky-test quarantine procedure, selector conventions, Playwright upgrade procedure, synthetic account review cadence, test-data lifecycle, execution-time budgets, ownership documentation |
| **Key Requirements** | — |
| **Docs** | `operations.md`, `roadmap.md` M8 |

## Dependency Chain Summary

```
M0 (Planning — this epic)
 │
 └── PW-01 (Runner)
       │
       ├───────────────────┐
       v                   v
   PW-02 (Evidence)    PW-03 (Synthetic IDs)
       │                   │
       └────────┬──────────┘
                v
            PW-04 (ABS Smoke — unauthenticated)
                │
                v
            PW-05 (ABS OIDC Login)
                │
                ├───────────────────┐
                v                   v
            PW-06 (ABS Playback) PW-07 (ABS Auth)
                │                   │
                └────────┬──────────┘
                         v
                     PW-08 (CI Integration)
                         │
                         ├───────────────────┐
                         v                   v
                     PW-09 (Jellyfin)    PW-10 (Maintenance)
```

## Total Estimated Issues

| Category | Count | Status |
|---|---|---|
| Planned (not yet in GitHub) | 10 | PW-01 through PW-10 |

Epic completion triggers creation of these issues in GitHub as child issues. Each issue SHOULD be refined, scoped and estimated before implementation begins.

## Epic Completion Criteria

The Playwright epic is complete when:

1. All issues are closed.
2. All `MUST` requirements from `requirements.md` are verified.
3. Audiobookshelf smoke and authorisation suites are operational.
4. Jellyfin demonstrates reuse of the shared platform.
5. CI integration produces review-ready evidence without human clicks.
6. Reliability maintenance is documented and enforced.
7. All open questions (Q-001 — Q-006) are resolved.
