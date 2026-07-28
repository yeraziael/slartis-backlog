# Audiobookshelf — CI/CD

## CI Pipeline

The Audiobookshelf CI runs as part of the `Homelab/Architecture` repository's shared CI pipeline (Gitea Actions). There is no separate Audiobookshelf-specific CI.

### Pipeline Definition

- **Repository:** `Homelab/Architecture` (Gitea)
- **CI System:** Gitea Actions
- **Runner:** rechenknecht (v0.6.1)
- **Trigger:** Push to any branch, PR to `main`
- **Manifest:** `ci-manifest.yaml` (single source of truth)
- **Generator:** `ci-generate.py` produces Makefile + workflow + pre-commit + config

### CI Jobs

| Job | Scope | Tools | Expected |
|---|---|---|---|
| `lint` | All files | `check-links`, `scan-secrets`, `git diff --check` | PASS |
| `test-unit` | Compose validation, contract tests | `docker compose config`, shell test scripts | PASS |
| `report` | Aggregate results | CI framework | PASS |

### Compose Validation (part of test-unit)

Runs against every Compose file in `pi/compose/`:

```bash
docker compose -f pi/compose/audiobookshelf.yml config
```

Expected: Exit 0, valid YAML.

### Audiobookshelf Proxy Tests (part of test-unit)

```bash
bash pi/tests/test_audiobookshelf_proxy.sh
```

Expected: 27 assertions, all PASS.

See `docs/review/gh59-audiobookshelf-proxy-tls/TESTING.md` for detailed test output.

### Secret Scan

```bash
# Part of lint job
scan-secrets
```

Expected: PASS. The scanner checks for:
- Common credential patterns
- Private keys
- API tokens
- Connection strings with embedded secrets

### Link Check

```bash
# Part of lint job
check-links
```

Expected: PASS. Validates all internal and external links in documentation.

### Git Diff Check

```bash
# Part of lint job
git diff --check
```

Expected: PASS. Rejects trailing whitespace, merge conflict markers, etc.

## CI Configuration Files

| File | Location | Purpose |
|---|---|---|
| CI manifest | `ci-manifest.yaml` | Single source of truth |
| CI workflow | `.gitea/workflows/ci.yaml` | Gitea Actions workflow |
| Makefile | `Makefile` | Local development targets |
| Pre-commit config | `.pre-commit-config.yaml` | Pre-commit hooks |

## Current CI Status

| Check | Status | Evidence |
|---|---|---|
| Compose valid | PASS | Verified in GH-58, GH-59 |
| Proxy contract tests (27 assertions) | PASS | Run #613 (GH-59) |
| No host ports | PASS | Compose validation |
| Secret scan | PASS | GH-58, GH-59 review packages |
| Link check | PASS | GH-58, GH-59 review packages |
| Git diff check | PASS | GH-58, GH-59 review packages |

## Planned CI Additions

The following CI checks are planned but not yet implemented:

| Check | Trigger | Status |
|---|---|---|
| OIDC config validation | On changes to OIDC scripts | Planned (part of GH-60) |
| NFS mount test (syntax) | On changes to mount scripts | Planned (part of NFS issue) |
| Backup script test (dry-run) | On changes to backup scripts | Planned (part of GH-62) |
| Restore script test (dry-run) | On changes to restore scripts | Planned (part of GH-62) |

## Deployment Pipeline

Deployment is NOT automated in CI. Deployment follows the Homelab convention:

1. PR merged in `Homelab/Architecture` (by Eddie).
2. Lydia pulls latest `main` on Pi5.
3. Lydia runs `docker compose up -d` with updated Compose file.
4. Lydia verifies container health.

## Local CI Execution

Developers can run the same checks locally:

```bash
# Full CI suite
make lint
make test

# Individual checks
docker compose -f pi/compose/audiobookshelf.yml config
bash pi/tests/test_audiobookshelf_proxy.sh
git diff --check
scan-secrets
check-links
```

## CI Gotchas

From `AGENTS.md` (Homelab operational knowledge):

- Gitea Actions YAML: `on:` is parsed as boolean `true` in YAML 1.1 → must use `"on":`.
- `actions/checkout@v4` must be the first step in each job.
- Runner image is `debian:bookworm-slim` — tools like `shellcheck`, `shfmt` need `apt-get install`.
- Labels are in `.runner` config, not overridable by env vars.
- `actions/upload-artifact@v4` rejected with `GHESNotSupportedError` → use `@v3`.
- Validate workflow locally: `python3 -c "import yaml; yaml.safe_load(open('.gitea/workflows/ci.yaml'))"`.
