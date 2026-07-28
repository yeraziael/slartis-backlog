# TESTING — Epic #253 Partial Closeout Evidence

## Classification of Test Evidence
Testing for Epic #253 comprises two categories:

### A. Infrastructure/Unit Test Suites (Python/Bash)
Validates the CI pipeline, manifest generation, operations policy, and bootstrap integrity. These run on every PR and merge.

| Test Suite | Command | Source SHA | CI Run & Step | Verdict |
|---|---|---|---|---|
| Bootstrap Tests | `python3 tests/test_playwright_bootstrap.py` | `5b944908a5c6d3b2be5f2904005374f7d6d4fbd8` | Gitea Actions Run #870 / `Unit Tests` / `playwright-bootstrap` | PASS (139/139) |
| CI Generator Tests | `python3 tests/test_ci_generator.py` | `5b944908a5c6d3b2be5f2904005374f7d6d4fbd8` | Gitea Actions Run #870 / `Unit Tests` / `ci-generator` | PASS |
| Operations Policy Tests | `python3 tests/test_playwright_operations.py` | No successful exact-SHA CI binding identified | Not an explicit step in the cited workflow | NOT VERIFIED BY THIS PACKAGE |

### B. Playwright Browser/E2E Test Suites
Validates browser-based service journeys. The records below distinguish PR-head CI from merge-commit CI and report the observed results without inferring success from merge state.

#### PR Bundle #105 — Audiobookshelf onboarding + OIDC + unauthenticated smoke
- **Gitea PR**: #105, feature branch `feat/pw-bundle-i09-i12`
- **PR Head SHA**: `b12884a039aa79007d124ae1e0c04682df35de9a`
- **Merge Commit**: `80c1a496c7b2fcd358d63f75da8526ab143f74e8`
- **CI Run**: #846 (head SHA `b12884a`)
- **Result**: ALL GREEN — all 3 jobs (Linting & Validation, Unit Tests, Reporting) passed with all steps SUCCESS.
- **Playwright steps within Unit Tests**:
  - `playwright-platform`: SUCCESS
  - `playwright-service`: SUCCESS
  - `playwright-bootstrap`: SUCCESS
  - `playwright-headed-contract`: SUCCESS

#### PR Bundle #106 — Audiobookshelf auth + library/playback + authorization + CI + post-deployment
- **Gitea PR**: #106, feature branch `feat/pw-bundle-i13-i17`
- **PR Head SHA**: `5b944908a5c6d3b2be5f2904005374f7d6d4fbd8`
- **Merge Commit**: `e74c58b2edb583819b091f4cf158e817e35fe99e`
- **CI Runs**: #869 (feature-branch context), #870 (pull-request context), both at head SHA `5b944908a5c6d3b2be5f2904005374f7d6d4fbd8`
- **Result**: Unit Tests: FAILURE — all infrastructure and Python steps PASSED, but step `playwright-platform` FAILED (known `@fail` intentional-failure fixtures being resolved by this PR). `playwright-service` SKIPPED due to earlier failure.
- **Verified passing steps**:
  - `playwright-bootstrap`: PASS
  - `playwright-headed-contract`: PASS
  - All infrastructure/Python test steps: PASS (check-scripts, ci-generator, matrix-*, audiobookshelf-proxy)
- **Known gap**: `playwright-platform` and `playwright-service` are not fully green for this bundle. Code review does not replace runtime verification; PW-I13–PW-I17 remain verification-incomplete.

#### PR Bundle #107 — Jellyfin unauthenticated smoke + auth/roles + playback + operations
- **Gitea PR**: #107, feature branch `feat/pw-bundle-i18-i21`
- **PR Head SHA**: `a7b0eb79afa74c03379fd997092305e94f0fa55b`
- **Merge Commit**: `6ee0b7821ed51b77b89ae679520123bc763e2654`
- **CI Runs**: #888 (feature-branch context), #889 (pull-request context), both at head SHA `a7b0eb79afa74c03379fd997092305e94f0fa55b`
- **Result**: Unit Tests: FAILURE — `check-scripts` step FAILED (infrastructure test script issue, not a Playwright test). Playwright steps were SKIPPED because failure occurred before the Playwright stage.
- **Verified passing**: Linting & Validation (all steps), Reporting
- **Known gap**: Playwright tests for Jellyfin (PW-I19, PW-I20, PW-I21) did not execute in these runs. Code review does not replace runtime verification; these tickets remain verification-incomplete.

### C. PR-CI Evidence Summary
| Bundle PR | Merge Commit SHA | CI Run ID | Linting | Unit Tests Status | Playwright Platform | Playwright Service | Reporting |
|---|---|---|---|---|---|---|---|
| #105 | `80c1a49...` | #846 | PASS | PASS | PASS | PASS | PASS |
| #106 | `e74c58b...` | #869/#870 | PASS | FAIL | FAIL (known @fail) | SKIPPED | PASS |
| #107 | `6ee0b78...` | #888/#889 | PASS | FAIL (infra) | SKIPPED | SKIPPED | PASS |

### D. Production Gate — INCOMPLETE
The final merged head `6ee0b7821ed51b77b89ae679520123bc763e2654` has these relevant runs:

| Run | Context | Linting | Unit Tests | Reporting | Post-Deployment Smoke |
|---|---|---|---|---|---|
| #890 | `main` | FAIL | FAIL | PASS | FAIL |
| #892 | pull-request context | PASS | FAIL (`check-scripts`) | PASS | SKIPPED |

**Note**: The `Post-Deployment Smoke` job runs only on `refs/heads/main` (workflow condition `github.ref == 'refs/heads/main'`). Main-branch Run #871 at merge commit `e74c58b2edb583819b091f4cf158e817e35fe99e` and main-branch Run #890 at final head `6ee0b7821ed51b77b89ae679520123bc763e2654` both recorded this job as FAIL.

These results do not establish an operational production gate. Full closeout requires later exact-SHA evidence with `playwright-platform`, `playwright-service`, and `Post-Deployment Smoke` all successful.

## Immutable References
- **Repository**: Homelab/Architecture, branch `main`
- **Final HEAD**: `6ee0b7821ed51b77b89ae679520123bc763e2654`
- **Gitea Actions runs by bundle**: PR #105 → Run #846, PR #106 → Runs #869/#870 and main Run #871, PR #107 → Runs #888/#889 and final-head main Run #890
