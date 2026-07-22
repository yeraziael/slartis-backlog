# Playwright — Roadmap

## Milestone Overview

```
M0: Planning & Requirements ───── IN REVIEW (PR #82)
M1: Runner Foundation ──────────── PLANNED
M2: Shared Fixtures & Evidence ─── PLANNED
M3: Audiobookshelf Smoke Pilot ─── PLANNED
M4: Audiobookshelf Authorisation ─ PLANNED
M5: CI & Deployment Gating ─────── PLANNED
M6: Jellyfin Adoption ──────────── PLANNED
M7: Additional Services ────────── PLANNED
M8: Reliability & Maintenance ──── PLANNED
```

## Delivery Principle

Deliver a small shared platform, prove it against Audiobookshelf, then reuse the same fixtures, evidence contract and execution model for Jellyfin and later services. The roadmap separates platform capability from service-specific coverage. A service MUST NOT block adoption of the shared platform merely because its complete regression suite is unfinished.

## Milestone Details

### M0: Planning & Requirements (IN REVIEW)

| Item | Status | Source |
|---|---|---|
| Epic scope document | Done | PR #82 (initial version) |
| Plan-as-Code epic structure (14 documents) | IN REVIEW (PR #82) | This directory |
| Authority boundaries defined | Done | README.md |
| Synthetic identity model | Done | contracts.md, requirements.md |
| Evidence contract defined | Done | contracts.md |
| Decision register initialised | Done | decisions.md |
| Backlog with provisional issues | Done | backlog.md |

### M1: Runner Foundation (PLANNED)

| Item | Status |
|---|---|
| Pinned Playwright container image | Not started |
| Playwright configuration (`playwright.config.ts`) | Not started |
| Chromium baseline | Not started |
| Environment and service-target configuration | Not started |
| Local and CI-compatible entry commands | Not started |
| Deterministic exit codes (0, 1, 2) | Not started |
| Initial JUnit and JSON reporting | Not started |
| Failure-only trace and screenshot retention | Not started |

**Gate:** The runner executes a trivial test against a controlled endpoint from both operator invocation and CI context.

### M2: Shared Fixtures & Evidence (PLANNED)

| Item | Status |
|---|---|
| Keycloak OIDC login fixture | Not started |
| Synthetic user-role fixture | Not started |
| Service URL and health prerequisite fixture | Not started |
| Console-error capture | Not started |
| Screenshot and trace sanitisation policy | Not started |
| Evidence manifest generator | Not started |
| Source/architecture/version binding | Not started |
| Browser failure vs prerequisite classification | Not started |

**Gate:** A failed and a successful sample run both produce complete, machine-readable and commit-bound evidence without exposing secrets.

### M3: Audiobookshelf Smoke Pilot (PLANNED)

| Item | Status |
|---|---|
| HTTPS endpoint loads | Not started |
| HTTP redirect where applicable | Not started |
| Expected Audiobookshelf page rendered | Not started |
| Keycloak redirect and callback complete | Not started |
| Authorised E2E user can log in | Not started |
| Library page visible | Not started |
| Controlled test title can be opened | Not started |
| Playback can start and pause | Not started |
| Logout completes | Not started |
| Controlled test library contract defined | Not started |
| Evidence bundle for PR/ACP review | Not started |

**Gate:** An Audiobookshelf deployment can receive a functional smoke verdict without a human operating the frontend.

### M4: Audiobookshelf Authorisation (PLANNED)

| Item | Status |
|---|---|
| Denied user cannot enter service | Not started |
| Normal user lacks administrative functions | Not started |
| Administrator can reach admin functions | Not started |
| Changed/removed group membership affects access | Not started |
| Logout terminates application session | Not started |
| Invalid/incomplete auth flows fail closed | Not started |
| No secrets in retained evidence | Not started |
| Break-glass test (separate controlled suite) | Not started |

**Gate:** The browser suite proves both positive and negative access-control behaviour for the exact tested deployment.

### M5: CI & Deployment Gating (PLANNED)

| Item | Status |
|---|---|
| Pre-merge suite for deterministic tests | Not started |
| Post-deployment smoke suite | Not started |
| Explicit prerequisite/blocked result state | Not started |
| Retry policy for transient infrastructure | Not started |
| Artifact retention policy | Not started |
| ACP-compatible evidence handoff | Not started |
| Merge policy for test results | Not started |

**Gate:** A worker can execute, report and hand off tests without human clicks; the reviewer can verify coverage, provenance and result integrity.

### M6: Jellyfin Adoption (PLANNED)

| Item | Status |
|---|---|
| Login and logout | Not started |
| Permitted library visibility | Not started |
| Restricted library denial | Not started |
| Opening controlled media item | Not started |
| Playback start | Not started |
| User vs admin navigation and permissions | Not started |
| Transcoding initiation (deterministic only) | Not started |

**Gate:** Jellyfin reuses shared fixtures and evidence generation with only service-specific page objects and journeys added.

### M7: Additional Services (PLANNED)

| Item | Status |
|---|---|
| Candidate evaluation (dashboard, Paperless-ngx, Gitea) | Not started |
| Adopting service onboarding per contracts.md | Not started |
| Each service documents browser-test value proposition | Not started |

**Candidates:** family dashboard, Paperless-ngx critical workflows, Gitea operator-facing pages, future yt-dlp-sub web controls (if a UI exists).

For yt-dlp-sub, UI tests MUST remain complementary to CLI, API, download-decision, filesystem and import integration tests.

**Gate:** Each added service documents why browser testing is valuable and which lower-layer tests remain authoritative.

### M8: Reliability & Maintenance (PLANNED)

| Item | Status |
|---|---|
| Flaky-test quarantine policy | Not started |
| Selector and page-object conventions | Not started |
| Browser and Playwright upgrade procedure | Not started |
| Periodic synthetic-account review | Not started |
| Test-data reset strategy | Not started |
| Execution-time budgets | Not started |
| Trend reporting for failures and flakiness | Not started |
| Documented ownership for fixtures and service suites | Not started |

**Gate:** The suite has measurable reliability, bounded runtime and no permanently ignored failures.

## Dependency Graph

```
M0 Planning
   │
   v
M1 Runner Foundation
   │
   v
M2 Shared Fixtures + Evidence
   │
   v
M3 ABS Smoke Pilot
   │
   ├───────────────────┐
   v                   v
M4 ABS Auth        M5 CI/Gating
   │                   │
   └───────┬───────────┘
           v
     M6 Jellyfin
           │
           v
     M7 Additional Services
           │
           v
     M8 Reliability
```

M5 may begin once the Audiobookshelf smoke suite is stable; complete authorisation coverage is not a hard prerequisite for initial post-deployment smoke gating.

## Delivery Sequencing

| Phase | Milestones | Risk | Value |
|---|---|---|---|
| 1: Foundation (IN REVIEW) | M0 | Low | Approved scope, shared understanding |
| 2: Platform Core (NEXT) | M1, M2 | Low | Reproducible execution, reusable primitives |
| 3: First Consumer | M3, M4 | Medium | Automated smoke + auth for Audiobookshelf |
| 4: Integration | M5 | Medium | Evidence in workflow, no manual clicks |
| 5: Expansion | M6, M7 | Medium | Proved reusable across services |
| 6: Maturity | M8 | Low | Trustworthy, bounded runtime, maintained |

## Completion Criteria

The epic is complete when:

1. The shared runner is reproducible and pinned.
2. Synthetic identities and secrets are handled safely.
3. Evidence is machine-readable and bound to tested state.
4. Audiobookshelf smoke and authorisation suites are operational.
5. Deployment smoke tests no longer require routine human frontend interaction.
6. Jellyfin demonstrates reuse of the shared platform.
7. Lower-layer test boundaries are documented.
8. Flaky tests and artifact retention have enforceable policies.
9. Reviewers can make merge decisions from requirements, code and evidence without manually repeating scripted click paths.

## Status Legend

- **DONE** — implemented, deployed, verified.
- **IN REVIEW** — specification complete, pending merge.
- **PLANNED** — requirements defined, not started.
- **Not started** — no implementation work done.
