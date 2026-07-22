# Playwright — CI/CD

## CI Pipeline

The Playwright platform CI runs as part of the `Homelab/Architecture` repository's shared CI pipeline (Gitea Actions). There is no separate CI for the Playwright epic plan (this directory).

### Execution Strategy

| Aspect | Specification |
|---|---|
| Invocation | Gitea Actions workflow step calling `docker run` with the pinned Playwright image |
| Trigger | Post-deployment, or on changes to tests/playwright/ in Homelab/Architecture |
| Runner | rechenknecht (Gitea Actions runner) — Pi5 is not suitable for browser tests |
| Parallelism | Services tested in parallel where possible; suites within a service run sequentially |
| Pre-check | Prerequisite check before test execution (see `testing.md` §Prerequisite Classification) |

### CI Workflow Integration

```yaml
"on":
  push:
    paths:
      - 'tests/playwright/**'
      - 'pi/compose/**'
  workflow_dispatch: {}

jobs:
  playwright:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Playwright smoke suite
        run: |
          docker run --rm \
            -e SERVICE_URL=https://audiobookshelf.hl.maier.wtf \
            -e KEYCLOAK_URL=https://keycloak.hl.maier.wtf \
            -e TEST_USERNAME=${{ secrets.PW_ABS_USER }} \
            -e TEST_PASSWORD=${{ secrets.PW_ABS_PASS }} \
            -e SUITE=smoke \
            -v $PWD/test-results:/results \
            mcr.microsoft.com/playwright:v1.52.0@sha256:<digest> \
            npx playwright test --config=playwright.config.ts

      - name: Upload evidence
        uses: actions/upload-artifact@v3
        with:
          name: playwright-evidence
          path: test-results/
```

**Note:** The above is a template. Actual CI configuration will be versioned in `Homelab/Architecture`.

### Job Structure

| Job | Scope | Expected |
|---|---|---|
| `playwright-smoke` | Smoke suite for changed or target service | PASS or prerequisite_error |
| `playwright-regression` | Full regression suite (on release branches) | PASS |
| `playwright-e2e` | E2E acceptance suite (on release branches) | PASS |
| `evidence-validate` | Validate evidence bundle integrity | PASS |

## Artifact Retention

| Artifact Type | Retention | Rationale |
|---|---|---|
| Evidence bundles (pass) | 7 days | Available for review, then cleaned up |
| Evidence bundles (fail) | 30 days | Extended retention for failure investigation |
| Screenshots (fail) | 30 days | Part of evidence bundle |
| Traces (fail) | 30 days | Part of evidence bundle |
| CI logs | Gitea Actions default | Transient infrastructure diagnostics |

## Gating

### Pre-Merge Gate (Homelab/Architecture)

Changes to `tests/playwright/` in `Homelab/Architecture`:

| Gate | Required | Failure Action |
|---|---|---|
| Platform self-tests | YES | Block merge |
| Smoke suite for affected service | YES | Block merge |
| Regression suite | For release branches | Block merge |
| Evidence validation | YES | Block merge |
| Secret scan | YES (repo-wide) | Block merge |
| Link check | YES (repo-wide) | Block merge |
| Git diff check | YES (repo-wide) | Block merge |

### Post-Deployment Gate (Homelab/Architecture)

After a service deployment:

| Gate | Required | Failure Action |
|---|---|---|
| Smoke suite | YES | Rollback deployment candidate |
| Evidence manifest valid | YES | Investigate test infrastructure |
| Prerequisite check all pass | YES | Investigate infrastructure before product |

### Merge Policy

- A passing Playwright suite MUST NOT override failing lower-layer tests (unit, API, integration, infrastructure).
- A prerequisite_error MUST NOT block a release — it indicates an infrastructure issue, not a product regression.
- A test failure in the smoke suite after deployment SHOULD trigger a rollback or investigation.

## Retry Policy

| Failure Type | Retry Count | Retry Condition |
|---|---|---|
| Prerequisite error (infrastructure) | 2, with 60s delay | Only if known transient (DNS, container restart) |
| Test failure (assertion) | 0 | Failure is real — must be investigated |
| Runner error (container crash) | 1 | Infrastructure issue, retry once |
| Timeout | 1 | May be transient load; retry once |

Retries MUST be configurable and SHOULD be documented in the CI configuration. Excessive retries mask real problems.

## Prerequisite Handling

The CI pipeline MUST run prerequisite checks before the test suite:

1. **DNS resolution** — service FQDN resolves.
2. **TLS certificate** — valid, not expired.
3. **Service healthcheck** — service responds with 200.
4. **Keycloak reachable** — OIDC discovery or login page accessible.
5. **Test identity exists** — synthetic account can authenticate.

If any prerequisite fails, the job reports `prerequisite_error` and exits with code 2. No test suite is executed.

## CI Gotchas

From Homelab operational knowledge (`AGENTS.md`):

- Gitea Actions YAML: `on:` is parsed as boolean `true` in YAML 1.1 → must use `"on":`.
- `actions/checkout@v4` must be the first step in each job.
- Runner image is `debian:bookworm-slim` — Node.js and Playwright deps need `apt-get install` or use of a prebuilt Playwright container.
- `actions/upload-artifact@v4` is rejected with `GHESNotSupportedError` → use `@v3`.
- Validate workflow locally: `python3 -c "import yaml; yaml.safe_load(open('.gitea/workflows/ci.yaml'))"`.
- Playwright browser binaries need system dependencies: `libnss3`, `libatk-bridge2.0-0`, etc. Using the official Playwright container image avoids this.
