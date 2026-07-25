# Architecture — ACP v0.2 Contracts

## Current State (ACP v0.1.0-draft)

- Slarti → Lydia: unstructured task descriptions, ad-hoc parameters
- Eddie → Lydia: no formal trigger mechanism; scheduling done via cron/systemd
- No versioning of actions or tools
- No structured error handling for rejected tasks

## New/Changed Components

### Execution Contract (`SPEC/execution-contract.md`)

- **7-state lifecycle:** Draft → Active → Running → Completed | Failed → Archived
- **Immutable after activation** — contract content cannot change post-activation
- **Executor interprets nothing** — every parameter is explicit
- **Structured rejection** — missing fields, unknown actions, unmet preconditions return structured errors

### Trigger Contract (`SPEC/trigger-contract.md`)

- **6 trigger types:** cron, interval, event, manual, condition, webhook
- **5-state lifecycle:** Registered → Active → Suspended → Completed → Archived
- **Eddie triggers only, never executes** — no execution logic in Orchestrator
- **Immutability** — contracts are immutable after submission/activation

### Data Flow

```
Slarti ──(Execution Contract)──→ Lydia
   │                                 │
   │                                 ├── validates (schema, preconditions)
   │                                 ├── executes (registered action)
   │                                 └── returns (structured result)
   │
Eddie ──(Trigger Contract)──→ Lydia
   │                                 │
   ├── checks schedule/event         ├── validates at trigger time
   └── dispatches execution          └── returns (status + evidence)
```

## Architecture Decisions

- ADR-001 (`DECISIONS/001-execution-trigger-contracts.md`) documents:
  - Why separate contracts instead of unified
  - Mapping to existing mechanisms (Lydia task-loop, plugin-engine, worker-dispatch)
  - Consequences for immutability and versioning

## Impact on Existing Responsibilities

| Role | Before | After |
|------|--------|-------|
| Slarti | Free-form tasking | Structured contract submission |
| Lydia | Interpretive execution | Deterministic, schema-validated execution |
| Eddie | No formal trigger role | Registered action dispatch only |
