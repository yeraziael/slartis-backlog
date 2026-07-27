# Implementation — PW Bundle 2

## Files Changed (15 files, +520/-13)

| File | Status | Lines | Issue |
|------|--------|-------|-------|
| `tests/playwright/services/audiobookshelf/smoke-authenticated.spec.ts` | **new** | +118 | PW-I13 |
| `tests/playwright/services/audiobookshelf/pages/library.ts` | **new** | +37 | PW-I14 |
| `tests/playwright/services/audiobookshelf/pages/player.ts` | **new** | +19 | PW-I14 |
| `tests/playwright/services/audiobookshelf/library-playback.spec.ts` | **new** | +55 | PW-I14 |
| `tests/playwright/services/audiobookshelf/pages/authorization.ts` | **new** | +38 | PW-I15 |
| `tests/playwright/services/audiobookshelf/authorization.spec.ts` | **new** | +83 | PW-I15 |
| `tests/playwright/package.json` | modified | +2/-1 | PW-I16 |
| `tests/playwright/runner/run.sh` | modified | +20/-3 | PW-I16 |
| `tests/playwright/ci/post-deploy.sh` | **new** | +31 | PW-I17 |
| `docs/playwright-ci-runbook.md` | **new** | +76 | PW-I17 |
| `ci-manifest.yaml` | modified | +27/-4 | PW-I16/I17 |
| `.gitea/workflows/ci.yaml` | modified | +15/-1 | generated |
| `Makefile` | modified | +9/-3 | generated |
| `tests/test_playwright_bootstrap.py` | modified | +3/-2 | test fix |

### Semantic Summary

**PW-I13 — Authenticated Smoke (5 scenarios)**
- SSO button redirects to Keycloak realm
- Login with valid credentials lands on service
- Logout terminates session and redirects to login
- Post-logout reload stays unauthenticated
- Callback failure (wrong credentials) shows error

**PW-I14 — Library/Playback Page Objects + Spec (4 scenarios)**
- `LibraryPage`: `goto()`, `cardCount()`, `openBookByTitle(title)`
- `PlayerPage`: `isPlaying()`, `play()`, `pause()`
- Library page shows book cards after login
- Known title opens and displays book detail
- Play button starts playback
- Pause button stops playback

**PW-I15 — Authorization (8 scenarios)**
- Denied user cannot log in
- Denied user sees login page after failed attempt
- User can log in and reach library
- User cannot see admin section
- Admin can log in and reach library
- Admin can see admin section
- Empty credentials stay on login page
- Invalid username shows error on Keycloak

**PW-I16 — CI Gates**
- `npm run test:service` script targeting `services/` directory
- Runner `service` mode without base URL (no prereq checks)
- CI manifest: enable `playwright-platform` and `playwright-service` steps
- Manifest generator: service_name dynamic per suite

**PW-I17 — Post-Deployment**
- `tests/playwright/ci/post-deploy.sh` wrapper script
- `post-deploy` stage in ci-manifest.yaml (main branch only)
- `docs/playwright-ci-runbook.md` — runbook with all stages, runner modes, test counts

### Breaking Changes
None. The `test:platform` now uses explicit directory arguments instead of `testDir: "."` — functionally equivalent since the directory arguments match the previous test file locations.

### Version/Release Impact
None. No service images or deployment artifacts are modified.
