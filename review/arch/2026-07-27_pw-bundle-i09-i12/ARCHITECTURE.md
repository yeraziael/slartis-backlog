# Architecture: PW-I09/I10/I11/D05/I12 Bundle

## Current State

PW-I01–I08 established the Playwright runner platform, evidence manifests, sanitisation, and prerequisite checks. No service-level fixtures or tests existed.

## New Components

### Shared Fixtures (`tests/playwright/fixtures/`)

| File | Purpose | PWR Ref |
|------|---------|---------|
| `service.ts` | Typed env parsing, service URL/health check fixture | PWR-072 |
| `roles.ts` | User/admin/denied role selection from env vars | PWR-071 |
| `console.ts` | Filtered console-error capture with allowlist | PWR-073 |
| `oidc.ts` | Keycloak OIDC login/logout fixture (service-neutral) | PWR-070 |
| `fake-oidc.ts` | Fake OIDC harness for deterministic fixture self-tests | — |

### Platform Self-Tests (`tests/playwright/platform/`)

| File | Tests | Coverage |
|------|-------|----------|
| `shared-fixtures.spec.ts` | 10 | Service env parsing, role resolution, console capture |
| `oidc-fixture.spec.ts` | 7 | Redirect, callback, credentials, logout, session cleanup, secrets |

### Service Suite (`tests/playwright/services/audiobookshelf/`)

| File | Purpose |
|------|---------|
| `pages/login.ts` | Login page object (root navigation, SSO button, main content) |
| `smoke-unauthenticated.spec.ts` | 5-scenario unauthenticated smoke (HTTPS, render, SSO, title) |

### Identity Provisioning (`pi/`)

| File | Purpose |
|------|---------|
| `audiobookshelf/scripts/setup-playwright-identities.sh` | Idempotent Keycloak identity provisioning |
| `tests/test_playwright_identities.sh` | 13 mock tests for provisioning script |

### Documentation

| File | Content |
|------|---------|
| `docs/playwright-synthetic-identities.md` | Identity contract (naming, rotation, injection) |
| `docs/decisions/playwright/audiobookshelf-onboarding.md` | Onboarding contract (journeys, selectors, prereqs) |

## Data Flow

```
spec → fixtures/service.ts → SERVICE_URL env → health check
spec → fixtures/roles.ts → PW_E2E_ABS_* env → role identity
spec → fixtures/console.ts → page.on('console') → filtered errors
spec → fixtures/oidc.ts → Keycloak login → storage state
spec → services/audiobookshelf/pages/login.ts → ABS page interactions
```

## Impact

Purely additive. No existing files modified. Establishes the fixture architecture for all subsequent PW-I* issues.
