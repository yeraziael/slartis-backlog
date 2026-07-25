# Testing — ACP v0.2 Contracts

## Validators Executed

| Validation | Tool | Status |
|-----------|------|--------|
| JSON Schema validation (valid examples) | `jsonschema` CLI | pass |
| JSON Schema validation (invalid examples) | `jsonschema` CLI | pass (all rejected as expected) |
| Governance referential integrity | `validate_governance.py` | pass (0 errors) |
| Model policy consistency | `tools/model_policy.py` | pass |
| No-secrets scan | `test_no_secrets.py` | pass |
| Review bundle validation | `tools/validate_review_bundle.py` | pass (exit 0) |

## Reproducible Commands

```bash
# Validate JSON Schemas against examples
jsonschema -i EXAMPLES/execution-contract-valid.json SCHEMAS/execution-contract.json
jsonschema -i EXAMPLES/execution-contract-invalid.json SCHEMAS/execution-contract.json  # expected to fail
jsonschema -i EXAMPLES/trigger-contract-valid.json SCHEMAS/trigger-contract.json
jsonschema -i EXAMPLES/trigger-contract-invalid.json SCHEMAS/trigger-contract.json  # expected to fail

# Governance validation
make test
make validate
```

## Results

- All 4 JSON Schema validations produced expected results
- Full ai-governance test suite: 210 tests, all passed
- Governance validator: 0 errors (pre-existing warnings only)

## CI Status

- Gitea Actions on Homelab/ACP: merged (post-merge review; no CI run captured for this PR HEAD)
- GitHub actions on yeraziael/ai-governance: N/A (this is a review bundle, not a governance change)

## Known Test Gaps

- No runtime end-to-end test (bundle is a post-merge review of already-merged changes)
- No blackbox test (requires Michael to execute; deferred to ACP adoption phase)
