# TESTING - Playwright Epic Closeout Fixes Post-Merge Audit

## Exact Review Span

- Base: `6ee0b7821ed51b77b89ae679520123bc763e2654`.
- Head: merge commit `11921fb0572222e5d3ccf7652ef1b466c704bc0f`.
- Canonical PR: `Homelab/Architecture#109`, squash-merged by `eddie-policy`.
- Tree equivalence: the merge diff has the same 21 files, 834 insertions, 145 deletions, and changeset SHA-256 as reviewed PR head `efac29fd9abfa9578c8f88bfd27937eb3c05a856`.

## Local Validation

| Command | Result |
|---|---|
| `make ci` | PASS. Full generated lint and test contract completed. |
| `python3 tests/test_playwright_bootstrap.py` | PASS, 144/144. |
| `python3 tests/test_ci_generator.py` | PASS. |
| `python3 tests/test_playwright_operations.py` | PASS, 2/2. |
| `bash tests/test_checks.sh` | PASS, 12/12. |
| `shellcheck tests/playwright/runner/run.sh tests/playwright/ci/post-deploy.sh tests/test_checks.sh` | PASS. |
| `git diff --check` | PASS. |
| `bash tests/playwright/runner/run.sh platform` | PASS, 39/39; generated manifest schema-valid. |

The platform suite was rerun after the final module-relative fixture change and remained 39/39 green.

## Pre-Merge Gitea CI

Gitea Actions Run #906 is bound to exact head `efac29fd9abfa9578c8f88bfd27937eb3c05a856` and completed with conclusion `success`.

| Job ID | Job | Result |
|---|---|---|
| #3279 | Linting & Validation | SUCCESS |
| #3280 | Unit Tests | SUCCESS, including Playwright platform and operations steps |
| #3281 | Reporting | SUCCESS |
| #3282 | Post-Deployment Audiobookshelf | SKIPPED as expected on the feature-branch push |
| #3283 | Post-Deployment Jellyfin | SKIPPED as expected on the feature-branch push |

The skipped service jobs are not production evidence. Their main-branch execution requires operator-provisioned secrets and reachable services.

## Post-Merge Gitea CI

Main Run #908 is bound to merge commit `11921fb0572222e5d3ccf7652ef1b466c704bc0f` and completed with failure. A same-SHA rerun reproduced the Unit Tests failure.

| Job ID | Runner | Job | Result |
|---|---|---|---|
| #3289 | not material | Linting & Validation | SUCCESS |
| #3290 | ID 3, `rechenknecht` | Unit Tests | FAILURE twice; results initializer exits before repository code with `exec /bin/bash: exec format error` |
| #3291 | not material | Reporting | SUCCESS |
| #3292 | service gate | Post-Deployment Audiobookshelf | FAILURE; operator credentials/evidence inputs absent |
| #3293 | service gate | Post-Deployment Jellyfin | FAILURE; target and operator credentials/evidence inputs absent |

Successful PR Unit Tests job #3280 used runner ID 4. Failing main Unit Tests job #3290 used runner ID 3. Both advertise name `rechenknecht` and label `ubuntu-latest`; the active local runner container is registration ID 4. Duplicate runner remediation is tracked separately by `slarti/backlog#284`.

## Diagnostic Regression Evidence

Earlier exact-head runs exposed distinct Gitea-only failures and informed the committed regressions:

| Run | Observed failure | Resulting correction |
|---|---|---|
| #894/#895 | Job-container checkout path used as a host bind source. | Discover and reuse the job checkout mount. |
| #896 | Nested `node_modules` target absent below a read-only checkout. | Prepare the target and propagate dependency failures. |
| #898 | Broad job-volume inheritance caused OCI execution failure. | Import only the checkout mount. |
| #900 | Non-root browser could not write the root-owned results volume. | Add isolated results initialization. |
| #902 | Results initialization attached to the dependency phase produced repeatable OCI failure. | Separate one-volume initialization from dependency execution. |
| #904 | Four tests assumed `file:///workspace/tests/playwright`. | Resolve local fixtures relative to each module. |
| #906 | Final exact-head run. | SUCCESS. |
| #908 | Merge-SHA run and rerun selected duplicate runner ID 3. | Unit Tests fail before repository code; operator runner gate #284 opened. |

## Service Runtime Observations

- Audiobookshelf was reachable in a live no-credential probe: 11 tests passed and 11 credential-gated tests skipped. This verifies gating behavior but does not satisfy the zero-skip production contract.
- Jellyfin was not reachable at the proposed hostname; TLS returned an unrecognized-name failure.
- The Architecture repository had no Gitea Actions secrets for these service suites during this review.

## Known Test Gaps

- No authenticated Audiobookshelf production evidence exists at the reviewed SHA.
- No Jellyfin service execution exists because the target and identities are not provisioned.
- No main-branch post-deployment artifact exists at the reviewed SHA.
- No green main-branch Unit Tests job exists at the merge SHA because duplicate runner ID 3 fails before repository code.
- Service gaps are tracked by `slarti/backlog#283`; runner remediation is tracked by `slarti/backlog#284`. Both prevent full runtime closeout.
