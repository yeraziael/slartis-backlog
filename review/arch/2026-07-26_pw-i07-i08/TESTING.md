# Testing

## Local

```bash
python3 tests/test_playwright_bootstrap.py
python3 tests/playwright/evidence/bundle/bundle-self-test.py
git diff --check origin/main...HEAD
```

- 137/137 bootstrap checks pass.
- Bundle self-test validates golden pass, fail, and prerequisite-error
  bundles; deterministic inventory output; missing-JUnit rejection; and
  forbidden-input rejection.
- A Debian bookworm-slim Python 3 run also completed 137/137 checks.

## CI

- PW-I07 final PR head `5ba23c7` received green Gitea Actions after the
  no-`unzip` Python fallback correction.
- PW-I08 PR head `372953b` received green Gitea Actions run #785.
- Both canonical PRs are merged; this bundle reviews Architecture main
  `3362689b63a8e557b8f1a8ac160fed066677ec32`.

## Known Gap

The real Docker platform suite remains disabled in CI. Its controlled runtime
execution requires non-root Docker on rechenknecht.
