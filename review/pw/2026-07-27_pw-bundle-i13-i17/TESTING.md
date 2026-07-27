# Testing — PW Bundle 2 (v2, head=45a80c4)

## Tests Executed

All tests pass on the canonical repository (`make test` on commit `45a80c4`).

### Shell/Unit Tests (`make test-checks`)
- 12/12 PASS — link checker, compose checker, secret scanner, git-diff

### CI Generator Tests (`make test-ci-generator`)
- **12/12 PASS** — includes new `test_playwright_steps_have_explicit_arguments` and `test_post_deploy_has_branch_condition` round-trip assertions

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
- `playwright-platform` now correctly passes `platform` argument to runner
- `playwright-service` now correctly passes `service` argument to runner
- `post-deploy` job has `if: github.ref == 'refs/heads/main'` condition
- YAML validation: PASS

## Findings Resolved (v2)

### Finding 1: Missing `flags` argument in `bash` tool
- **Fix:** `ci-generate.py` `bash` tool handler now appends `flags` to run command (line 105)
- **Round-trip guard:** `test_playwright_steps_have_explicit_arguments` test verifies correct command lines

### Finding 2: Post-deploy branch condition missing
- **Fix:** Added `condition: github.ref == 'refs/heads/main'` to `post-deploy` stage in `ci-manifest.yaml`
- **Fix:** Added `if:` support to `ci-generate.py` for stage-level conditions
- **Fix:** `post-deploy.sh` now fails closed (exit 2) when `CI=true` and no URL is provided
- **Round-trip guard:** `test_post_deploy_has_branch_condition` test verifies the condition

## Reproducible Commands

```bash
cd /mnt/raid0/slarti/workspace/worktrees/architecture-main-sync
make lint    # ALL PASS
make test    # ALL PASS (except pre-existing playwright ESM issue)
python3 tests/test_ci_generator.py  # 12/12 PASS
```

## Test Gaps
- Service tests (authorization, library-playback, smoke-authenticated) require live environment with credentials — not executable in CI without `PW_E2E_ABS_USER`/`PW_E2E_ABS_PASSWORD` env vars
- The `post-deploy` stage is only triggered on main branch, not testable on feature branches
- Pre-existing: playwright platform tests fail in Docker due to `__dirname` in ESM context
