# Summary — ACP v0.2: Execution Contract and Trigger Contract

## Problem

The Agent Coordination Protocol (ACP) defined Slarti, Lydia, and Eddie roles but lacked formal contracts for:

- How Slarti hands off executable work to Lydia (Execution Contract)
- How Eddie triggers registered, versioned actions (Trigger Contract)

In practice, missing preconditions, ambiguous parameters, and unregistered actions caused repeated failures documented in `slarti/backlog` learnings.

## Goal

Formalise two contracts:

1. **Execution Contract** — deterministic, non-interpretive handoff from Slarti to Lydia
2. **Trigger Contract** — registered, versioned action dispatch from Eddie to Lydia

## Scope

- 15 new/changed files (13 original + 2 corrective: test_schemas.py, ci.yaml)
- 2 new SPEC documents (execution-contract.md, trigger-contract.md)
- 2 JSON Schemas (draft-07) corrected per review findings 1-6
- 4 example files (valid + invalid per contract) updated
- 1 test harness (SCHEMAS/test_schemas.py) added
- 1 ADR (DECISIONS/001-execution-trigger-contracts.md)
- VERSION bump 0.1.0-draft → 0.2.1-draft

## Not in Scope

- Eddie runtime implementation
- Migration of existing Lydia tasks
- Deployment of any new infrastructure
- Changes to Vekling orchestration policy

## Affected Components

- `Homelab/ACP` — canonical repository
- `SPEC/` — contract specifications
- `SCHEMAS/` — JSON Schema validators
- `EXAMPLES/` — contract examples
- `DECISIONS/` — architecture decision record

## Canonical References

- **Repository:** Homelab/ACP (Gitea)
- **PR:** #6 — ACP v0.2: Execution Contract and Trigger Contract
- **Issue:** yeraziael/Slartis-backlog#88
