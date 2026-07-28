# Review Summary: Playwright Plan-as-Code — Bundle 2 (PW-I13–I17)

## Problem Statement
The Architecture repository needs browser-based integration tests for Audiobookshelf (authenticated smoke, library/playback, authorization) and corresponding CI gates to execute them on every push and after deployment.

## Goal
Deliver the second Playwright bundle covering 5 issues in a single PR:
- **PW-I13:** Authenticated smoke tests (SSO redirect, valid login, logout, post-logout reload, callback failure)
- **PW-I14:** Library and player page objects with playback scenarios
- **PW-I15:** Authorization tests (denied/user/admin/malformed auth)
- **PW-I16:** CI gates for playwright platform + service tests
- **PW-I17:** Post-deployment smoke wrapper and runbook

## Scope
- 3 new spec files, 3 new page objects, 1 CI wrapper, 1 runbook
- CI manifest update with `playwright-service` step and `post-deploy` stage
- Runner update for `service` mode (no base URL — npm run test:service)
- Npm `test:service` script targeting `services/` directory
- Test count update: 53 total (31 provisioning + 10 shared fixtures + 7 OIDC + 5 smoke)

## Not in Scope
- PW-I06 (evidence schema evolution), PW-I07 (CI reports) — deferred to future bundles
- PW-ACP-CP1 (#261) — skipped per operator
- Playwright headed/VNC platform tests — pre-existing `__dirname` ESM issue

## Affected Components
- `tests/playwright/` — new spec files, page objects, CI wrapper
- `ci-manifest.yaml` + `ci-generate.py` — CI pipeline definition
- `tests/test_playwright_bootstrap.py` — updated package.json script assertion
- `docs/playwright-ci-runbook.md` — new runbook

## Canonical References
- **Repository:** Homelab/Architecture
- **PR:** #106
- **Base commit:** `80c1a496c7b2fcd358d63f75da8526ab143f74e8`
- **Head commit:** `2beb30f1aa7626e2f07cdcf10be415dd80adf63a`
- **Issues:** #272 (PW-I13), #273 (PW-I14), #274 (PW-I15), #275 (PW-I16), #276 (PW-I17)
