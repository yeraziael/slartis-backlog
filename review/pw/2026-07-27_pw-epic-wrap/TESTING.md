# TESTING — Epic #253 Closeout Verification

## Classification of Test Evidence
Testing for Epic #253 comprises two categories:

### A. Infrastructure/Unit Test Suites (Python)
Validates the CI pipeline, manifest generation, operations policy, and bootstrap integrity. These run on every PR and merge.

| Test Suite | Command | Source SHA | CI Merge-Job Reference | Verdict |
|---|---|---|---|---|
| Bootstrap Tests | `python3 tests/test_playwright_bootstrap.py` | `6ee0b7821ed51b77b89ae679520123bc763e2654` | Gitea PR #107 merge CI (Run #870, `Architecture CI / Linting & Validation`) | 139/139 PASS |
| CI Generator Tests | `python3 tests/test_ci_generator.py` | `6ee0b7821ed51b77b89ae679520123bc763e2654` | Gitea PR #107 merge CI (Run #870, `Architecture CI / Unit Tests`) | PASS |
| Operations Policy Tests | `python3 tests/test_playwright_operations.py` | `6ee0b7821ed51b77b89ae679520123bc763e2654` | Gitea PR #107 merge CI (Run #870, `Architecture CI / Reporting`) | PASS |

### B. Playwright Browser/E2E Test Suites
Validates browser-based service journeys against Audiobookshelf and Jellyfin. These execute in ephemeral Playwright containers within Gitea Actions CI. Each PR merge below confirms the associated browser tests passed at merge time.

| Scope | Gitea PR | Merge Commit SHA | Browser Tests Executed | PR-CI Verdict |
|---|---|---|---|---|
| Audiobookshelf onboarding + OIDC fixture + unauthenticated smoke | #105 | `80c1a496c7b2fcd358d63f75da8526ab143f74e8` | PW-I10, PW-I11, PW-I12 | GREEN (all Playwright spec suites) |
| Audiobookshelf auth smoke + library/playback + authorization + CI gates + post-deployment | #106 | `e74c58b2edb583819b091f4cf158e817e35fe99e` | PW-I13, PW-I14, PW-I15, PW-I16, PW-I17 | GREEN (all Playwright spec suites) |
| Jellyfin unauthenticated smoke + auth/roles + media playback + operations runbook | #107 | `6ee0b7821ed51b77b89ae679520123bc763e2654` | PW-I18, PW-I19, PW-I20, PW-I21 | GREEN (all Playwright spec suites + operations tests) |

Each PR's CI job output is anchored to its merge commit SHA, providing an immutable provenance trail from the merge commit to the Gitea Actions run log. The CI manifest (`ci-manifest.yaml`) and generated workflow (`.gitea/workflows/ci.yaml`) define which Playwright specs execute at each gate.

## Immutable References
- **Repository**: Homelab/Architecture, branch `main`
- **Final HEAD**: `6ee0b7821ed51b77b89ae679520123bc763e2654`
- **Infrastructure CI**: Gitea Actions Run #870 (Jobs: `Linting & Validation` #3126, `Unit Tests` #3127, `Reporting` #3128)
- **Browser/Playwright CI**: Verified at each PR merge commit (PRs #105, #106, #107)
