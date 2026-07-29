# Executable Backlog

IDs are dependency ordered. Each execution issue must add acceptance evidence, rollback and secret-handling details before implementation.

| ID | Task | Depends on | Status |
|---|---|---|---|
| CAP-P01 | Reconcile PR #71, issue #74, legacy directory and upstream facts | — | Ready |
| CAP-P02 | Independent architecture and security review | CAP-P01 | Ready |
| CAP-G01 | Define released governance schema and local override model | CAP-P02 | Planned |
| CAP-G02 | Implement classification challenge and conflict governance | CAP-G01 | Planned |
| CAP-G03 | Implement checkpoint and commit-trailer validation | CAP-G01 | Planned |
| CAP-L01 | Select and pin LiteLLM upstream version and image strategy | CAP-P01 | Planned |
| CAP-L02 | Deploy LiteLLM production frontdoor with Zen Free and Ollama routing | CAP-L01, CAP-P02 | Planned |
| CAP-L03 | Implement per-client LiteLLM credentials and Keycloak integration | CAP-L02 | Planned |
| CAP-L04 | Implement LiteLLM-to-CLIProxyAPI forwarding for subscription/OAuth | CAP-L02 | Planned |
| CAP-L05 | Implement LiteLLM routing audit and telemetry | CAP-L03 | Planned |
| CAP-B01 | Select and pin CLIProxyAPI upstream version and image strategy | CAP-P01 | Planned |
| CAP-I01 | Deploy CLIProxyAPI as private downstream backend | CAP-B01, CAP-P02 | Planned |
| CAP-I02 | Implement CLIProxyAPI provider/account isolation and OAuth auth | CAP-I01 | Planned |
| CAP-I03 | Implement CLIProxyAPI sequential quota routing and sticky sessions | CAP-I02, CAP-G01 | Planned |
| CAP-I04 | Implement CLIProxyAPI Retry-After, backoff and probes | CAP-I03 | Planned |
| CAP-R01 | Implement end-to-end deterministic dry-run API and Decision Hash | CAP-L04, CAP-I03, CAP-G02 | Planned |
| CAP-O01 | Implement audit ring and persistent heuristic telemetry | CAP-L05 | Planned |
| CAP-O02 | Implement drain, backup, degraded mode and restore (both gateways) | CAP-L02, CAP-I01 | Planned |
| CAP-O03 | Implement seven-day admission calibration and dashboard diagnostics | CAP-O01, CAP-O02 | Planned |
| CAP-E01 | Build ephemeral experiment controller with LiteLLM and CLIProxyAPI test containers | CAP-L04, CAP-I02, CAP-O03 | Planned |
| CAP-E02 | Implement run lifecycle, attempts, limits, overrides and reactivation | CAP-E01 | Planned |
| CAP-E03 | Implement report, manifest, hash, confinement and HTTP package delivery | CAP-E02 | Planned |
| CAP-E04 | Add Playwright fixtures, reset endpoints and reproducibility suite | CAP-E03 | Planned |
| CAP-A01 | Run OpenCode pilot against LiteLLM frontdoor with provider compliance gate | CAP-R01, CAP-O02 | Planned |
| CAP-A02 | Enable Slarti and Lydia through OpenCode | CAP-A01 | Planned |
| CAP-F01 | Freeze execution manifest, hash and handover | all required milestones | Planned |

## Issue #74 mapping

Issue #74 must not be silently closed. CAP-P01 inventories every obligation and maps it to retained, superseded, split or completed status. Any runtime evidence from #74 remains linked from the corresponding execution item.

## Regression debt

A regression receives `<origin-task>-RF<n>`, references the introducing task, broken task, causing PR/commit and evidence. Open regression debt blocks regular merges in the same functional area unless an independent reviewer or Operator grants a documented time-limited waiver: 14 days, then 7, then 3; no further waiver after that.
