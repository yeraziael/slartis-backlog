# Testing: PW-I13 Audiobookshelf Authenticated Smoke

## Tests Executed

### Local Validation

| Step | Command | Result |
|------|---------|--------|
| Lint | `make lint` (shellcheck, shfmt, yamllint, ci-generate check, pytest) | PASS |
| Unit tests | `make test` (bats: test_bats, test_playwright_identities, test_playwright_config, ci_generator) | PASS |
| Diff check | `git diff --check` | PASS |

### Playwright Spec Execution (2026-07-26)

**Command:** `node node_modules/@playwright/test/cli.js test --config=playwright.config.ts --project=chromium tests/playwright/services/audiobookshelf/smoke-authenticated.spec.ts`

**Environment:** rechenknecht, headless Chromium 149.0.7827.55, no `PW_E2E_ABS_USER`/`PW_E2E_ABS_PASSWORD` set.

| # | Test | Result | Evidence |
|---|------|--------|----------|
| 1 | `login success redirects to library landing` | **FAIL** (credential gate) | `PW_E2E_ABS_USER and PW_E2E_ABS_PASSWORD must be set for authenticated smoke tests. Skipping.` |
| 2 | `invalid credentials stays on Keycloak login with error` | **FAIL** (timeout) | ABS redirected to Keycloak; no Keycloak SSO button found. `getByRole('button', { name: /keycloak\|log in with keycloak/i })` timed out at 30s. |
| 3 | `logout terminates local session and redirects` | **FAIL** (credential gate) | Same as #1 |
| 4 | `post-logout reload remains unauthenticated` | **FAIL** (credential gate) | Same as #1 |
| 5 | `revisit protected route after logout requires re-authentication` | **FAIL** (credential gate) | Same as #1 |

**Interpretation:**
- Tests 1, 3, 4, 5: Credential gate works as designed — fails fast with a clear message when env vars are absent. No silent pass, no empty-string credential fill.
- Test 2: Ran against live `audiobookshelf.hl.maier.wtf`. ABS redirects to Keycloak login; the login button selector does not match the live Keycloak page. This is a real selector mismatch that will need fixing before live execution with credentials.

### CI Status

No CI run for Playwright specs yet. The CI manifest step `playwright-identities`
(PW-I09) validates the provisioning script, not the Playwright specs themselves.
Playwright CI integration is deferred to PW-D05 follow-up.

## Schema Validations

| Schema | Result |
|--------|--------|
| `governance/schemas/review-manifest-schema.yaml` | PASS (exit 0) |

## Known Test Gaps

- No CI registration for Playwright specs (deferred to PW-D05)
- No Playwright config `projects` entry for `services/audiobookshelf` yet
- Live Keycloak login button selector needs updating after live test (test 2 finding)
- No test for denied role (PW-I17), admin role (PW-I15), or playback (PW-I16)
- No shared OIDC fixture (deferred to PW-I11)
- Credentials need provisioning via `setup-playwright-identities.sh --commit` before live test run
