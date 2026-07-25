# Changelog

## v0.2.1-draft

- **Breaking:** `activation` is now a required top-level field; `activation.version` is required
- **Breaking:** `action_ref` version suffix is now mandatory (was optional with `[:version]` pattern)
- Added immutable identity model: `(trigger_id, activation.version)` is the normative identity pair
- Changed `trigger_id` registration semantics from update-on-reregister to version-aware rejection of conflicting content
- Added `SCHEMAS/test_schemas.py` — schema-level test harness
- Added 3 new invalid scenarios: missing activation, missing activation.version, conflicting (trigger_id, version) content
- Updated CI workflow to run schema tests

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

## v0.1.0-draft

- Initial repository setup
- Added `FINDINGS/` directory with Pilot 57 findings and reusable template
- Added `DECISIONS/` directory for architectural decision records
- Updated repository structure documentation in `README.md`
