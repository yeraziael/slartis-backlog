# Testing - ACP Release-State Audit

## Local Validation

| Check | Result |
|---|---|
| PyYAML safe-load of `.gitea/workflows/ci.yaml` | PASS |
| `python3 SCHEMAS/test_schemas.py` | PASS |
| CI secret-scanner pipeline | PASS |
| `git diff --check` | PASS |

## Canonical CI Evidence

The original main run 686 failed in `schema-tests`. On the reviewed PR head,
the replacement runs 689 and 690 completed successfully after the dependency
and placeholder-scanner fixes.

## Review-Bundle Validation

The bundle validator is run from `yeraziael/ai-governance` against this exact
bundle. Its result is recorded in the GitHub review PR.
