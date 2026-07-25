# Implementation — ACP v0.2 Contracts

## File Manifest

| File | Status | Lines | Description |
|------|--------|-------|-------------|
| `VERSION` | modified | 1/1 | 0.1.0-draft → 0.2.0-draft |
| `CHANGELOG.md` | modified | +12 | Added v0.2.0-draft entries |
| `README.md` | modified | +4/-3 | Updated scope and structure |
| `DECISIONS/README.md` | modified | +1/-1 | Updated decision index |
| `SPEC/execution-contract.md` | added | +258 | Execution Contract specification |
| `SPEC/trigger-contract.md` | added | +329 | Trigger Contract specification |
| `SCHEMAS/execution-contract.json` | added | +137 | JSON Schema (draft-07) |
| `SCHEMAS/trigger-contract.json` | added | +158 | JSON Schema (draft-07) |
| `EXAMPLES/execution-contract-valid.json` | added | +69 | Valid ollama.prompt example |
| `EXAMPLES/execution-contract-invalid.json` | added | +119 | 5 invalid scenarios |
| `EXAMPLES/trigger-contract-valid.json` | added | +50 | Valid Paperless backup trigger |
| `EXAMPLES/trigger-contract-invalid.json` | added | +80 | 4 invalid scenarios |
| `DECISIONS/001-execution-trigger-contracts.md` | added | +99 | ADR-001 |

## Semantic Summary

- **Execution Contract:** Defines 7-state lifecycle, normative principles (executor interprets nothing, structured rejection), all 14+ fields with types and descriptions, and alignment mapping to existing Lydia mechanisms
- **Trigger Contract:** Defines 6 trigger types with type-specific schedule metadata, 5-state lifecycle, Retry/Backoff/Deduplication rules, sequence diagram (Slarti → Eddie → Lydia → Result), and alignment mapping
- **Schemas:** Full JSON Schema (draft-07) with conditional `required` for trigger types, enum-based action/status validation
- **Examples:** 4 files with valid and intentionally broken contracts

## Breaking Changes

- None. ACP v0.2 is additive to v0.1.0-draft. Existing mechanisms remain compatible.

## Migration

- Existing Lydia tasks and Eddie cron jobs are not migrated by this PR. The alignment mapping documents how each existing mechanism maps to the new contracts.

## Version/Release Impact

- VERSION: 0.1.0-draft → 0.2.0-draft
- No release tag created
