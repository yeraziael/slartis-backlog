# Changelog

## v0.2.0-draft

- Added `SPEC/execution-contract.md` — Execution Contract specification
- Added `SPEC/trigger-contract.md` — Trigger Contract specification
- Added `SCHEMAS/execution-contract.json` — JSON Schema for Execution Contracts
- Added `SCHEMAS/trigger-contract.json` — JSON Schema for Trigger Contracts
- Added `EXAMPLES/execution-contract-valid.json` — valid Execution Contract example
- Added `EXAMPLES/execution-contract-invalid.json` — 5 invalid Execution Contract examples
- Added `EXAMPLES/trigger-contract-valid.json` — valid Trigger Contract example
- Added `EXAMPLES/trigger-contract-invalid.json` — 4 invalid Trigger Contract examples
- Added `DECISIONS/001-execution-trigger-contracts.md` — ADR-001 for this change

## v0.2.1-draft

- **Breaking:** `action_ref` version suffix is now mandatory (was optional)
- **Breaking:** `constraints`, `rollback`, `success_criteria` are now required top-level fields in Execution Contract
- **Breaking:** `webhook.secret` renamed to `webhook.secret_ref` with normative resolution requirement
- Added immutable identity model: `(trigger_id, activation.version)` is the immutable identity pair
- Added conditional required sub-fields for `schedule`: cron type requires `cron`, schedule type requires `interval_seconds`
- Added `SCHEMAS/test_schemas.py` — schema-level test harness with 12+ validation scenarios
- Updated CI workflow to run schema tests
- Added schema-level violation examples for unversioned action_ref and missing required fields

## v0.1.0-draft

- Initial repository setup
- Added `FINDINGS/` directory with Pilot 57 findings and reusable template
- Added `DECISIONS/` directory for architectural decision records
- Updated repository structure documentation in `README.md`
