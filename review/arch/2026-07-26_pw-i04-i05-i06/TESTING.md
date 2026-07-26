## Static Bootstrap Tests

```bash
python3 tests/test_playwright_bootstrap.py
```

All 117 pass. Test categories:

| Category | Count |
|----------|-------|
| File existence & structure | ~15 |
| package.json contract | 3 |
| Playwright config contract | 1 |
| Bootstrap spec | 1 |
| Lockfile validator | 2 |
| Runner script structure | 11 |
| Docker argument contract (fake docker) | 8 |
| Platform self-tests | 8 |
| Result semantics (PW-I03) | 4 |
| map-result.sh unit (PW-I03) | 16 |
| run.sh subcommand (PW-I03) | 5 |
| Evidence manifest (PW-I04) | 15 |
| Prerequisite checks (PW-I05) | 18 |
| Failure-only artifacts (PW-I06) | 9 |

## Playwright Self-Tests

| Test | Expected |
|------|----------|
| `prerequisite-classification.spec.ts` | DNS localhost resolves, HTTP fixture fails, check-all exits 2 on missing args |
| `artifact-self-test.spec.ts` | @pass test succeeds (green), @fail test fails intentionally, @prerequisite_error test detects missing env |
| `verify-artifacts.sh` (post-run harness) | Runs @pass + @fail suites on clean result dirs; pass → no artifacts; fail → PNG screenshot + ZIP trace required; missing trace is hard failure |

## Post-Run Artifact Harness

```bash
./tests/playwright/evidence/artifacts/verify-artifacts.sh
```

The harness:
1. Creates a clean temp directory
2. Runs the @pass suite — asserts zero artifacts produced
3. Runs the @fail suite — asserts the test failed (non-zero exit)
4. Checks for screenshot PNGs (valid 89 50 4E 47 header)
5. Checks for trace ZIPs (valid 50 4B 03 04 header)
6. Exits 0 only when all checks pass; both screenshot and trace are mandatory

## CI Status

- All Gitea Actions runs green for PR #86 (I04), PR #87 (I05), PR #88 (I06),
  PR #89 (I06-fix: artifact harness), PR #90 (I06-fix: trace hard failure),
  and PR #91 (I06-fix: structural ZIP integrity)
- All six PRs merged into main (b1b34b8)

## Known Gaps

- Real Docker platform test (`make test-playwright-platform`) requires
  non-root Docker on rechenknecht — documented limitation
- No production FQDN checks in CI (intentionally deferred to service suites)
- `verify-artifacts.sh` runs in temp directories with no real browser —
  validates artifact contract, not browser rendering
