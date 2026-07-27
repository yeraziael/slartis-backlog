# PW-I09/I10/I11/D05/I12: Playwright Shared Fixtures, OIDC, Onboarding, Unauthenticated Smoke

## Problem Statement

The Playwright test platform needs shared fixtures (service targets, role selection, console capture, OIDC auth) and the first Audiobookshelf service-level tests before authenticated smoke and regression coverage can proceed.

## Goal

Implement the foundational shared fixtures and first unauthenticated Audiobookshelf smoke tests, establishing the page object pattern and fixture architecture for all subsequent service suites.

## Scope

- PW-I09: Synthetic identity provisioning script + 30 mock tests + credential loader + contract doc
- PW-I10: Service target, role selection, console-error capture fixtures + 10 self-tests
- PW-I11: Shared Keycloak OIDC auth fixture + fake harness + 7 self-tests
- PW-D05: Audiobookshelf browser onboarding contract (selectors, journeys)
- PW-I12: Audiobookshelf unauthenticated smoke — HTTPS, render, SSO button (5 live tests)

## Not in Scope

- Authenticated login/logout (PW-I13)
- Library, playback, roles, admin (PW-I14–I17)
- Jellyfin (PW-I19–I21)
- CI integration (PW-I16)

## Affected Components

- `tests/playwright/fixtures/` — shared fixture library
- `tests/playwright/platform/` — fixture self-tests
- `tests/playwright/services/audiobookshelf/` — first service suite
- `pi/audiobookshelf/scripts/` — identity provisioning
- `docs/` — contracts and decisions

## Canonical References

- **PR:** Homelab/Architecture#105
- **Issues:** slarti/backlog#267, #268, #269, #270, #271
- **Parent Epic:** slarti/backlog#253
