# Implementation: PW-I13 Audiobookshelf Authenticated Smoke

## Files Changed

| File | Status | Lines |
|------|--------|-------|
| `tests/playwright/services/audiobookshelf/pages/oidc.page.ts` | **new** | +65 |
| `tests/playwright/services/audiobookshelf/pages/library.page.ts` | **new** | +40 |
| `tests/playwright/services/audiobookshelf/smoke-authenticated.spec.ts` | **new** | +116 |

**Total:** 3 files, +221 insertions, 0 deletions.

## Semantic Summary

Three TypeScript files implementing the first Playwright service-level tests
for Audiobookshelf. Two page objects (`OidcPage`, `LibraryPage`) encapsulate
page-specific selectors and interactions. One spec file (`smoke-authenticated`)
drives five test scenarios covering login success, invalid credentials,
logout, post-logout reload, and post-logout protected-route revisit.

## Breaking Changes

None. All files are new; no existing code is modified.

## Migration Requirements

None. Tests run via `node node_modules/@playwright/test/cli.js test` using existing config.

## Version Impact

This is the first service-level test for Audiobookshelf. It establishes the
page object pattern that PW-I12, PW-I14, PW-I15, PW-I16, PW-I17 will follow.

## Design Decisions

1. **Page objects over inline selectors** — each page gets its own class,
   keeping selectors isolated and reusable across specs.
2. **`requireCredentials()` gate** — throws a clear error when
   `PW_E2E_ABS_USER` / `PW_E2E_ABS_PASSWORD` are absent. No silent pass,
   no empty-string credential fill.
3. **`waitForAbsLanding()` glob** — uses `**` glob pattern instead of exact
   callback URL, avoiding race conditions with OIDC query params and
   intermediate redirects.
4. **`performRpInitiatedLogout()` throws on missing** — throws when no logout
   link is found, preventing silent no-op logout paths from hiding broken flows.
5. **Session invalidation proof** — fifth test revisits ABS after logout and
   asserts re-authentication is required, proving the session was actually
   terminated.
6. **Invalid credentials test** — submits wrong credentials to Keycloak,
   asserts error indicator or continued presence on Keycloak login page.
