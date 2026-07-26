# PW-I13: Audiobookshelf Authenticated Login and Logout Smoke

## Problem Statement

The Playwright test platform needs to prove that synthetic users can authenticate via Keycloak OIDC, land on the Audiobookshelf library, and terminate their sessions via RP-initiated logout. Without these tests, there is no automated evidence that the OIDC integration works end-to-end in the browser.

## Goal

Implement a deterministic Playwright harness covering login success, callback failure, logout, and post-logout unauthenticated reload for the `pw-e2e-abs-user` synthetic identity.

## Scope

- `tests/playwright/services/audiobookshelf/pages/oidc.page.ts` — OIDC page object
- `tests/playwright/services/audiobookshelf/pages/library.page.ts` — Library page object
- `tests/playwright/services/audiobookshelf/smoke-authenticated.spec.ts` — Smoke test spec

## Not in Scope

- Playback, admin role, denied role, group mutation, break-glass, or account provisioning
- Shared OIDC fixture implementation (deferred to PW-I11)
- Unauthenticated smoke flow (deferred to PW-I12)

## Affected Components

- `tests/playwright/services/audiobookshelf/` — new service layer for Audiobookshelf page objects

## Canonical References

- **PR:** Homelab/Architecture#103
- **Issue:** slarti/backlog#272
- **Parent Epic:** slarti/backlog#253