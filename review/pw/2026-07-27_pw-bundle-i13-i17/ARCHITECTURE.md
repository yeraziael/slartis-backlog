# Architecture — PW Bundle 2

## Current State

The Playwright test infrastructure (PW-I01–I12, delivered in PR #105) provides:
- Ephemeral Docker runner (`tests/playwright/runner/run.sh`) with dependency + test phases
- Platform tests (self-test, result semantics, manifest generation, prerequisite checks)
- Service tests with prerequisite checks against a live URL (`run.sh service:<base-url>`)
- OIDC/SSO shared fixtures in `tests/playwright/platform/shared-fixtures.spec.ts`
- Unauthenticated smoke test (`smoke-unauthenticated.spec.ts`)
- CI manifest with `lint`, `test-unit`, `report` stages

## Changes

### Test Directory Layout

```
tests/playwright/
├── platform/          # Platform-level tests (self-test, evidence, prerequisites, OIDC fixture)
├── services/
│   └── audiobookshelf/  # Service-level tests (authenticated smoke, library/playback, authorization)
│       ├── pages/
│       │   ├── authorization.ts    # PW-I15: AuthZ page object (role-based navigation checks)
│       │   ├── library.ts          # PW-I14: Library page object (card browsing, known title)
│       │   └── player.ts           # PW-I14: Player page object (play/pause)
│       ├── smoke-authenticated.spec.ts   # PW-I13: 5 SSO/login/logout scenarios
│       ├── library-playback.spec.ts      # PW-I14: 4 library/playback scenarios
│       └── authorization.spec.ts         # PW-I15: 8 role-based auth scenarios
├── runner/
│   └── run.sh        # Updated: service mode (no base URL) support
├── ci/
│   └── post-deploy.sh # PW-I17: Post-deployment smoke wrapper
```

### Runner Mode Expansion

The runner previously accepted `platform` and `service:<base-url>`. This bundle adds:
- **`service`** (no base URL): Runs `npm run test:service` without prerequisite checks. Used in CI where the deployed instance is assumed reachable.
- **`service:<base-url>`** (unchanged): Runs prerequisites against base-url, then `npm run test:service`.
- **`platform`**: Now runs `npm run test:platform` which targets only `platform/ evidence/ runner/` directories (was: entire test root).

### Script Separation

| Script | Target dirs |
|--------|------------|
| `npm run test:platform` | `platform/ evidence/ runner/` |
| `npm run test:service` | `services/` |

### CI Pipeline Extension

```
lint → test-unit → report → [post-deploy (main only)]
```

The `test-unit` stage now includes:
- `playwright-platform` (enabled): runs platform tests via Docker runner
- `playwright-service` (enabled): runs service tests via Docker runner

The `post-deploy` stage runs on main branch only:
- `smoke-audiobookshelf`: executes `tests/playwright/ci/post-deploy.sh`

### Interfaces and Data Flows

- Service tests read `PW_E2E_ABS_USER` and `PW_E2E_ABS_PASSWORD` environment variables for authentication
- Service tests target `PW_SERVICE_URL` (or fall back to the shared fixture's `SERVICE_URL`)
- The post-deploy wrapper delegates to `run.sh service` (no prereq checks)
- The manifest generator now produces correct `service_name` per suite (`playwright-platform` | `playwright-service`)

### Impact on Existing Responsibilities

- Existing platform tests (self-test, evidence, result-semantics) are unchanged
- OIDC shared fixtures (`shared-fixtures.spec.ts`) are re-used by all service test specs
- The `test:platform` npm script directory change (from `.` to `platform/ evidence/ runner/`) is backward-compatible for CI — platform tests continue to run in the same container
