# Changelog

## v0.3.0-draft

- Added `SPEC/review-provenance.md` — Review Provenance specification with 3 review types, commit binding, and supersession
- Added `SCHEMAS/review-verdict.json` — v2 review verdict schema with `review_type`/`verdict` cross-validation
- Added `EXAMPLES/review-verdict-valid.json` — 4 valid verdict scenarios (independent approved, independent changes, self-verification, post-merge)
- Added `EXAMPLES/review-verdict-invalid.json` — 7 invalid verdict scenarios (type mismatches, missing fields, invalid formats)
- Added `DECISIONS/002-review-provenance.md` — ADR-002 for this change
- Updated `SCHEMAS/test_schemas.py` — added review-verdict schema to test suite
- Updated `README.md` — referenced review-provenance spec
- Updated `DECISIONS/README.md` — added ADR-002 to register

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
