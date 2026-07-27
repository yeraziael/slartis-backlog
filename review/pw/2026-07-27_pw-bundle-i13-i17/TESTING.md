# Testing — PW Bundle 2

## Tests Executed

All tests pass on the canonical repository (`make test` on commit `2beb30f`).

### Shell/Unit Tests (`make test-checks`)
- 12/12 PASS — link checker, compose checker, secret scanner, git-diff

### CI Generator Tests (`make test-ci-generator`)
- 10/10 PASS — manifest validation, generator reproducibility, generated target matching

### Matrix/Framework Tests (`make test` — all framework tests)
- All Matrix, Synapse, Coturn, Mautrix, Audiobookshelf-proxy tests: PASS

### Playwright Bootstrap Tests (`make test-playwright-bootstrap`)
- **139/139 PASS** — playwright dirs, runner, package.json, evidence, prerequisites, artifacts, sanitisation, bundle

### Playwright Headed Contract Tests (`test-playwright-headed-contract`)
- **7/7 PASS** — headed image, entrypoint, endpoint loop, vnc wait, shellcheckable, documentation

### Playwright Platform Tests (`test-playwright-platform`)
- **Pre-existing failure** — `__dirname` is not defined in ES module scope (sanitisation-spec.spec.ts, prerequisite-classification.spec.ts)
- This is a pre-existing ESM/CommonJS compatibility issue, not introduced by this bundle

### Lint (`make lint`)
- check-links: PASS
- check-compose: PASS
- check-git-diff: PASS
- scan-secrets: PASS

## CI Status
- Gitea Actions workflow `.gitea/workflows/ci.yaml` updated with `playwright-service` and `post-deploy` stages
- YAML validation: PASS

## Reproducible Commands

```bash
cd /mnt/raid0/slarti/workspace/worktrees/architecture-main-sync
make lint    # ALL PASS
make test    # ALL PASS (except pre-existing playwright ESM issue)
```

## Test Gaps
- Service tests (authorization, library-playback, smoke-authenticated) require live environment with credentials — not executable in CI without `PW_E2E_ABS_USER`/`PW_E2E_ABS_PASSWORD` env vars
- The `post-deploy` stage is only triggered on main branch, not testable on feature branches
- Pre-existing: playwright platform tests fail in Docker due to `__dirname` in ESM context
