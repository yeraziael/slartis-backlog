# Trigger Contract (ACP v0.2)

**Version:** 0.2.1-draft
**Status:** Draft
**Supersedes:** Eddie's implicit cron definitions and ad-hoc webhook registrations

## Purpose

The Trigger Contract defines the formal agreement between a **Principal**
(Slarti, Operator) and an **Orchestrator** (Eddie) regarding when and how to
invoke an Execution Contract. The Orchestrator triggers but does not define or
modify the execution. Eddie contains no execution logic.

## Normative Principles

1. **Eddie triggers registered actions only.** Every trigger references an
   `action_ref` that matches a registered action in the Execution Contract
   space. Eddie never constructs, modifies, or infers action parameters.

2. **Eddie contains no execution logic.** Eddie does not translate, transform,
   or supplement the action definition. Its sole responsibility is to produce
   valid Execution Contracts from trigger definitions and submit them to the
   appropriate executor.

3. **Immutable identity model.** Every trigger definition is uniquely identified
   by the immutable pair `(trigger_id, activation.version)`. Changing any field
   of an active trigger — parameters, schedule, action_ref, or trigger_type —
   requires a new `activation.version`. Eddie MUST reject registration attempts
   where the same `(trigger_id, version)` pair already exists with different
   content. This ensures deterministic audit trails: every execution can be
   traced to exactly one trigger version.

5. **Missed runs are Eddie's accountability.** Eddie must handle scheduling
   gaps, retries, and deadline violations according to the contract without
   requiring operator intervention for routine misses.

## Lifecycle

```
                    ┌──────────────────┐
                    │   REGISTERED     │
                    │ (Principal       │
                    │  registers       │
                    │  trigger def.)   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   VALIDATED      │
                    │ (Eddie checks    │
                    │  action_ref,     │
                    │  executor avail.)│
                    └────────┬─────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
            ┌──────────────┐ ┌──────────────┐
            │   ACTIVE     │ │   REJECTED   │
            │ (firing on   │ │ (validation  │
            │  schedule)   │ │  failure)    │
            └──────┬───────┘ └──────────────┘
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
   ┌──────────────┐ ┌──────────────┐
   │  DISABLED    │ │  EXPIRED     │
   │ (manual)     │ │ (end_date    │
   │              │ │  reached)    │
   └──────────────┘ └──────────────┘
```

### Transitions

- `REGISTERED → VALIDATED`: Eddie received the trigger definition
- `VALIDATED → ACTIVE`: All validations passed, trigger begins firing
- `VALIDATED → REJECTED`: Validation failed (unknown action, unresolvable
  executor, invalid schedule)
- `ACTIVE → DISABLED`: Principal or operator manually disables the trigger
- `ACTIVE → EXPIRED`: `end_date` or `max_firings` reached
- `DISABLED → ACTIVE`: Re-enabled by Principal or operator

## Fields

### `acp_version`
- **Type:** `string` (const)
- **Required:** yes
- **Value:** `"0.2.1-draft"`

### `trigger_id`
- **Type:** `string`
- **Required:** yes
- **Pattern:** `^[A-Za-z0-9._~-]{1,128}$`
- **Description:** Globally unique identifier for this trigger definition.
  Used for idempotent registration: registering the same `trigger_id` again
  MUST update the existing definition, not create a duplicate.

### `action_ref`
- **Type:** `string`
- **Required:** yes
- **Pattern:** `^[a-z][a-z0-9._/-]{2,63}:[0-9]+\.[0-9]+\.[0-9]+$`
- **Description:** Reference to a registered action with mandatory version
  suffix. Format: `<action>:<version>`. Example: `ollama.prompt:1.2.0`.
  Eddie MUST resolve this against the executor's registered capabilities and
  reject the trigger if no executor provides the action.

### `provenance`
- **Type:** `object`
- **Required:** yes
- **Description:** Origin of the trigger definition.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `principal` | `string` | yes | Creator identity (e.g. `slarti`, `operator`) |
| `trace_id` | `string` | yes | Correlation ID |
| `created_at` | `string` (ISO 8601) | yes | When the trigger was defined |

