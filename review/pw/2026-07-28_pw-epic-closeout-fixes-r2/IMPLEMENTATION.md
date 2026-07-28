# IMPLEMENTATION - Playwright Epic Closeout Fixes

## Changed Files

| File | Change |
|---|---|
| `.gitea/workflows/ci.yaml` | Generated separate service jobs, explicit non-root runner identity, operations test, and evidence uploads. |
| `Makefile` | Generated registration for the operations test target. |
| `ci-generate.py` | Generates the expanded Playwright job and secret contracts. |
| `ci-manifest.yaml` | Source-of-truth definitions for operations and service-specific post-deployment jobs. |
| `docs/decisions/playwright/jellyfin-onboarding.md` | Records the actual undeployed runtime state and operator dependency. |
| `docs/playwright-ci-runbook.md` | Documents secret names, split jobs, evidence, and fail-closed behavior. |
| `docs/playwright-operations.md` | Clarifies runtime gate ownership and closeout requirements. |
| `tests/playwright/ci/post-deploy.sh` | Validates service-specific credentials and zero-failure, zero-skip evidence. |
| `tests/playwright/evidence/artifacts/artifact-self-test.spec.ts` | Resolves the local fixture relative to the test module. |
| `tests/playwright/evidence/result-summary.py` | Extracts final Playwright outcome totals from JSON reports. |
| `tests/playwright/package.json` | Adds service-specific suite commands. |
| `tests/playwright/platform/self-test.spec.ts` | Removes the fixed `/workspace` fixture path. |
| `tests/playwright/playwright.config.ts` | Writes the Playwright JSON report to the evidence output path. |
| `tests/playwright/runner/run.sh` | Implements CI mount discovery, non-root execution, isolated volumes, copy-back, cleanup, failure propagation, and manifest totals. |
| `tests/playwright/services/audiobookshelf/pages/authorization.ts` | Aligns authorization navigation with the current application behavior. |
| `tests/playwright/services/audiobookshelf/pages/login.ts` | Supports the direct-Keycloak login redirect. |
| `tests/playwright/services/audiobookshelf/smoke-authenticated.spec.ts` | Uses the revised login and controlled-data contracts. |
| `tests/playwright/services/audiobookshelf/smoke-unauthenticated.spec.ts` | Uses the revised unauthenticated navigation contract. |
| `tests/test_checks.sh` | Isolates git-diff fixtures from inherited CI repository state. |
| `tests/test_ci_generator.py` | Verifies generated operations and post-deployment contracts. |
| `tests/test_playwright_bootstrap.py` | Adds regressions for root-hosted CI, mount isolation, permissions, dependency failures, copy-back, counts, and path independence. |

No files are deleted.

## Semantic Changes

- CI no longer treats one generic service suite as evidence for two services.
- Production service jobs cannot pass through credential-based skips.
- Nested Docker no longer binds a path that exists only inside the job container.
- Dependency infrastructure failures stop execution instead of being discarded by `|| true`.
- Evidence totals now reflect the final Playwright outcomes rather than a constant zero-count envelope.
- Local fixture navigation follows module locations and works under any repository root.

## Breaking And Migration Impact

There is no application API or persisted-data migration. Operators must provision the documented Gitea Actions secret names before main-branch post-deployment jobs can pass. This is intentional fail-closed behavior, not a compatibility fallback.

## Release Impact

The change is CI, test-runner, and documentation scope and is merged as `11921fb0572222e5d3ccf7652ef1b466c704bc0f`. Deployment remains a separate operator action tracked by `slarti/backlog#283`; duplicate runner remediation is tracked by `slarti/backlog#284`.
