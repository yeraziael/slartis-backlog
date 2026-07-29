# Operations

## Maintenance and backup

Production backup uses drain mode across both gateways:

1. New requests receive HTTP 503 with machine-readable `maintenance` and `Retry-After` when known.
2. Running requests may finish.
3. Drain waits at most 15 minutes.
4. If a request still runs, it is not aborted; backup is skipped and retried in the next window.
5. Two consecutive missed windows create a dashboard warning, not a GitHub issue.
6. Container may be paused for backup.
7. Persistent telemetry and required runtime state are included in regular Homelab backup.
8. Restore testing is part of Definition of Done.

A successful backup clears the warning automatically. A failed backup puts the affected gateway into degraded mode.

## Degraded mode

### LiteLLM degraded

Inference for Zen Free and Ollama continues. CLIProxyAPI routing and governance updates are blocked. The Operator may authorize a production hotfix only for outage or security-critical work.

### CLIProxyAPI degraded

Subscription and OAuth backend routing is unavailable. LiteLLM continues routing Zen Free, Ollama and API-key providers. CLIProxyAPI hotfix rules are identical to LiteLLM degraded mode.

### Cross-gateway

The Operator dashboard exposes `run backup now` for each gateway independently: drain, wait up to 15 minutes, pause, back up persistent data, resume and verify. Success clears degraded; failure preserves degraded with a reason.

## Provider operations

Provider onboarding, account locking, credential rotation and revocation are Operator-only. Credentials never enter Git, issues, logs, reports or test packages. Each provider adapter requires a documented authentication method and compliance decision before activation. LiteLLM provider adapters (Zen Free, Ollama, API-key) and CLIProxyAPI provider adapters (subscription/CLI/OAuth) are managed separately.

## Governance rollout

Production automatically selects the latest released compatible governance. New releases affect new work immediately and running work only at a safe interruption point after commit. Regular governance updates are prohibited while either gateway is degraded.

## Experiment retention

Experiment output is not backed up. The service provides the complete authenticated HTTP package until explicit finish, idle expiry or final retention expiry. The experimenter owns durable persistence. Once the download window expires, run state and package are irreversibly destroyed.

## Monitoring

Dashboard displays:

- LiteLLM and CLIProxyAPI provider and account eligibility
- routing state and active governance version
- audit ring status per gateway
- backup and degraded state per gateway
- host admission calibration and current thresholds
- active experiment runs, attempts, deadlines and overrides
- missed backup warning and manual recovery action per gateway

No automatic GitHub issue is created for transient operational warnings unless a later governance rule explicitly requires one.
