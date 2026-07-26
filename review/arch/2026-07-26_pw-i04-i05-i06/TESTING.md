## Static Bootstrap Tests

```bash
python3 tests/test_playwright_bootstrap.py
```

All 114 pass. Test categories:

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
| Failure-only artifacts (PW-I06) | 7 |

## Playwright Self-Tests

| Test | Expected |
|------|----------|
| `prerequisite-classification.spec.ts` | DNS localhost resolves, HTTP fixture fails, check-all exits 2 on missing args |
| `artifact-self-test.spec.ts` | @pass produces no artifacts, @fail captures screenshot+trace |

## CI Status

- All Gitea Actions runs green for PR #86 (I04) and PR #87 (I05)
- PR #88 (I06) awaiting CI trigger after merge

## Known Gaps

- Real Docker platform test (`make test-playwright-platform`) requires
  non-root Docker on rechenknecht — documented limitation
- No production FQDN checks in CI (intentionally deferred to service suites)
