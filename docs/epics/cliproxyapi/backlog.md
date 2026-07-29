# Executable Backlog

IDs are dependency ordered. Each execution issue must add acceptance evidence, rollback and secret-handling details before implementation.

| ID | Task | Depends on | Status |
|---|---|---|---|---|
| CAP-P01 | Reconcile PR #71, issue #74, legacy directory and upstream facts | — | Complete |
| CAP-P02 | Independent architecture and security review | CAP-P01 | Ready |
| CAP-G01 | Define released governance schema and local override model | CAP-P02 | Planned |
| CAP-G02 | Implement classification challenge and conflict governance | CAP-G01 | Planned |
| CAP-G03 | Implement checkpoint and commit-trailer validation | CAP-G01 | Planned |
| CAP-B01 | Select pinned upstream version and image/build strategy | CAP-P01 | Planned |
| CAP-I01 | Deploy internal-only production gateway foundation | CAP-B01, CAP-P02 | Planned |
| CAP-I02 | Implement per-client keys and Keycloak management roles | CAP-I01 | Planned |
| CAP-R01 | Implement provider/account eligibility and sequential quota routing | CAP-I02, CAP-G01 | Planned |
| CAP-R02 | Implement sticky routing, Retry-After and bounded backoff probes | CAP-R01 | Planned |
| CAP-R03 | Implement deterministic dry-run API and Decision Hash | CAP-R01, CAP-G02 | Planned |
| CAP-O01 | Implement audit ring and persistent heuristic telemetry | CAP-R01 | Planned |
| CAP-O02 | Implement drain, backup, degraded mode and restore | CAP-I01 | Planned |
| CAP-O03 | Implement seven-day admission calibration and dashboard diagnostics | CAP-O01, CAP-O02 | Planned |
| CAP-E01 | Build ephemeral experiment controller and isolated test container | CAP-I02, CAP-O03 | Planned |
| CAP-E02 | Implement run lifecycle, attempts, limits, overrides and reactivation | CAP-E01 | Planned |
| CAP-E03 | Implement report, manifest, hash, confinement and HTTP package delivery | CAP-E02 | Planned |
| CAP-E04 | Add Playwright fixtures, reset endpoints and reproducibility suite | CAP-E03 | Planned |
| CAP-A01 | Run OpenCode pilot and provider compliance gate | CAP-R02, CAP-O02 | Planned |
| CAP-A02 | Enable Slarti and Lydia through OpenCode | CAP-A01 | Planned |
| CAP-F01 | Freeze execution manifest, hash and handover | all required milestones | Planned |

## Issue #74 mapping

Issue #74 must not be silently closed. CAP-P01 has inventoried every obligation:

| #74 obligation | CAP-P01 status | Notes |
|---|---|---|
| Current releases, registry, architectures | Completed | Upstream v7.2.104 verified 2026-07-29 |
| ARM64 build + resource usage | Retained, needs runtime | No deployment executed |
| Per-provider port documentation | Open question | Upstream docs insufficient |
| API/management/control-panel/plugin/debug audit | Completed | All surfaces documented in references.md |
| API-key vs OAuth per provider assessment | Completed | OAuth is primary mechanism |
| OpenCode endpoint test | Retained, deferred to CAP-A01 | Needs running instance |
| Secure baseline config | Open, blocks CAP-B01 | Multiple compliance blockers identified |
| Go/No-Go + host decision | Blocked on CAP-P02 | Requires independent review first

## Regression debt

A regression receives `<origin-task>-RF<n>`, references the introducing task, broken task, causing PR/commit and evidence. Open regression debt blocks regular merges in the same functional area unless an independent reviewer or Operator grants a documented time-limited waiver: 14 days, then 7, then 3; no further waiver after that.