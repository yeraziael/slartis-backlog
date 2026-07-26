# TODO: PW-I13 Audiobookshelf Authenticated Smoke

## Open Items

- [ ] **Playwright config integration:** `playwright.config.ts` needs a `projects` entry for `services/audiobookshelf` with service-specific base URL and credentials
- [ ] **CI registration:** Smoke specs need to run in CI after keycloak/ABS are provisioned (blocked on PW-D05 infra)
- [ ] **Shared OIDC fixture:** `OidcPage` credential setup is duplicated in each test; PW-I11 will extract a shared `playwright/services/audiobookshelf/fixtures/oidc.fixture.ts`

## Follow-up Issues

- PW-I12: Unauthenticated smoke flow (complement to PW-I13)
- PW-I14: Denied role smoke
- PW-I15: Admin role smoke
- PW-I16: Authenticated playback
- PW-I17: Group mutation smoke

## Technical Debt

- `ABS_BASE` and `ABS_LOGIN` are hardcoded in the spec file; should be centralized in config or fixture
- `OidcPage` constructor hardcodes ABS and Keycloak URLs; could accept a config object
- `.catch(() => {})` on `waitForURL` swallows timeout errors; consider explicit assertion instead

## Known Limitations

- Tests cannot run without a live Keycloak and Audiobookshelf instance
- No test isolation for logout state — tests must run sequentially or each perform a full login cycle
- Empty credentials on unset env vars produce a fill-then-submit failure rather than a clear skip

## Decisions Required

- Should page objects accept a config/URL object instead of hardcoding URLs?
- Should the spec use `test.describe.configure({ mode: 'serial' })` to enforce execution order?

## Deferred Items

- All items above are deferred to subsequent PW-I* issues
