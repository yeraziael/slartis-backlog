# Execution Contract (ACP v0.2)

**Version:** 0.2.1-draft
**Status:** Draft
**Supersedes:** Implicit execution conventions in `lydia/home-repo`

## Purpose

The Execution Contract defines the formal agreement between a **Principal**
(Slarti, Operator) and an **Executor** (Lydia, Execution Plane) for a single
deterministic action. It ensures that the Executor receives everything it needs
to execute without interpretation, inference, or tool selection.

## Normative Principles

1. **The Executor interprets nothing.** Every parameter, precondition, timeout,
   and success criterion is explicit in the contract. The Executor may not infer
   missing values, select tools autonomously, or supplement the action.

2. **The Executor rejects incomplete contracts.** Any missing required field,
   unresolved reference, or unfulfillable precondition causes a structured
   rejection before any execution attempt.

3. **The Principal is responsible for tool availability.** The action,
   referenced by `action` + `version`, must be registered and versioned in the
   Executor's handler or plugin registry before the contract is submitted.

4. **The contract is immutable after submission.** The Principal may not modify
   a submitted contract while it is in `pending` or `running` state. A new
   contract with a new `execution_id` is required for changes.

## Lifecycle

```
                    ┌──────────────────┐
                    │   SUBMITTED      │
                    │ (Principal sends │
                    │  contract)       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
              ┌────│   VALIDATED      │────┐
              │    │ (Executor checks │    │
              │    │  preconditions)  │    │
              │    └────────┬─────────┘    │
              │             │              │
              ▼             ▼              ▼
     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
     │  REJECTED   │ │  APPROVED   │ │  REJECTED   │
     │ (precond.   │ │             │ │ (schema     │
     │  failure)   │ │             │ │  failure)   │
     └─────────────┘ └──────┬──────┘ └─────────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │   EXECUTING      │
                   │                  │
                   └────────┬─────────┘
                            │
                    ┌───────┴───────┐
                    │               │
                    ▼               ▼
           ┌──────────────┐ ┌──────────────┐
           │  COMPLETED   │ │   FAILED     │
           │ (with output │ │ (with error  │
           │  + evidence) │ │  + evidence) │
           └──────────────┘ └──────────────┘
```

### Transitions

- `SUBMITTED → VALIDATED`: Executor has received and parsed the contract
- `VALIDATED → APPROVED`: Preconditions met, action registered, schema valid
- `VALIDATED → REJECTED`: Schema validation or precondition failure
- `APPROVED → EXECUTING`: Executor has started the action
- `EXECUTING → COMPLETED`: Action finished with success criteria met
- `EXECUTING → FAILED`: Action finished with error or timeout

## Fields

### `acp_version`
- **Type:** `string` (const)
- **Required:** yes
- **Value:** `"0.2.1-draft"`
- **Description:** ACP specification version to which this contract conforms.

### `execution_id`
- **Type:** `string`
- **Required:** yes
- **Pattern:** `^[A-Za-z0-9._~-]{1,128}$`
- **Description:** Globally unique identifier for this execution. Used for
  idempotency, deduplication, and tracing. Must be stable across retries of the
  same logical action.

### `action`
- **Type:** `string`
- **Required:** yes
- **Pattern:** `^[a-z][a-z0-9._-]{2,63}$`
- **Description:** Registered action name in the Executor's handler or plugin
  registry. Example: `ollama.prompt`, `fileops.copy`, `issue.create`.
  Corresponds to the `capability` name from Eddie executor registration or the
  handler ID from Lydia's task dispatch registry.

### `version`
- **Type:** `string`
- **Required:** yes
- **Pattern:** `^[0-9]+\.[0-9]+\.[0-9]+$`
- **Description:** Semantic version of the action/tool that the Principal has
  verified as available, tested, and compatible. The Executor MUST reject the
  contract if the requested version is not available.

### `provenance`
- **Type:** `object`
- **Required:** yes
- **Description:** Who created this contract and how to trace it.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `principal` | `string` | yes | Identity of the contract creator (e.g. `slarti`, `operator`) |
| `session_id` | `string` | no | Session or ticket identifier for traceability |
| `trace_id` | `string` | yes | Correlation ID propagated across hops |
| `created_at` | `string` (ISO 8601) | yes | Timestamp of contract creation |

### `parameters`
- **Type:** `object`
- **Required:** yes
- **Description:** Typed parameters matching the action's schema. The Executor
  MUST validate parameters against the registered action schema before
  execution. Unknown or invalid parameters cause structured rejection.

### `preconditions`
- **Type:** `array` of `object`
- **Required:** no
- **Description:** Conditions that MUST be true before execution. Each
  precondition is evaluated by the Executor; any failure rejects the contract.

