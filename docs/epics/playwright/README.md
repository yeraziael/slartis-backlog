# Homelab Browser Test Platform

## Purpose

Establish Playwright as the shared browser-based functional and regression test layer for web-facing Homelab services.

The objective is to remove routine human interaction from reproducible frontend acceptance tests. A human reviewer remains responsible for architecture, security posture, test adequacy, subjective UX and final merge decisions; scripted functional verification is executed by a Vekling or CI runner.

## Scope

The platform provides reusable browser automation for:

- Audiobookshelf as the pilot service;
- Jellyfin as the second service;
- other browser-based Homelab services where UI-level verification adds value;
- OIDC login flows through Keycloak;
- role and permission checks;
- deployment smoke tests;
- frontend regression tests;
- machine-readable evidence bound to the tested source and runtime state.

`yt-dlp-sub` is included only where a browser-accessible management interface exists. Its download, filesystem and import behaviour remains primarily covered by CLI, API, integration and filesystem tests.

## Non-Goals

Playwright does not replace:

- unit tests;
- API and contract tests;
- Docker, network and storage tests;
- NFS interruption tests;
- backup and restore tests;
- load and performance testing;
- malware or media-file validation;
- subjective UX acceptance.

## Architectural Position

Playwright is a cross-cutting test platform, not a private implementation detail of one service epic.

```text
Planer / Reviewer
  defines requirements, coverage and acceptance gates
          |
          v
Slarti
  designs and versions service-specific suites
          |
          v
Vekling / CI Runner
  executes tests against the exact deployment candidate
          |
          v
Evidence Bundle
  results + traces + screenshots + tested commit/runtime identity
          |
          v
Reviewer / Merge Gate
```

The runner SHOULD be ephemeral and use a pinned Playwright container image. It MUST NOT require a permanently running browser service.

## Proposed Repository Layout

The authoritative implementation belongs in `Homelab/Architecture` because it tests deployed runtime state and service configuration.

```text
tests/playwright/
├── playwright.config.ts
├── fixtures/
│   ├── auth.ts
│   ├── users.ts
│   └── services.ts
├── helpers/
│   ├── evidence.ts
│   ├── health.ts
│   └── keycloak.ts
├── contracts/
│   ├── access-control.spec.ts
│   ├── oidc.spec.ts
│   └── tls.spec.ts
└── services/
    ├── audiobookshelf/
    ├── jellyfin/
    └── <future-service>/
```

This repository remains authoritative for epic scope, requirements, roadmap and backlog. `Homelab/Architecture` is authoritative for runner implementation, deployed test configuration and runtime evidence.

## Test Levels

### Smoke

Runs after deployment and SHOULD complete within a few minutes.

Minimum checks:

- HTTPS endpoint reachable;
- expected page loads;
- login flow completes;
- one critical user action succeeds;
- logout succeeds;
- no unexpected browser-console errors in the covered flow.

### Regression

Runs for releases or relevant changes.

Covers navigation, permissions, session behaviour, core workflows, negative paths and previously fixed defects.

### End-to-End Acceptance

Uses deterministic test identities and controlled test data. It verifies a complete user journey and emits reviewable evidence.

## Test Identities

Automation MUST use synthetic accounts, never real family accounts.

Initial roles:

- service E2E user;
- service E2E administrator;
- service E2E denied or unassigned user.

Test identities MUST contain no personal data, MUST be visibly marked as automation accounts and MUST receive only the minimum permissions needed for their test role. Secrets MUST be injected at runtime and MUST NOT appear in source control, logs, screenshots, traces or PR text.

## Evidence Contract

Each run MUST produce a machine-readable manifest bound to the tested state.

Minimum fields:

```json
{
  "source_commit": "<commit-sha>",
  "architecture_commit": "<commit-sha>",
  "service": "audiobookshelf",
  "service_version": "<version-or-digest>",
  "environment": "<environment>",
  "suite": "smoke",
  "result": "pass"
}
```

Recommended bundle:

```text
test-results/
├── manifest.json
├── results.json
├── junit.xml
├── screenshots/
├── traces/
└── videos/
```

Screenshots, traces and videos SHOULD be retained on failure and MAY be suppressed on successful runs to minimise secret and privacy exposure.

## Pilot: Audiobookshelf

The Audiobookshelf pilot SHOULD automate at least:

- HTTP to HTTPS behaviour;
- public endpoint loading;
- Keycloak redirect and return flow;
- authorised user login;
- unauthorised user denial;
- administrator access;
- user versus administrator permission differences;
- library visibility using controlled test content;
- opening a title;
- starting and pausing playback;
- logout;
- break-glass login only in a separately controlled recovery test.

The pilot MUST distinguish browser-test failures from infrastructure failures such as unavailable DNS, TLS, Keycloak, NFS or container health.

## Expansion Targets

### Jellyfin

Add library visibility, user restrictions, playback, administration and—where deterministically observable—transcoding initiation.

### yt-dlp-sub

Use Playwright only for browser-facing controls. Test configuration parsing, download decisions, imports and filesystem effects below the UI layer.

## Governance

- Service epics define required user journeys and acceptance criteria.
- The shared platform defines fixtures, evidence format and execution conventions.
- A Vekling or CI runner executes the tests.
- Slarti maintains implementations and resolves failures.
- The reviewer evaluates coverage and evidence, not routine click paths.
- A passing UI suite MUST NOT override failing lower-level tests.
- Tests MUST fail closed when prerequisites, identities or evidence binding are ambiguous.

## Status

Planned. Audiobookshelf is the first implementation pilot.
