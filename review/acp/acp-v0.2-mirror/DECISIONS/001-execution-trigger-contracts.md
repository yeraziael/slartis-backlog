# ADR-001: Execution and Trigger Contracts for ACP v0.2

**Status:** Proposed
**Date:** 2026-07-25

## Context

Issue `yeraziael/slartis-backlog#88` identified that the existing ACP (`v0.1.0-draft`)
lacked formal contracts for two critical interactions:

1. **Execution Contract** between Slarti (Principal) and Lydia (Executor) —
   what must be provided for deterministic, non-interpretive execution.
2. **Trigger Contract** between Slarti, Eddie (Orchestrator), and Lydia —
   how Eddie triggers registered actions without containing execution logic.

Pilot 57 (`FINDINGS/PILOT-57.md`) produced four ACP-level findings (F-57-001
through F-57-003, F-57-006) that directly demand normative content. The SPEC/
directory was empty at v0.1.0-draft.

The analysis of `lydia/home-repo` showed multiple implicit contracts:
- `envelope.schema.json` (message envelope)
- `worker_schema.json` (ephemeral worker contract)
- `task_contract.sh` (task state machine, `lydia-task/v1`)
- Eddie's executor registration (`name`, `endpoint`, `capabilities`, `concurrency`)

These are implementation-specific. ACP must define transport-agnostic,
provider-independent contracts that can be realised by any executor.

## Decision

Add two normative specifications to ACP v0.2.1-draft:

1. **Execution Contract** (`SPEC/execution-contract.md`):
   - Defines what a Principal must provide for a single deterministic action.
   - 7 lifecycle states: SUBMITTED → VALIDATED → APPROVED/REJECTED → EXECUTING → COMPLETED/FAILED
   - Required fields: `acp_version`, `execution_id`, `action`, `version`,
     `provenance`, `parameters`, `evidence`
   - Optional but defined: `preconditions`, `security`, `constraints`,
     `rollback`, `success_criteria`, `failure_handling`
   - Normative principles: Executor interprets nothing, rejects incomplete
     contracts, Principal responsible for tool availability.

2. **Trigger Contract** (`SPEC/trigger-contract.md`):
   - Defines how a Principal registers a trigger with Orchestrator (Eddie).
   - 5 lifecycle states: REGISTERED → VALIDATED → ACTIVE/REJECTED → DISABLED/EXPIRED
   - 6 trigger types: `schedule`, `cron`, `event`, `webhook`, `manual`, `condition`
   - Required fields: `acp_version`, `trigger_id`, `action_ref`, `provenance`,
     `trigger_type`, `parameters`
   - Includes: retry policy, deduplication, concurrency, deadline, notifications, activation
   - Normative principles: Eddie triggers only registered actions, contains no
     execution logic, trigger changes require new version.

3. **JSON Schemas** (`SCHEMAS/execution-contract.json`, `SCHEMAS/trigger-contract.json`):
   - Draft-07 JSON Schema for machine validation of both contracts.

4. **Examples** (`EXAMPLES/`):
   - 1 valid + 5 invalid examples for Execution Contract
   - 1 valid + 4 invalid examples for Trigger Contract

## Consequences

**Easier:**
- Slarti can formally specify what Lydia must execute, with structured rejection
  on missing or invalid fields.
- Eddie can validate trigger registrations against executor capabilities before
  activation.
- New executors (Vekling workers, external services) can implement the same
  contract interface.
- Governance (`yeraziael/ai-governance`) can reference ACP contract versions
  for its rules on authority boundaries.

**Harder:**
- Existing bash-based task handlers (`task_contract.sh`, `task_handlers.sh`)
  need adapters to produce and consume ACP contracts.
- Eddie's executor registration currently lacks `version` and `action` granularity
  (capabilities is a flat string list).
- Lydia's `executor_server.py` handles `callback_url` ad-hoc; the ACP contract
  formalizes this.

## Relation to Existing Mechanisms

| Existing | ACP v0.2 | Mapping |
|----------|----------|---------|
| Task contract (`lydia-task/v1`) | Execution Contract | `task_id` → `execution_id`, `task_type` → `action`, `payload` → `parameters` |
| Worker contract (`worker_schema.json`) | Execution Contract | `task` → resolved parameters, `acceptance` → `success_criteria` |
| Eddie executor registration | Trigger Contract resolution | `Capabilities` → `action_ref` resolution |
| Eddie cron/scheduler | Trigger Contract `trigger_type: cron` | Same concept, formalized |
| Eddie dispatcher retry | Trigger Contract `retry` | Same mechanism, formalized |

## References

- Issue: `yeraziael/slartis-backlog#88`
- Pilot 57: `FINDINGS/PILOT-57.md`
- Existing task contract: `lydia/home-repo/runtime/dispatch/task_contract.sh`
- Existing worker schema: `lydia/home-repo/runtime/dispatch/worker_schema.json`
- Eddie executor contract: `lydia/home-repo/runtime/eddie/server/executors.go`
- Eddie dispatcher: `lydia/home-repo/runtime/eddie/dispatcher/dispatcher.go`
- Lydia executor: `lydia/home-repo/runtime/processor/executor_server.py`
- Architecture: `Homelab/Architecture/docs/ARCHITECTURE.md`
