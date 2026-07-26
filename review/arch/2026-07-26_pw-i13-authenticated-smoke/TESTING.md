# Testing: PW-I13 Audiobookshelf Authenticated Smoke

## Tests Executed

### Local Validation

| Step | Command | Result |
|------|---------|--------|
| Lint | `make lint` (shellcheck, shfmt, yamllint, ci-generate check, pytest) | PASS |
| Unit tests | `make test` (bats: test_bats, test_playwright_identities, test_playwright_config, ci_generator) | PASS |
| Diff check | `git diff --check` | PASS |

### Playwright Spec (not runnable in CI yet — no CI integration)

The spec `smoke-authenticated.spec.ts` defines 4 test cases:

| # | Test | Description |
|---|------|-------------|
| 1 | `login success redirects to library landing` | Logs in via Keycloak, verifies URL is not `/login` |
| 2 | `login callback failure stays on login page` | Navigates to login, verifies page stays on `/login` |
| 3 | `logout terminates local session and redirects` | Full login → logout cycle, verifies redirect |
| 4 | `post-logout reload remains unauthenticated` | Login → logout → reload, verifies still unauth |

**Note:** These tests require a running Keycloak and Audiobookshelf instance
with valid `PW_E2E_ABS_USER`/`PW_E2E_ABS_PASSWORD` credentials. They are
not yet registered in CI and must be run manually.

### CI Status

No CI run for Playwright specs yet. The CI manifest step `playwright-identities`
(PW-I09) validates the provisioning script, not the Playwright specs themselves.
Playwright CI integration is deferred to PW-D05 follow-up.

## Schema Validations

| Schema | Result |
|--------|--------|
| `governance/schemas/review-manifest-schema.yaml` | pending validation |

## Known Test Gaps

- No CI registration for Playwright specs (deferred to PW-D05)
- No Playwright config `projects` entry for `services/audiobookshelf` yet
- No `playwright.config.ts` integration — specs rely on `@playwright/test` defaults
- No test for denied role (PW-I17), admin role (PW-I15), or playback (PW-I16)
- No shared OIDC fixture (deferred to PW-I11)
