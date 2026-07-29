# Testing and Evidence

## Required test layers

- Static schema, configuration, link and stable-ID validation.
- Secret scanning for repository, logs, reports and packages.
- Reproducible image build and digest verification for supported architectures.
- LiteLLM configuration validation (model routing, provider backends, credential isolation).
- Authentication and authorization tests for normal user, `test-service` and `operator`.
- Provider/account isolation across LiteLLM and CLIProxyAPI.
- LiteLLM direct routing to Zen Free and Ollama.
- LiteLLM-to-CLIProxyAPI forwarding for subscription/CLI/OAuth backends.
- Explicit OpenCode model-ID mapping to LiteLLM model groups; tests must not assume automatic custom-provider discovery.
- Sticky routing and sequential quota rollover end-to-end.
- CLIProxyAPI `fill-first` configuration for sequential account use and stable affinity-key propagation across both hops.
- Retry-After handling, exponential backoff, model-specific probe and automatic resume.
- Classification challenge, conflict precedence and released-governance adoption.
- Checkpoint commit and `Resolves-Checkpoint:` merge gates.
- Maintenance drain, missed backup, degraded mode (LiteLLM and CLIProxyAPI independently), hotfix and restore.
- Dry-run determinism, Decision Hash stability and spoof/non-spoof separation.
- Experiment lifecycle, attempts, idle, keep-alive, hard stop, reactivation and expiry.
- Resource and admission protection under CPU, memory, swap, I/O and disk pressure.
- Package schema, canonical SHA-256, artifact confinement and immutable finalization.

## Playwright contract

Playwright uses only the separate experiment containers and test endpoints. Versioned fixtures create defined initial state. Reset endpoints affect only isolated test state. A run report records browser, Playwright version, suite, fixtures, configuration, expected and actual results, traces and screenshots. Playwright tests cover both LiteLLM and CLIProxyAPI experiment containers.

## Security tests

- Test containers cannot resolve, mount or read production provider secrets.
- External artifact paths, traversal and escaping symlinks are refused.
- Prompt, response, secret and account-identifier leakage tests are mandatory.
- Unauthorized spoofing, provider management, backup and override operations fail closed.
- Operator overrides never bypass fixed CPU/RAM limits or artifact isolation.
- LiteLLM cannot access CLIProxyAPI-internal credentials; CLIProxyAPI cannot access LiteLLM Zen Free or Ollama credentials.
- CLIProxyAPI binds only to the approved private network; plugins, control-panel download/update, cloaking, remote management and debug endpoints remain disabled.
- Provider OAuth callback ports fail closed unless the tested provider contract explicitly enables that exact port.

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
