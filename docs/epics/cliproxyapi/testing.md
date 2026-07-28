# Testing and Evidence

## Required test layers

- Static schema, configuration, link and stable-ID validation.
- Secret scanning for repository, logs, reports and packages.
- Reproducible image build and digest verification for supported architectures.
- Authentication and authorization tests for normal user, `test-service` and `operator`.
- Provider/account isolation, sticky routing and sequential quota rollover.
- Retry-After handling, exponential backoff, model-specific probe and automatic resume.
- Classification challenge, conflict precedence and released-governance adoption.
- Checkpoint commit and `Resolves-Checkpoint:` merge gates.
- Maintenance drain, missed backup, degraded mode, hotfix and restore.
- Dry-run determinism, Decision Hash stability and spoof/non-spoof separation.
- Experiment lifecycle, attempts, idle, keep-alive, hard stop, reactivation and expiry.
- Resource and admission protection under CPU, memory, swap, I/O and disk pressure.
- Package schema, canonical SHA-256, artifact confinement and immutable finalization.

## Playwright contract

Playwright uses only the separate experiment container and test endpoints. Versioned fixtures create defined initial state. Reset endpoints affect only isolated test state. A run report records browser, Playwright version, suite, fixtures, configuration, expected and actual results, traces and screenshots.

## Security tests

- Test container cannot resolve, mount or read production provider secrets.
- External artifact paths, traversal and escaping symlinks are refused.
- Prompt, response, secret and account-identifier leakage tests are mandatory.
- Unauthorized spoofing, provider management, backup and override operations fail closed.
- Operator overrides never bypass fixed CPU/RAM limits or artifact isolation.

## Admission tests

Before sufficient calibration history, conservative bootstrap limits are tested. After seven days, tests verify robust calibration, outlier resistance and activation only between runs. Each rejection must produce the required diagnostic snapshot without secrets.

## Evidence contract

Every executable backlog item defines:

- acceptance criteria
- test commands or API sequence
- expected evidence
- negative tests
- rollback
- secret-handling constraints
- model and governance trailers

A task is complete only when implemented, verified, independently reviewed, approved and merged. A merged regression creates a separate `-RF<n>` debt item and does not reopen the old task.