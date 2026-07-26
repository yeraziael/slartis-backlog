# Risks: PW-I13 Audiobookshelf Authenticated Smoke

## Architecture

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Page objects tightly coupled to ABS DOM structure | Medium | Low | Selectors use ARIA roles and `data-testid` where possible; easy to update |
| `OidcPage` hardcodes Keycloak URLs | Low | Low | URLs match current Keycloak realm config; change if realm changes |

## Security

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Credentials passed via `process.env` | Low | Low | Standard Playwright pattern; env vars not logged by default |
| Empty credentials on unset env vars | Medium | Medium | Tests fail with empty string fill — visible in output, no silent pass |

## Operations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Tests require live Keycloak + ABS | High | Medium | Not registered in CI yet; run manually or in integration environment |
| Keycloak rate-limiting on failed logins | Low | Low | Only one callback failure test; no brute-force pattern |

## Migration

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| None | — | — | Purely additive |

## Compatibility

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Playwright version mismatch | Low | Low | `package.json` pins Playwright version |
| ABS DOM changes break selectors | Medium | Medium | Page object pattern isolates selector updates |

## Maintainability

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Duplicate credential setup across specs | High | Low | Deferred to PW-I11 shared OIDC fixture |
| Hardcoded ABS_BASE in spec | Low | Low | Could move to page object constructor or config |

## Rollback

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| None | — | — | Delete 3 files; no existing code affected |
