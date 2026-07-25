# Playwright — Decision Register

## Purpose

This register records architectural and planning decisions for the Playwright epic. It is **not** a substitute for Architecture Decision Records (ADRs). Cross-epic or Homelab-wide decisions belong in `docs/adrs/`. This register tracks decisions scoped to this epic.

Stable decision IDs are prefixed `PWDEC-`. Status values: `Accepted`, `Implemented`, `Proposed`, `Superseded`.

## Register

### PWDEC-001: Shared Platform

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Decision** | Playwright is a shared, cross-cutting browser test platform, not a private dependency of any single service epic |
| **Rationale** | Avoid duplicating browser test infrastructure per service; consistent evidence format, shared fixtures, single runner maintenance |
| **Alternatives** | Each service owns its own Playwright setup (duplicated effort, inconsistent evidence, harder to maintain) |
| **Consequences** | Platform team maintains runner, fixtures, evidence generation; service epics define coverage; onboarding contract required |
| **Source** | PR #82 |
| **Related ADR** | None |

### PWDEC-002: Ephemeral Runner

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Decision** | The Playwright runner MUST be ephemeral — a fresh container per run, no permanently running browser service |
| **Rationale** | Deterministic execution, no state leakage between runs, no persistent attack surface, CI-native pattern |
| **Alternatives** | Persistent browser service (state leakage, maintenance overhead, single point of failure) |
| **Consequences** | Container startup time added to each run; credentials injected at container start; container discarded after each run |
| **Source** | PR #82, PWR-002 |
| **Related ADR** | None |

### PWDEC-003: Synthetic Identities

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Decision** | Automation MUST use synthetic Keycloak accounts, never real family accounts. Three roles per service: user, admin, denied |
| **Rationale** | No risk of personal data exposure in test evidence; deterministic role mapping; credentials can be rotated without service impact |
| **Alternatives** | Real user accounts (data privacy risk, cannot control permissions), mocks (do not test real OIDC flow) |
| **Consequences** | Keycloak administration overhead for synthetic accounts; credential rotation procedure; naming convention `pw-e2e-<service>-<role>` |
| **Source** | PR #82, PWR-020 — PWR-025 |
| **Related ADR** | None |

### PWDEC-004: Evidence-First Reviews

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Decision** | Every test run produces a machine-readable evidence manifest bound to source commit, service version and runtime state. Reviewers evaluate evidence, not routine click paths |
| **Rationale** | Non-repudiation of tested state; reviewer can verify exactly what was tested and against which deployment; ACP-compatible |
| **Alternatives** | Screenshot-only evidence (no provenance, no machine readability), no evidence (cannot verify what was tested) |
| **Consequences** | Evidence manifest schema must be maintained; evidence sanitisation required; CI artifact retention policy needed |
| **Source** | PR #82, PWR-030 — PWR-034, PWR-110, PWR-111 |
| **Related ADR** | None |

### PWDEC-005: Browser Boundaries

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Decision** | Playwright covers only browser-observable behaviour. It does not replace unit, API, integration, infrastructure, backup or performance tests |
| **Rationale** | Clear responsibility boundaries prevent scope creep and brittle test suites. Lower-layer tests remain authoritative for their domain |
| **Alternatives** | Playwright as universal test tool (brittle, slow, tests wrong layer) |
| **Consequences** | Service epics must document which lower-layer tests remain authoritative; Playwright results never override failing lower-layer tests |
| **Source** | PR #82, README.md (Non-Goals) |
| **Related ADR** | None |

### PWDEC-006: Implementation in Homelab/Architecture

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Decision** | Playwright implementation code lives in `Homelab/Architecture/tests/playwright/`. This repository (`yeraziael/slartis-backlog`) holds epic scope, requirements and roadmap |
| **Rationale** | `Homelab/Architecture` is the authoritative repository for deployed configuration and runtime tests. Consistent with existing service patterns |
| **Alternatives** | Separate repository (additional maintenance), slartis-backlog (mixes epic planning with implementation) |
| **Consequences** | Two repositories must stay aligned; epic changes in slartis-backlog may require implementation changes in Homelab/Architecture |
| **Source** | PR #82, README.md §Authority Boundaries |
| **Related ADR** | None |

### PWDEC-007: Chromium Baseline

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Decision** | Chromium is the primary and required browser target. Firefox and WebKit are secondary targets |
| **Rationale** | Chromium offers best Playwright support, fastest execution, broadest feature coverage. All Homelab services are tested against Chromium-based browsers in production |
| **Alternatives** | Firefox primary (slower, some Playwright features limited), equal multi-browser (increased CI time and maintenance) |
| **Consequences** | Firefox and WebKit support deferred to post-MVP; cross-browser coverage is a desired but not required feature |
| **Source** | PR #82, PWR-060 — PWR-063 |
| **Related ADR** | None |

### PWDEC-008: Failure Classification

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Decision** | Test results MUST distinguish browser-test failures from prerequisite failures. Exit code 2 = prerequisite error, not test failure |
| **Rationale** | Infrastructure and product concerns are orthogonal. A DNS outage must not be reported as a product regression |
| **Alternatives** | All failures treated equally (infrastructure outages block releases), no prerequisite check (tests fail with confusing messages) |
| **Consequences** | Prerequisite check step required before any test suite; separate reporting channel for infrastructure issues; retry policy limited to known transient conditions |
| **Source** | PR #82, PWR-090 — PWR-093 |
| **Related ADR** | None |
