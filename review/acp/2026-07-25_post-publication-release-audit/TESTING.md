# Testing - ACP Post-Publication Release Audit

## Test-First Evidence

The first fixture run failed with `FileNotFoundError` for the intentionally
missing `CONFORMANCE/release_audit.py`. Implementation followed that fixed
contract.

## Local Validation

| Check | Result |
|---|---|
| `python3 CONFORMANCE/test_release_audit.py` | PASS, 13/13 |
| `python3 SCHEMAS/test_schemas.py` | PASS |
| PyYAML safe-load of both Gitea workflows | PASS |
| Repository no-secret scanner | PASS |
| `git diff --check` | PASS |
| Authenticated adapter against current ACP inventory | PASS, 0 findings |

## Canonical Gitea CI

| Run | Commit | Event | Result | Relevant evidence |
|---|---|---|---|---|
| 693 | `386c0e8f1398020fb6306b17b5cd27a463eb615c` | pull_request | success | Schema, structure, 13 release fixtures, no-secret gate |
| 697 | `9a713a5d4ce5f3993da779dc2e6b6cdc669361c3` | pull_request | success | Corrective secret-name diff |
| 701 | `1e1a4c34ab59794bf6a5ed45e5db026a2b80cca3` | pull_request | success | Credential-shaped placeholder correction |
| 703 | `38baaf19568766e3911f63edd1509c8997030eab` | workflow_dispatch | success | Credential preflight and real post-publication adapter |

Run 703 used the provisioned `read:repository` Actions secret. The current ACP
inventory contains no stable tag, so zero release-audit findings is expected.

## Review-Bundle Validation

The bundle is validated with the canonical
`yeraziael/ai-governance/tools/validate_review_bundle.py` against this exact
directory before the GitHub review PR is created.
