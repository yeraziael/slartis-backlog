# Testing

```bash
python3 tests/test_playwright_bootstrap.py
python3 tests/playwright/evidence/bundle/bundle-self-test.py
git diff --check origin/main...HEAD
```

- 139/139 bootstrap checks pass locally.
- 139/139 checks pass in a Debian bookworm-slim Python 3 container.
- Bundle self-test passes, including symlinked input rejection.
- Gitea Actions run #791 is green for canonical PR #95 head `7f9c725`.

The updated Playwright spec could not run locally: this host has Node 18 while
the pinned Playwright suite requires Node 24. The Gitea browser platform job
is currently disabled; this remains a documented test gap.
