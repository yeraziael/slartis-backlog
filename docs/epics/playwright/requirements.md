# Playwright — Requirements

Normative keywords: **MUST** / **MUST NOT** / **REQUIRED** / **SHALL** / **SHALL NOT** / **SHOULD** / **SHOULD NOT** / **RECOMMENDED** / **MAY** / **OPTIONAL** per RFC 2119.

## 1. Shared Runner

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-001 | The runner **MUST** use a pinned Playwright container image with an immutable digest. | Confirmed | Planned |
| PWR-002 | The runner **MUST** be ephemeral — no permanently running browser service. | Confirmed | Planned |
| PWR-003 | The runner **MUST** support Chromium as the baseline browser. | Confirmed | Planned |
| PWR-004 | The runner **SHOULD** support Firefox and WebKit for cross-browser coverage. | Desired | Planned |
| PWR-005 | The runner **MUST** support both local (operator) and CI execution modes. | Confirmed | Planned |
| PWR-006 | The runner **MUST** produce deterministic exit codes (0 = pass, 1 = fail, 2 = prerequisite error). | Confirmed | Planned |

## 2. Ephemeral Execution

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-010 | Each test run **MUST** start from a clean browser context. | Confirmed | Planned |
| PWR-011 | State between test runs **MUST NOT** persist in the runner container. | Confirmed | Planned |
| PWR-012 | The runner container **MUST** be discarded after each run. | Confirmed | Planned |
| PWR-013 | Test identity secrets **MUST** be injected at container start, never baked into the image. | Confirmed | Planned |

## 3. Synthetic Keycloak Identities

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-020 | Automation **MUST** use synthetic Keycloak accounts, never real family accounts. | Confirmed | Planned |
| PWR-021 | Synthetic identities **MUST** contain no personal data. | Confirmed | Planned |
| PWR-022 | Synthetic identities **MUST** be visibly marked as automation accounts (username, display name). | Confirmed | Planned |
| PWR-023 | Each service **MUST** have at least three synthetic roles: E2E user, E2E admin, E2E denied. | Confirmed | Planned |
| PWR-024 | Synthetic accounts **MUST** receive only the minimum permissions needed for their test role. | Confirmed | Planned |
| PWR-025 | Synthetic account credentials **MUST** be rotatable without modifying test code. | Confirmed | Planned |

## 4. Evidence Manifests

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-030 | Every test run **MUST** produce a machine-readable evidence manifest. | Confirmed | Planned |
| PWR-031 | The manifest **MUST** include: source commit SHA, architecture commit SHA, service name, service version or image digest, environment, suite name, result. | Confirmed | Planned |
| PWR-032 | The manifest **MUST** be bound to the tested runtime state (container IDs, image digests). | Confirmed | Planned |
| PWR-033 | The manifest **SHOULD** be in JSON format. | Confirmed | Planned |
| PWR-034 | The evidence bundle **MUST** be suitable for inclusion in ACP review packages. | Confirmed | Planned |

## 5. Trace Retention Policy

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-040 | Playwright traces **MUST** be retained on test failure. | Confirmed | Planned |
| PWR-041 | Playwright traces **SHOULD** be suppressed on successful runs. | Confirmed | Planned |
| PWR-042 | Retained traces **MUST** be sanitised for secrets, tokens and personal data. | Confirmed | Planned |
| PWR-043 | Trace retention **MUST** have a configurable expiry. | Confirmed | Planned |

## 6. Screenshot Policy

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-050 | Screenshots **MUST** be captured on test failure. | Confirmed | Planned |
| PWR-051 | Screenshots **MAY** be captured on success if explicitly configured. | Desired | Planned |
| PWR-052 | Screenshots containing authenticated sessions **MUST NOT** expose tokens in visible UI elements. | Confirmed | Planned |

## 7. Browser Support

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-060 | Chromium **MUST** be the primary browser target. | Confirmed | Planned |
| PWR-061 | Firefox **SHOULD** be supported as a secondary target. | Desired | Planned |
| PWR-062 | WebKit **MAY** be supported as a tertiary target. | Desired | Planned |
| PWR-063 | Browser version **MUST** be pinned with the Playwright container image. | Confirmed | Planned |

## 8. Fixture Reuse

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-070 | Keycloak OIDC login **MUST** be a shared fixture usable by all service suites. | Confirmed | Planned |
| PWR-071 | Synthetic user-role mapping **MUST** be a shared fixture. | Confirmed | Planned |
| PWR-072 | Service URL and health prerequisite check **MUST** be a shared fixture. | Confirmed | Planned |
| PWR-073 | Console-error capture **MUST** be a shared fixture. | Confirmed | Planned |
| PWR-074 | Fixtures **MUST NOT** contain service-specific test logic. | Confirmed | Planned |

## 9. Page Object Conventions

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-080 | Service-specific interactions **SHOULD** use the Page Object Model. | Confirmed | Planned |
| PWR-081 | Shared UI patterns (login forms, navigation bars) **SHOULD** have shared page objects. | Confirmed | Planned |
| PWR-082 | Selectors **MUST** prefer data-testid or other stable attributes over CSS class names. | Confirmed | Planned |

## 10. Failure Classification

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-090 | Test results **MUST** distinguish browser-test failures from prerequisite failures. | Confirmed | Planned |
| PWR-091 | Prerequisite failures (DNS, TLS, Keycloak, container health) **MUST** report as `prerequisite_error`. | Confirmed | Planned |
| PWR-092 | A suite **MUST** fail closed when prerequisites cannot be verified. | Confirmed | Planned |
| PWR-093 | Infrastructure failures **MUST NOT** be reported as product regressions. | Confirmed | Planned |

## 11. CI Integration

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-100 | The runner **MUST** be invocable from Gitea Actions CI. | Confirmed | Planned |
| PWR-101 | Test results **MUST** be reported in JUnit format for CI consumption. | Confirmed | Planned |
| PWR-102 | Evidence artifacts **MUST** be retained as CI run artifacts. | Confirmed | Planned |
| PWR-103 | CI **MUST** support a retry policy for known transient infrastructure failures. | Confirmed | Planned |

## 12. ACP Evidence Compatibility

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-110 | Evidence bundles **MUST** be compatible with the ACP review package format. | Confirmed | Planned |
| PWR-111 | The manifest **MUST** include enough provenance data for a reviewer to verify the tested state. | Confirmed | Planned |

## 13. Service Onboarding Contract

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PWR-120 | Each service **MUST** document required user journeys before Playwright coverage is implemented. | Confirmed | Planned |
| PWR-121 | Each service **MUST** provide controlled test data for E2E tests. | Confirmed | Planned |
| PWR-122 | Each service **MUST** document why browser testing adds value beyond lower-layer tests. | Confirmed | Planned |
| PWR-123 | Onboarding **MUST NOT** require platform fixture changes for common patterns. | Desired | Planned |

## 14. Open Questions

| ID | Question | Relevant To |
|---|---|---|
| Q-001 | Which Playwright container image and version will be the baseline? | PWR-001 |
| Q-002 | Where will synthetic Keycloak accounts be managed (Keycloak realm, automation script)? | PWR-020 — PWR-025 |
| Q-003 | How long should evidence artifacts be retained in CI? | PWR-043 |
| Q-004 | What is the retry policy for transient infrastructure failures? | PWR-103 |
| Q-005 | Which Homelab services beyond Audiobookshelf and Jellyfin will adopt Playwright? | PWR-120 — PWR-123 |
| Q-006 | Will Firefox and WebKit support be implemented for the initial release? | PWR-061, PWR-062 |
