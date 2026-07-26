# Architecture: PW-I13 Audiobookshelf Authenticated Smoke

## Current State

The Playwright test platform (PW-I01–I08) provides:
- Infrastructure: `tests/playwright/services/service.ts` (service factory)
- Config: `tests/playwright/playwright.config.ts` (multi-browser, env-driven)
- Helpers: `tests/playwright/helpers/env.ts`, `tests/playwright/helpers/logger.ts`
- ADR: `docs/decisions/playwright/adr-001-playwright-testing-strategy.md`

No service-level page objects existed before PW-I13. The Audiobookshelf service
domain had no test coverage.

## New Components

### `tests/playwright/services/audiobookshelf/pages/oidc.page.ts`

Page object encapsulating the Keycloak OIDC login/logout flow:
- `navigateToLogin()` — loads the ABS root, which redirects to the login page
- `clickKeycloakLogin()` — finds and clicks the Keycloak SSO button
- `fillKeycloakCredentials(user, pass)` — fills the Keycloak login form
- `waitForCallback()` — waits for the `/auth/openid/callback` redirect
- `performRpInitiatedLogout()` — clicks logout link and waits for session termination

### `tests/playwright/services/audiobookshelf/pages/library.page.ts`

Page object for the Audiobookshelf library view:
- `waitForLoad()` — waits for the `[role="main"]` element
- `hasLibraryList()` — checks for library list presence
- `isLoginPage()` — detects if the page is a login/auth redirect
- `getCurrentHref()` — returns the current URL
- `hasNoMediaItems()` — confirms no media items are rendered (post-logout check)

### `tests/playwright/services/audiobookshelf/smoke-authenticated.spec.ts`

Four-scenario smoke test covering the authenticated lifecycle:
1. Login success → library landing (no `/login` in URL)
2. Callback failure → stays on login page
3. Logout → session terminated, redirect to login/logout
4. Post-logout reload → remains unauthenticated

## Data Flow

```
spec → OidcPage → Keycloak (auth.hl.maier.wtf)
     → LibraryPage (audiobookshelf.hl.maier.wtf)
     → OidcPage.performRpInitiatedLogout()
     → Keycloak logout endpoint
```

## Interfaces

- **Environment variables:** `PW_E2E_ABS_USER`, `PW_E2E_ABS_PASSWORD` (provisioned by PW-I09)
- **URLs:** `audiobookshelf.hl.maier.wtf`, `auth.hl.maier.wtf/realms/homelab/...`
- **Config:** `tests/playwright/playwright.config.ts` base URL and credentials

## Impact

No existing components are modified. This is purely additive — new service
layer files under `tests/playwright/services/audiobookshelf/`.