Each precondition object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | yes | One of: `file_exists`, `path_accessible`, `tool_available`, `network_reachable`, `resource_free`, `custom` |
| `target` | `string` | yes | Target of the precondition (path, host, resource name, tool name) |
| `message` | `string` | no | Human-readable description of the precondition |

### `security`
- **Type:** `object`
- **Required:** no
- **Description:** Security requirements that constrain execution.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `allowed_paths` | `array` of `string` | no | `[]` | Paths the action may read or write |
| `requires_approval` | `boolean` | no | `false` | Whether operator approval is required before execution |
| `allowed_hosts` | `array` of `string` | no | `[]` | Network targets the action may contact |

### `constraints`
- **Type:** `object`
- **Required:** yes
- **Description:** Execution boundaries. Every contract MUST specify explicit
  timeouts, retry limits, and concurrency/idempotency keys. Default values
  are never assumed — the Principal must choose deliberate bounds for every
  execution.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `timeout_seconds` | `integer` | no | `300` | Maximum execution time |
| `max_retries` | `integer` | no | `0` | Number of automatic retries on failure |
| `concurrency_key` | `string` | no | `null` | Prevents concurrent executions with the same key |
| `idempotency_key` | `string` | no | `execution_id` | Key for idempotent re-execution (defaults to `execution_id`) |

### `rollback`
- **Type:** `object`
- **Required:** yes
- **Description:** Rollback strategy for failures. Every contract MUST declare
  what happens on failure. Even actions that cannot be reverted MUST declare
  `strategy: none` explicitly. The Executor MUST execute the rollback strategy
  before returning the `FAILED` result if the executed action left state changes
  behind.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `strategy` | `string` | yes | One of: `revert`, `compensating_action`, `manual`, `none` |
| `action` | `string` | no | Action name for `compensating_action` strategy |
| `parameters` | `object` | no | Parameters for the compensation action |

### `success_criteria`
- **Type:** `array` of `object`
- **Required:** yes
- **Description:** Explicit criteria that define success. Every contract MUST
  declare at least one success criterion. A non-zero exit status or error
  response is always a failure regardless of criteria, but without explicit
  criteria the Executor cannot determine what constitutes a successful outcome.
  Example default: `[{ "type": "exit_code", "target": "0" }]`.

Each criterion object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | yes | One of: `exit_code`, `output_match`, `file_exists`, `custom` |
| `target` | `string` | yes | Expected value (exit code `0`, regex pattern, file path) |

### `evidence`
- **Type:** `object`
- **Required:** yes
- **Description:** What constitutes proof of execution.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `require_output` | `boolean` | no | Whether stdout/stderr must be captured |
| `require_artifacts` | `boolean` | no | Whether output files must be listed |
| `require_logs` | `boolean` | no | Whether execution logs must be retained |

### `failure_handling`
- **Type:** `object`
- **Required:** no
- **Description:** Structured error handling.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `error_classes` | `array` of `string` | no | `["timeout", "precondition", "execution", "permission"]` | Expected error classes |
| `notify_on` | `array` of `string` | no | `["failure"]` | When to notify (`failure`, `success`, `all`) |
| `escalate_after` | `integer` | no | `0` | Number of failures before escalation |

## Return Value

The Executor MUST return a structured response:

```json
{
  "execution_id": "...",
  "status": "completed" | "failed" | "rejected",
  "output": {
    "stdout": "...",
    "stderr": "...",
    "exit_code": 0
  },
  "artifacts": ["path/to/output.ext"],
  "evidence": {
    "logs": "...",
    "started_at": "2026-07-25T12:00:00Z",
    "completed_at": "2026-07-25T12:00:05Z"
  },
  "error": {
    "class": "execution" | "precondition" | "permission" | "timeout" | "schema",
    "message": "...",
    "details": {}
  }
}
```

## Alignment With Existing Architecture

| ACP Term | Lydia/home-repo mapping |
|----------|------------------------|
| `action` | Handler ID (`_TASK_HANDLERS` key) or Eddie executor capability |
| `version` | Tool/plugin version in `init.sh` or CI manifest |
| `parameters` | Task contract `payload` field |
| `preconditions` | Execution gate `confinement_check`, `policy_guard`, `path_sanitizer` |
| `security.allowed_paths` | Handler policy `allowed_paths` (`policy_guard.sh`) |
| `security.requires_approval` | Approval store (`approvals.py`) |
| `constraints.timeout_seconds` | Eddie job `timeout` field |
| `constraints.concurrency_key` | Task lock (`task_lock.sh`) |
| `constraints.idempotency_key` | Idempotency state (`idempotency.sh`) |
| `rollback` | Not yet formalized in existing code |
| `evidence` | Task contract `result.artifacts` |
| `failure_handling` | Task contract `result.failure_reason`, `result.escalation_required` |
