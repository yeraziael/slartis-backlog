# Operations

## Maintenance and backup

Production backup uses drain mode:

1. New requests receive HTTP 503 with machine-readable `maintenance` and `Retry-After` when known.
2. Running requests may finish.
3. Drain waits at most 15 minutes.
4. If a request still runs, it is not aborted; backup is skipped and retried in the next window.
5. Two consecutive missed windows create a dashboard warning, not a GitHub issue.
6. Container may be paused for backup.
7. Persistent telemetry and required runtime state are included in regular Homelab backup.
8. Restore testing is part of Definition of Done.

A successful backup clears the warning automatically. A failed backup puts the service into degraded mode.

## Degraded mode

Inference continues, but regular CLIProxyAPI and governance updates are blocked. The Operator may authorize a production hotfix only for outage or security-critical work. The hotfix requires an explicit marker, risk assessment, rollback plan and mandatory backup attempt afterwards. Regular changes remain blocked until backup succeeds.

The Operator dashboard exposes `run backup now`: drain, wait up to 15 minutes, pause, back up persistent data, resume and verify. Success clears degraded; failure preserves degraded with a reason.

## Provider operations

Provider onboarding, account locking, credential rotation and revocation are Operator-only. Credentials never enter Git, issues, logs, reports or test packages. Each provider adapter requires a documented authentication method and compliance decision before activation.

## Governance rollout

Production automatically selects the latest released compatible governance. New releases affect new work immediately and running work only at a safe interruption point after commit. Regular governance updates are prohibited while degraded.

## Experiment retention

Experiment output is not backed up. The service provides the complete authenticated HTTP package until explicit finish, idle expiry or final retention expiry. The experimenter owns durable persistence. Once the download window expires, run state and package are irreversibly destroyed.

## Monitoring

Dashboard displays:

- provider and account eligibility
- routing state and active governance version
- audit ring status
- backup and degraded state
- host admission calibration and current thresholds
- active experiment runs, attempts, deadlines and overrides
- missed backup warning and manual recovery action

No automatic GitHub issue is created for transient operational warnings unless a later governance rule explicitly requires one.