### `trigger_type`
- **Type:** `string`
- **Required:** yes
- **Enum:** `"schedule"`, `"cron"`, `"event"`, `"webhook"`, `"manual"`,
  `"condition"`
- **Description:** The type of trigger.

| Type | Description |
|------|-------------|
| `schedule` | One-shot or interval-based (every N seconds/minutes/hours) |
| `cron` | Standard cron expression with timezone |
| `event` | Fires on a specific event type from Eddie's event router |
| `webhook` | Fires on an external HTTP POST to a webhook URL |
| `manual` | Fires only on explicit operator invocation |
| `condition` | Fires when a boolean condition evaluates to true |

### `schedule` (required when `trigger_type` is `schedule` or `cron`)
- **Type:** `object`
- **Required:** conditional

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cron` | `string` | for `cron` | Standard 5-field cron expression |
| `interval_seconds` | `integer` | for `schedule` | Interval in seconds |
| `timezone` | `string` | no | IANA timezone (default: `UTC`) |
| `start_date` | `string` (ISO 8601) | no | When to start firing |
| `end_date` | `string` (ISO 8601) | no | When to stop firing |
| `max_firings` | `integer` | no | Maximum number of firings before auto-expire |

### `event_filter` (required when `trigger_type` is `event`)
- **Type:** `object`
- **Required:** conditional

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `event_type` | `string` | yes | Event type to match (e.g. `gitea.issue.created`, `paperless.document.received`) |
| `source` | `string` | no | Event source filter |
| `condition` | `string` | no | JSONPath or JMESPath expression to filter event payload |

### `webhook` (required when `trigger_type` is `webhook`)
- **Type:** `object`
- **Required:** conditional

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | `string` | yes | URL path suffix (e.g. `/webhooks/my-trigger`) |
| `method` | `string` | no | HTTP method to accept (default: `POST`) |
| `secret_ref` | `string` | no | Reference to a shared secret for HMAC validation. Format: `secret:<name>` or `vault:<path>`. Eddie MUST resolve the reference to a concrete secret value before registration succeeds. An unresolvable reference MUST cause a `resolution` rejection. |

### `parameters`
- **Type:** `object`
- **Required:** yes
- **Description:** Static or template parameters to include in every Execution
  Contract produced by this trigger. These are merged with any dynamic
  parameters from the event payload.

### `retry`
- **Type:** `object`
- **Required:** no
- **Description:** Retry policy for failed executions.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `max_retries` | `integer` | no | `3` | Maximum retry attempts |
| `backoff_strategy` | `string` | no | `exponential` | One of: `fixed`, `exponential`, `linear` |
| `backoff_seconds` | `integer` | no | `5` | Base backoff interval in seconds |
| `max_backoff_seconds` | `integer` | no | `300` | Maximum backoff interval |

### `deduplication`
- **Type:** `object`
- **Required:** no
- **Description:** Deduplication and idempotency strategy.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `idempotency_key_source` | `string` | no | `trigger_id + timestamp` | Strategy for generating idempotency keys: `trigger_id`, `event_id`, `custom` |
| `dedup_window_seconds` | `integer` | no | `0` | Time window in seconds for deduplication (0 = disabled) |

### `concurrency`
- **Type:** `object`
- **Required:** no
- **Description:** Concurrency and locking behavior.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `max_concurrent` | `integer` | no | `1` | Maximum concurrent executions from this trigger |
| `lock_key` | `string` | no | `trigger_id` | Key for locking across triggers |
| `queue_on_conflict` | `boolean` | no | `false` | Whether to queue execution if at concurrency limit |

### `deadline`
- **Type:** `object`
- **Required:** no
- **Description:** Deadline and missed-run behavior.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `missed_run_action` | `string` | no | `skip` | One of: `skip`, `catch_up`, `error` |
| `max_execution_seconds` | `integer` | no | `300` | Per-execution timeout (overrides the Execution Contract default) |

### `notifications`
- **Type:** `object`
- **Required:** no
- **Description:** Notification and escalation rules.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `on_success` | `array` of `string` | no | `[]` | Notification channels on success |
| `on_failure` | `array` of `string` | no | `["default"]` | Notification channels on failure |
| `on_missed` | `array` of `string` | no | `[]` | Notification channels on missed run |
| `escalate_after` | `integer` | no | `3` | Consecutive failures before escalation |

### `activation`
- **Type:** `object`
- **Required:** no
- **Description:** Activation controls.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `enabled` | `boolean` | no | `true` | Whether the trigger is active on registration |
| `version` | `string` | no | `"1.0.0"` | Trigger definition version for change tracking |

## Return Value (Trigger Registration)

Eddie MUST respond to trigger registration requests:

```json
{
  "trigger_id": "...",
  "status": "active" | "rejected",
  "action_ref": "...",
  "trigger_type": "...",
  "schedule_summary": "...",
  "created_at": "2026-07-25T12:00:00Z",
  "error": {
    "class": "validation" | "resolution",
    "message": "..."
  }
}
```

## Sequence: Slarti → Eddie → Lydia → Result

```
Slarti                        Eddie                         Lydia
  │                             │                             │
  │  1. register trigger ──────→│                             │
  │     (Trigger Contract)     │                             │
  │                             │                             │
  │                             │  2. validate action_ref     │
  │                             │     resolve executor        │
  │                             │                             │
  │                             │  3. on schedule/event:      │
  │                             │     create Execution        │
  │                             │     Contract                │
  │                             │                             │
  │                             │  4. dispatch ──────────────→│
  │                             │     (Execution Contract)    │
  │                             │                             │
  │                             │                             │  5. validate preconditions
  │                             │                             │     start execution
  │                             │                             │
  │                             │                             │  6. ── COMPLETED/FAILED ──
  │                             │←──── callback ─────────────│
  │                             │     (status + evidence)     │
  │                             │                             │
  │                             │  7. retry/notify/escalate   │
  │                             │                             │
  │  8. result notification ────│                             │
  │     (evidence summary)      │                             │
