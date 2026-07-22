# Homelab Browser Test Platform — Roadmap

## Delivery Principle

Deliver a small shared platform, prove it against Audiobookshelf, then reuse the same fixtures, evidence contract and execution model for Jellyfin and later services.

The roadmap separates platform capability from service-specific coverage. A service MUST NOT block adoption of the shared platform merely because its complete regression suite is unfinished.

## Phase 0 — Planning Baseline

### Objective

Approve scope, authority boundaries, test levels, synthetic identity model and evidence contract.

### Outputs

- accepted epic plan;
- agreed repository location in `Homelab/Architecture`;
- named Audiobookshelf pilot journeys;
- privacy and secret-handling rules;
- definition of smoke, regression and E2E acceptance suites.

### Gate

A reviewer can identify what Playwright covers, what remains below the browser layer and which evidence is required for merge decisions.

## Phase 1 — Runner Foundation

### Objective

Create a reproducible, ephemeral Playwright runner.

### Outputs

- pinned Playwright container image;
- Playwright configuration;
- Chromium baseline;
- environment and service-target configuration;
- local and CI-compatible entry commands;
- deterministic exit codes;
- initial JUnit and JSON reporting;
- failure-only trace and screenshot retention.

### Gate

The runner executes a trivial test against a controlled endpoint from both an operator invocation and the intended worker/CI context.

## Phase 2 — Shared Fixtures and Evidence

### Objective

Implement reusable platform primitives before service-specific tests proliferate.

### Outputs

- Keycloak login fixture;
- synthetic user-role fixture;
- service URL and health prerequisite fixture;
- console-error capture;
- screenshot and trace sanitisation policy;
- evidence manifest generator;
- binding to source commit, architecture commit, service version or image digest and environment;
- clear classification of browser failure versus prerequisite failure.

### Gate

A failed and a successful sample run both produce complete, machine-readable and commit-bound evidence without exposing secrets.

## Phase 3 — Audiobookshelf Smoke Pilot

### Objective

Replace routine manual deployment clicks with a minimal automated acceptance suite.

### Initial Coverage

- HTTPS endpoint loads;
- HTTP redirect where applicable;
- expected Audiobookshelf page is rendered;
- Keycloak redirect and callback complete;
- authorised E2E user can log in;
- library page is visible;
- controlled test title can be opened;
- playback can start and pause;
- logout completes.

### Outputs

- `services/audiobookshelf/smoke.spec.ts` or equivalent;
- controlled test library contract;
- post-deployment invocation;
- evidence bundle suitable for PR or ACP review.

### Gate

An Audiobookshelf deployment can receive a functional smoke verdict without a human operating the frontend.

## Phase 4 — Audiobookshelf Authorization and Negative Tests

### Objective

Automate the high-value security and role regression paths.

### Coverage

- denied user cannot enter the service;
- normal user lacks administrative functions;
- administrator can reach required administration functions;
- changed or removed group membership changes effective access according to the service contract;
- logout terminates the expected application session;
- invalid or incomplete authentication flows fail closed;
- browser-visible secrets or tokens are not emitted into retained evidence.

Break-glass testing MUST run separately from normal smoke tests and MUST use a controlled recovery procedure.

### Gate

The browser suite proves both positive and negative access-control behaviour for the exact tested deployment.

## Phase 5 — CI and Deployment Gating

### Objective

Integrate Playwright into the implementation and review workflow without making transient infrastructure failures indistinguishable from product regressions.

### Outputs

- pre-merge suite for deterministic tests;
- post-deployment smoke suite;
- explicit prerequisite or blocked result state;
- retry policy limited to known transient infrastructure conditions;
- artifact retention policy;
- ACP-compatible evidence handoff;
- merge policy defining which suites are required for which change classes.

### Gate

A worker can execute, report and hand off tests without human clicks, while the reviewer can verify coverage, provenance and result integrity.

## Phase 6 — Jellyfin Adoption

### Objective

Prove that the platform is reusable rather than Audiobookshelf-specific.

### Coverage

- login and logout;
- permitted library visibility;
- restricted library denial;
- opening a controlled media item;
- playback start;
- user versus administrator navigation and permissions;
- transcoding initiation only where it can be observed deterministically without brittle UI assumptions.

### Gate

Jellyfin reuses shared fixtures and evidence generation with only service-specific page objects and journeys added.

## Phase 7 — Additional Services

### Objective

Adopt the platform selectively where browser automation provides meaningful assurance.

### Candidates

- family dashboard;
- Paperless-ngx critical workflows;
- Gitea or other operator-facing services;
- future yt-dlp-sub web controls, if such a UI exists.

For yt-dlp-sub, UI tests MUST remain complementary to CLI, API, download-decision, filesystem and import integration tests.

### Gate

Each added service documents why browser testing is valuable and which lower-layer tests remain authoritative.

## Phase 8 — Reliability and Maintenance

### Objective

Keep the suite trustworthy and inexpensive to operate.

### Outputs

- flaky-test quarantine policy;
- selector and page-object conventions;
- browser and Playwright upgrade procedure;
- periodic synthetic-account review;
- test-data reset strategy;
- execution-time budgets;
- trend reporting for failures and flakiness;
- documented ownership for fixtures and service suites.

### Gate

The suite has measurable reliability, bounded runtime and no permanently ignored failures.

## Dependency Overview

```text
Phase 0 Planning
       |
       v
Phase 1 Runner
       |
       v
Phase 2 Shared Fixtures + Evidence
       |
       v
Phase 3 ABS Smoke
       |
       +-------------------+
       v                   v
Phase 4 ABS Auth       Phase 5 CI/Gating
       |                   |
       +---------+---------+
                 v
         Phase 6 Jellyfin
                 |
                 v
       Phase 7 Additional Services
                 |
                 v
       Phase 8 Reliability
```

Phase 5 may begin once the Audiobookshelf smoke suite is stable; complete authorization coverage is not a hard prerequisite for initial post-deployment smoke gating.

## Suggested First Execution Issues

1. Define the Playwright runner and pinned-image contract.
2. Implement the evidence manifest and failure artifacts.
3. Provision synthetic Keycloak test identities without personal data.
4. Implement Audiobookshelf unauthenticated endpoint smoke tests.
5. Implement Audiobookshelf OIDC login and logout.
6. Add controlled library and playback smoke flow.
7. Add Audiobookshelf user, admin and denied-role tests.
8. Integrate post-deployment execution and ACP evidence handoff.
9. Add Jellyfin pilot coverage.
10. Define maintenance, flake and upgrade policy.

These are provisional execution units and SHOULD be refined into small issues after the platform contracts are reviewed.

## Completion Criteria

The epic is complete when:

- the shared runner is reproducible and pinned;
- synthetic identities and secrets are handled safely;
- evidence is machine-readable and bound to tested state;
- Audiobookshelf smoke and authorization suites are operational;
- deployment smoke tests no longer require routine human frontend interaction;
- Jellyfin demonstrates reuse of the shared platform;
- lower-layer test boundaries are documented;
- flaky tests and artifact retention have enforceable policies;
- reviewers can make merge decisions from requirements, code and evidence without manually repeating scripted click paths.
