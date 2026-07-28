# Architecture

## Runtime topology

```mermaid
flowchart LR
  S[Slarti] --> O[OpenCode]
  L[Lydia] --> O
  W[Future workers] -. later .-> O
  O --> C[CLIProxyAPI production]
  C --> OA[OpenAI accounts]
  C --> Z[OpenCode Zen Free accounts]
  C --> G[Gemini accounts]
  K[Keycloak] --> D[Dashboard and management API]
  D --> C
  E[Experimenter / Playwright] --> X[Ephemeral experiment controller]
  K --> X
  X --> T[Ephemeral CLIProxyAPI test container]
  T --> A[Run-local artifacts]
  A --> H[Authenticated HTTP download]
```

## Trust boundaries

1. OpenCode is the only normal model client endpoint consumer.
2. Production provider credentials are available only to production CLIProxyAPI and never to experiment containers.
3. Keycloak controls dashboard, management API and experiment authorization.
4. Runtime telemetry is persistent production state but remains outside Git; only schema, migrations, aggregation logic and compact approved summaries are versioned.
5. Experiment artifacts are run-local, ephemeral and confined to the canonical run directory.

## Production data paths

- Incoming OpenCode request is authenticated by a per-client credential.
- Task classification is accepted, challenged upward or generated when absent.
- Released global governance and approved project-local additions produce the candidate set.
- Account state, quota, backoff, stickiness and quality metrics select provider, model and account.
- Routing audit records assignment metadata only: task, class, model, provider, governance version, override/fallback and reason.
- Prompts, responses, secrets and account identifiers are not persisted by planning contract.

## Experiment control plane

The experiment controller owns lifecycle and package delivery. The test container is created only for a run, receives isolated fixtures and spoofable non-production state, and cannot access production secrets. It writes only beneath `experiments/<run-id>/`. On finalization, the directory becomes immutable, is packaged as `cliproxyapi-experiment-<run-id>.tar.gz` and exposed through an authenticated download endpoint until explicit finish or idle/retention expiry.

## Management roles

### `operator`

May enable or disable providers, lock or unlock individual production accounts, inspect routing state, diagnose degraded mode, trigger backup, authorize run-specific concurrency and duration overrides, extend or reactivate experiment runs and use simulator spoofing.

### `test-service`

May use the simulator, versioned fixtures, Playwright test endpoints, reset isolated test state and set spoofed quota/provider/telemetry state. It cannot affect production state.

### Authenticated user

May execute read-only real-state dry-runs without spoofing.

## Decision engine

The dashboard and dry-run API use the same routing engine as production. With identical normalized input, governance and effective system state, the result is deterministic and includes a stable Decision Hash. The hash changes only when the effective routing decision changes.

## Resilience

Production CLIProxyAPI may enter maintenance or degraded state. Planned maintenance returns HTTP 503 with machine-readable `maintenance` and `Retry-After` when known. Degraded mode permits inference but blocks regular CLIProxyAPI and governance updates. Only Operator-authorized outage/security production hotfixes are allowed until a successful backup clears degraded state.