```

### Sequence Steps

1. **Slarti registers a Trigger Contract** with Eddie (via HTTP API or Gitea
   Issue with `trigger` label). The contract specifies `action_ref`,
   `trigger_type`, `parameters`, retry and notification policies.

2. **Eddie validates** the trigger: resolves `action_ref` against registered
   executor capabilities, checks that at least one executor provides the action,
   validates schedule/event syntax.

3. **On schedule tick or event match**, Eddie constructs an Execution Contract
   by copying `parameters` from the trigger definition and adding runtime
   fields (`execution_id`, `provenance.trace_id`).

4. **Eddie dispatches** the Execution Contract to the appropriate executor
   (identified during step 2) via the executor's registered endpoint.

5. **Lydia validates** preconditions, acquires locks, and executes the action.

6. **Lydia returns** the result synchronously (or via callback for async
   actions) with status, output, and evidence.

7. **Eddie processes** the result: marks success, schedules retry on failure,
   escalates if retries exhausted, sends notifications.

8. **Eddie notifies** Slarti (or the configured notification target) with
   the execution result and evidence summary.

## Alignment With Existing Architecture

| ACP Term | Eddie/Lydia/home-repo mapping |
|----------|-------------------------------|
| `trigger_id` | Eddie job `id` or scheduler entry key |
| `action_ref` | `RegisterExecutorRequest.Capabilities` + action versioning |
| `trigger_type: cron` | Eddie scheduler `cron.go` |
| `trigger_type: event` | Eddie event router (`POST /api/v1/events`) |
| `trigger_type: webhook` | Eddie webhooks (`server/webhooks.go`) |
| `trigger_type: manual` | Eddie job API (`POST /api/v1/jobs`) |
| `parameters` | `DispatchRequest.Params` → executor `params` |
| `retry` | Eddie dispatcher `retryFailed()`, `retryDelay()` |
| `concurrency` | Eddie executor `Concurrency` field, `ActiveCount` tracking |
| `deduplication` | Task contract duplicate check (`task_contract_create` return 2) |
| `notifications` | Not yet formalized; currently via `callback_url` + outgoing/ |
| `deadline` | Eddie dispatcher `checkTimeouts()` |
