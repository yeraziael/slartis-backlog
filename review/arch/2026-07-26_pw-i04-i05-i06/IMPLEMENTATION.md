## Files Changed

| File | Change | Notes |
|------|--------|-------|
| `tests/playwright/evidence/manifest.schema.json` | new | JSON Schema v1 |
| `tests/playwright/evidence/manifest-generate.py` | new | Typed generator |
| `tests/playwright/evidence/manifest-validate.sh` | new | Shell validator |
| `tests/playwright/prerequisites/check-dns.sh` | new | DNS resolution check |
| `tests/playwright/prerequisites/check-http.sh` | new | HTTP status check |
| `tests/playwright/prerequisites/check-tls.sh` | new | TLS cert check |
| `tests/playwright/prerequisites/check-keycloak.sh` | new | OIDC discovery check |
| `tests/playwright/prerequisites/check-all.sh` | new | Orchestrator |
| `tests/playwright/prerequisites/fixtures/pass-all.env` | new | Deterministic fixture |
| `tests/playwright/platform/prerequisite-classification.spec.ts` | new | Playwright self-tests |
| `tests/playwright/evidence/artifacts/artifact-self-test.spec.ts` | new | Artifact self-tests |
| `tests/playwright/playwright.config.ts` | modified | Capture settings |
| `tests/playwright/runner/run.sh` | modified | Manifest + prereq integration |
| `tests/playwright/evidence/artifacts/verify-artifacts.sh` | new → modified | Post-run harness; trace hard-fail (PR #90); structural ZIP validation via `unzip -t` / `python3 zipfile.testzip()` (PR #91) |
| `tests/test_playwright_bootstrap.py` | modified | +325 lines, 118 tests total |

## Semantic Summary

- **Manifest generation:** Every run (including forced outcomes) produces a
  validated `manifest.json` bound to exact SHA commits and runtime container
  IDs.
- **Prerequisite classification:** Four composable check types with an
  orchestrator supporting fixture (deterministic) and service (real) modes.
- **Failure-only capture:** Playwright screenshot/trace configured to fire on
  failure only; self-tests assert correct artifact presence/absence.
- **Post-run verification harness:** `verify-artifacts.sh` runs @pass/@fail
  suites on clean directories, validates PNG screenshot (89 50 4E 47 header)
  and ZIP trace (50 4B 03 04 header) — both mandatory on failure.
- **No breaking changes:** Existing PW-I01 through PW-I03 behaviour preserved.
