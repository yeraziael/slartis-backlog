# Implementation: PW-I13 Audiobookshelf Authenticated Smoke

## Files Changed

| File | Status | Lines |
|------|--------|-------|
| `tests/playwright/services/audiobookshelf/pages/oidc.page.ts` | **new** | +49 |
| `tests/playwright/services/audiobookshelf/pages/library.page.ts` | **new** | +40 |
| `tests/playwright/services/audiobookshelf/smoke-authenticated.spec.ts` | **new** | +87 |

**Total:** 3 files, +176 insertions, 0 deletions.

## Semantic Summary

Three TypeScript files implementing the first Playwright service-level tests
for Audiobookshelf. Two page objects (`OidcPage`, `LibraryPage`) encapsulate
page-specific selectors and interactions. One spec file (`smoke-authenticated`)
drives four test scenarios covering login, callback failure, logout, and
post-logout session verification.

## Breaking Changes

None. All files are new; no existing code is modified.

## Migration Requirements

None. Tests run via `npx playwright test` using existing config.

## Version Impact

This is the first service-level test for Audiobookshelf. It establishes the
page object pattern that PW-I12, PW-I14, PW-I15, PW-I16, PW-I17 will follow.

## Design Decisions

1. **Page objects over inline selectors** — each page gets its own class,
   keeping selectors isolated and reusable across specs.
2. **`process.env` for credentials** — reads `PW_E2E_ABS_USER` /
   `PW_E2E_ABS_PASSWORD` at test time. Falls back to empty string if unset,
   which causes the test to fail gracefully (filling empty credentials).
3. **Soft URL assertions** — uses `toContain` / `includes` rather than exact
   match, since ABS may redirect through multiple intermediate URLs.
4. **Catch-and-continue on waitForURL** — `.catch(() => {})` prevents timeout
   failures when the page doesn't redirect as expected; the subsequent
   assertion catches the actual state.
