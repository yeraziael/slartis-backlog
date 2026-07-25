# Testing — ACP v0.2 Review Fix

## Schema Validation Test Suite

All tests pass: `python3 SCHEMAS/test_schemas.py`

| Test | Result |
|------|--------|
| trigger-contract.json is valid Draft-07 | PASS |
| trigger-contract-valid.json passes schema | PASS |
| Invalid: Unregistered action_ref (runtime) | PASS |
| Invalid: Missing schedule for cron (schema catches) | PASS |
| Invalid: Bad cron expression (passes schema, runtime) | PASS |
| Invalid: _violation field (schema catches) | PASS |
| Invalid: Unversioned action_ref (schema rejection) | PASS |
| execution-contract.json is valid Draft-07 | PASS |
| execution-contract-valid.json passes schema | PASS |
| Invalid: Missing required fields (schema rejection) | PASS |
| Invalid: Unknown action (runtime) | PASS |
| Invalid: Version mismatch (runtime) | PASS |
| Invalid: Missing parameters (schema catches) | PASS |
| Invalid: Path outside allowed_paths (runtime) | PASS |

## CI Integration

New `schema-test` step in `.gitea/workflows/ci.yaml`:
```yaml
- name: schema-test
  run: python3 SCHEMAS/test_schemas.py
```

## Verification

```bash
# From repo root:
python3 SCHEMAS/test_schemas.py
```
