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

## Current Runtime Evidence — Run #978 (SHA fd797dbbe191c5ed81d34628886d9bedd96ccb4c)

### Source

This evidence was gathered after `slarti/backlog#283` prerequisites were provisioned by the operator (Jellyfin deployment, synthetic identities, Gitea Actions secrets). The Architecture repository's merged mainline evolved past the original #283 target SHA `11921fb...`. Operator approved SHA `fd797db...` as the current source for #283 closeout evidence. It does not descend from `11921fb...`; it is the operator-approved current source after subsequent #283-related changes.

### Run #978 — Main Branch Push (success)

| Field | Value |
|---|---|
| Run ID | 978 |
| Event | push |
| Branch | main |
| SHA | `fd797dbbe191c5ed81d34628886d9bedd96ccb4c` |
| Title | `fix(playwright): align Jellyfin runtime smoke (#130)` |
| Conclusion | success |
| Trigger actor | eddie-policy |
| Started | 2026-07-29T10:32:16+02:00 |
| Completed | 2026-07-29T10:37:57+02:00 |

### Jobs

All 5 jobs on runner ID 4 (`rechenknecht`):

| Job ID | Name | Status | Conclusion |
|---|---|---|---|
| #3631 | Linting & Validation | completed | success |
| #3632 | Unit Tests | completed | success |
| #3633 | Reporting | completed | success |
| #3634 | Post-Deployment Audiobookshelf | completed | success |
| #3635 | Post-Deployment Jellyfin | completed | success |

### Post-Deployment Job Steps

**Job #3634 — Post-Deployment Audiobookshelf**:
| Step | Status | Conclusion |
|---|---|---|
| Run actions/checkout@v4 | completed | success |
| setup | completed | success |
| smoke-audiobookshelf | completed | success |
| Run actions/upload-artifact@v3 | completed | success |

**Job #3635 — Post-Deployment Jellyfin**:
| Step | Status | Conclusion |
|---|---|---|
| Run actions/checkout@v4 | completed | success |
| setup | completed | success |
| smoke-jellyfin | completed | success |
| Run actions/upload-artifact@v3 | completed | success |

### CI Configuration (fail-closed contract)

Per `ci-manifest.yaml` and generated `.gitea/workflows/ci.yaml` at SHA `fd797db`:

1. **Post-deploy.sh** (PW-I17): Validates all required credential environment variables are set before executing the Playwright runner. If any credential is unset → exit 2 → job failure.
2. **run.sh** (PW-I01/I03/I04): Maps Playwright exit codes through `map-result.sh` — any test failure (exit code != 0) propagates to job failure. Evidence manifest is generated and schema-validated before upload.
3. **Evidence sanitisation** (PW-I07): Runtime credential values are appended to the sanitisation pattern file before scanning. If unsafe evidence is detected, all evidence is removed, a forced error manifest is generated, and the job exits with error.
4. **Upload step**: `actions/upload-artifact@v3` with `if-no-files-found: error` — if the evidence directory does not exist or was removed by sanitisation, the upload step fails the job.
5. **Quality gate**: `exit_zero` — the entire step process must exit with code 0.

The Gitea Actions `conclusion=success` on both post-deployment jobs therefore implies:
- All required credential secrets were provisioned and correctly named.
- Playwright service tests executed (smoke steps not skipped).
- No Playwright test failures (exit code 0).
- Schema-valid manifest generated.
- Evidence sanitisation passed (no credential patterns found).
- Artifact upload completed successfully.

### Artifact Verification

**Evidence artifact names** (per CI manifest):
- `playwright-audiobookshelf-evidence`
- `playwright-jellyfin-evidence`

Gitea 1.26.4 artifact REST API (`/api/v1/repos/Homelab/Architecture/actions/artifacts?run_id=978`) returns `{"artifacts": [], "total_count": 0}`. This is a known Gitea 1.26.4 behaviour where the REST list endpoint may return empty despite successful uploads and populated `action_artifact` database records.

Independent verification of the `action_artifact` database table (run_id=978, commit_sha=`fd797db...`, artifact names `playwright-audiobookshelf-evidence` and `playwright-jellyfin-evidence`, status=uploaded) is not possible through the public API on this instance. The storage chunk integrity check (path under Gitea data directory `actions/artifacts/`) requires filesystem access to the Gitea server host which is outside the available credential-safe scope.

### Manifest Contents (0 failed / 0 skipped)

The manifest.json is inside the uploaded artifact. Without artifact content inspection the exact `tests.failed` and `tests.skipped` values from the schema-validated manifest cannot be read directly.

**Confidence analysis**:
- **Zero failed**: HIGH — Playwright exits non-zero on any test failure. The job's `conclusion=success` and the step-level `conclusion=success` on `smoke-audiobookshelf` and `smoke-jellyfin` confirm the Playwright exit code was 0.
- **Zero skipped**: UNKNOWN — Playwright exits 0 with skipped tests. The CI does not independently enforce `skipped == 0` in the job runner; it relies on the manifest.json contents which are inside the unverifiable artifact.

**Conclusion**: The `0 failed / 0 skipped` manifest DoD item (item 3) **cannot be fully established** without artifact content inspection. All other DoD items are verified.
