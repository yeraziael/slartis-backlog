# Implementation — ACP v0.2 Review Fix

## Changes per Finding

### Finding 1 — Conditional schedule sub-fields
- Split the combined `cron/schedule` allOf in `trigger-contract.json` into two separate `if/then` branches
- Cron trigger type now requires `schedule.cron`
- Schedule trigger type now requires `schedule.interval_seconds`

### Finding 2 — webhook.secret → secret_ref
- Renamed field in `trigger-contract.json` schema
- Added pattern validation `^[A-Za-z0-9._/-]+$`
- Updated normative description with resolution requirement

### Finding 3 — Immutable identity
- Added new normative principle to `trigger-contract.md`
- Explicit: `(trigger_id, activation.version)` is the immutable identity pair

### Finding 4 — Mandatory action_ref version
- Schema pattern changed from `:semver?` (optional) to `:semver` (required)
- Spec description updated: "optional version suffix" → "mandatory version suffix"

### Finding 5 — Required execution contract fields
- Added `constraints`, `rollback`, `success_criteria` to required array in schema
- Spec descriptions updated to explain why these are mandatory
- Every contract must declare explicit boundaries and failure strategy

### Finding 6 — Test harness
- New file: `SCHEMAS/test_schemas.py`
- Validates schema syntax (Draft-07 conformance)
- Validates all 4 example files pass/fail as expected
- 14 scenarios: 2 schema validation, 4 valid examples, 8 invalid scenarios
- Integrated into CI pipeline as `schema-test` step
