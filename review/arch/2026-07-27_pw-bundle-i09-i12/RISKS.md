# Risks: PW-I09/I10/I11/D05/I12 Bundle

## Architecture

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Fake OIDC harness diverges from real Keycloak | Low | Low | Harness tests structure, not protocol; live tests validate real flow |
| Fixtures too generic for service needs | Low | Low | Fixtures compose with service page objects; no forced abstraction |

## Security

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Credentials in test output | Low | Low | `innerText()` assertion proves passwords not visible; no page.content() check against hardcoded values |

## Operations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Provisioning script requires kcadm | High | Low | Mock mode for CI; commit mode only in operator runtime |

## Migration

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| None | — | — | Purely additive |

## Rollback

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| None | — | — | Delete 13 files; no existing code affected |
