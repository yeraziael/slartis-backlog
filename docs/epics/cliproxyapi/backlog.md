# Executable Backlog

`plan.yaml` is the machine-readable task graph. IDs are frozen when CAP-F01 completes. Each execution issue must preserve its CAP ID, dependencies, acceptance evidence, rollback and secret/runtime boundary.

## Status and dependencies

| ID | Task | Depends on | Status |
|---|---|---|---|
| CAP-P01 | Reconcile legacy plan and upstream facts | — | Complete |
| CAP-P02 | Independent architecture and security review | CAP-P01 | Complete |
| CAP-F01 | Freeze manifest, hash and execution-issue links | CAP-P02 | Complete |
| CAP-G01 | Define released governance schema and local override model | CAP-P02 | Planned |
| CAP-G02 | Implement pre-routing classification challenge and conflicts | CAP-G01 | Planned |
| CAP-G03 | Implement checkpoint and commit-trailer validation | CAP-G01 | Planned |
| CAP-L01 | Pin LiteLLM source, image and compatibility matrix | CAP-P02 | Implemented in code |
| CAP-S01 | Verify or reject end-to-end affinity contract | CAP-L01, CAP-B01 | Planned |
| CAP-L02 | Prepare reproducible LiteLLM frontdoor deployment | CAP-L01, CAP-P02 | Implemented in code |
| CAP-L03 | Implement LiteLLM model map, client-key schema and Keycloak contract | CAP-L02, CAP-G01 | Planned |
| CAP-L04 | Implement LiteLLM-to-CLIProxyAPI forwarding contract | CAP-L02, CAP-S01 | Planned |
| CAP-L05 | Implement LiteLLM routing audit and telemetry hooks | CAP-L03, CAP-G01 | Planned |
| CAP-B01 | Pin CLIProxyAPI source, image and capability matrix | CAP-P02 | Implemented in code |
| CAP-I01 | Prepare hardened private CLIProxyAPI deployment | CAP-B01, CAP-P02 | Implemented in code |
| CAP-I02 | Implement provider/account schema and OAuth secret-mount contract | CAP-I01 | Planned |
| CAP-I03 | Implement approved pools and end-to-end affinity | CAP-I02, CAP-G01, CAP-S01 | Planned |
| CAP-I04 | Implement bounded backoff and model-specific probe controller | CAP-I03 | Planned |
| CAP-R01 | Implement deterministic decision library, dry-run and hash | CAP-L04, CAP-I03, CAP-G02 | Planned |
| CAP-O01 | Implement cross-gateway audit ring and heuristic telemetry | CAP-L05, CAP-R01 | Planned |
| CAP-O02 | Implement drain, backup, degraded mode and restore automation | CAP-L02, CAP-I01 | Planned |
| CAP-O03 | Implement admission calibration and operator diagnostics | CAP-O01, CAP-O02 | Planned |
| CAP-E01 | Build isolated dual-gateway experiment controller | CAP-L04, CAP-I02, CAP-O03 | Planned |
| CAP-E02 | Implement experiment lifecycle and limits | CAP-E01 | Planned |
| CAP-E03 | Implement report, manifest, hash and package delivery | CAP-E02 | Planned |
| CAP-E04 | Implement Playwright and integration reproducibility suite | CAP-E03 | Planned |
| CAP-A01 | Prepare OpenCode pilot and compliance evidence package | CAP-R01, CAP-O02, CAP-E04 | Planned |
| CAP-A02 | Prepare Slarti/Lydia adoption and rollback runbook | CAP-A01 | Planned |
| CAP-X01 | Operator gate: deploy candidate and decide host | CAP-L02, CAP-I01, CAP-O02 | Operator gated |
| CAP-X02 | Operator gate: approve providers and provision credentials | CAP-L03, CAP-I02 | Operator gated |
| CAP-X03 | Operator gate: run OpenCode pilot | CAP-A01, CAP-X01, CAP-X02 | Operator gated |
| CAP-X04 | Operator gate: enable Slarti and Lydia | CAP-A02, CAP-X03 | Operator gated |

## Common execution contract

Every implementation task must:

- name the target repository, branch, permitted files and exact test working directory;
- add focused tests before implementation and wire them into required PR CI;
- use pinned source/image references and keep all example credentials inert;
- run the focused tests, repository suite and `git diff --check`;
- document rollback without executing deployment, DNS or credential changes;
- stop at an Operator gate for runtime, secret, provider-account or production action;
- return commit SHA, changed files, test commands/results, CI state and limitations.

## Task packets

### CAP-P01 — Reconcile legacy plan and upstream facts

Acceptance: PR #71, issue #74 and all eight legacy files are mapped; current CLIProxyAPI facts and compliance blockers are recorded in `references.md`.

Evidence: PR #130 commit `9b77bb7` plus the incorporated CAP-P01 sections in PR #131.

### CAP-P02 — Independent architecture and security review

Acceptance: LiteLLM/OpenCode, CLIProxyAPI/security and cross-document reviews complete; every blocker has a disposition; no unsupported enforcement claim remains.

Evidence: `references.md` independent-review disposition and PR #131 review comment bound to the reviewed head.

### CAP-F01 — Freeze manifest, hash and execution-issue links

Acceptance: `plan.yaml` validates, dependency graph is acyclic, every non-complete CAP task links one GitHub issue, exact SHA-256 is committed and PR #131 is review-ready.

Verification: parse YAML, verify unique IDs/dependencies/issue links, run `sha256sum -c plan.sha256`, `git diff --check`.

### CAP-G01 — Governance schema

Deliverable: versioned schema for classification, model eligibility, backend identity, auth class, compliance state, affinity and paid-fallback policy.

Acceptance: released global governance remains authoritative; local rules cannot weaken security; invalid/unknown releases fail closed; schema tests are required CI.

### CAP-G02 — Classification challenge

Deliverable: pre-routing challenge/conflict component independent of both gateways.

Acceptance: upward challenge works, silent lowering fails, equal-specificity conflict selects stricter class, unresolved mismatch requests Operator input, deterministic fixtures pass.

### CAP-G03 — Repository evidence gates

Deliverable: checkpoint/trailer validator and PR-CI integration.

Acceptance: unresolved checkpoints, checkpoint final commits and missing execution trailers fail CI; planning-only pre-freeze commits remain exempt.

### CAP-L01 — Pin LiteLLM

Deliverable: dated primary-source capability matrix and exact source/image digest for amd64 and arm64.

Acceptance: Zen API variants, Ollama, streaming, tools, model map, virtual keys, health/fallback and CLIProxyAPI forwarding are verified; mutable tags fail validation.

### CAP-S01 — End-to-end affinity spike

Deliverable: versions-bound decision packet that either defines or rejects the LiteLLM-to-CLIProxyAPI affinity interface.

Acceptance: pin both upstream versions; identify the exact LiteLLM hook and forwarded header/metadata field; define a collision-resistant opaque value and privacy boundary; prove matching CLIProxyAPI account selection; specify missing/malformed/expired key, account exhaustion, retry, failover and paid-fallback behavior; add black-box contract tests; obtain independent architecture/security review. If any element cannot be proven, record No-Go and retain single-account/fail-closed behavior.

Boundary: research, fixtures and isolated test topology only. No production subscriptions, credentials, ports or services.

### CAP-L02 — LiteLLM frontdoor preparation

Deliverable: Compose/config artifacts for a private, reproducible LiteLLM service without deploying them.

Acceptance: only LiteLLM is exposed to OpenCode, healthcheck exists, resource bounds and rollback are declared, configuration renders without secrets.

### CAP-L03 — LiteLLM model and client contract

Deliverable: explicit OpenCode-to-LiteLLM model map, virtual-key policy schema and Keycloak authorization contract using placeholders.

Acceptance: no automatic model discovery is assumed; stale/missing aliases fail CI; client isolation and least privilege have negative tests; no real keys are created.

### CAP-L04 — CLIProxyAPI downstream adapter

Deliverable: LiteLLM model groups and transport mapping for private CLIProxyAPI ingress.

Acceptance: backend identity/auth class/compliance metadata survive routing; no direct OpenCode URL exists; the accepted CAP-S01 affinity contract is implemented exactly; subscription exhaustion cannot change accounts for a stateful session or reach a paid API fallback unless that behavior is explicitly authorized by the contract and governance.

### CAP-L05 — LiteLLM telemetry hooks

Deliverable: secret-free gateway-hop event interface and tests.

Acceptance: task/model/provider/gateway/governance/reason fields are emitted; prompts, responses, keys and account identifiers are rejected or redacted.

### CAP-B01 — Pin CLIProxyAPI

Deliverable: exact source/image digest and provider/port/auth capability matrix.

Acceptance: ARM64 build is reproducible; every enabled feature maps to primary-source evidence; mutable image, unreviewed plugin and auto-update fail CI.

### CAP-I01 — Hardened CLIProxyAPI preparation

Deliverable: private Compose/config baseline without deployment.

Acceptance: private bind only; plugins, panel download/update, cloaking, remote management and debug disabled; callback ports deny by default; no production auth mount exists in tests.

### CAP-I02 — Provider/account contract

Deliverable: provider inventory schema, secret-mount paths and operator procedures with inert placeholders.

Acceptance: each provider records auth class, compliance status, ports and revocation; management and provider secrets are separate; experiment mounts cannot resolve production paths.

### CAP-I03 — Sequential pools and affinity

Deliverable: `fill-first` stateless pool config plus only the affinity mapping accepted by CAP-S01.

Acceptance: stateless exhaustion moves to the next eligible account; a stateful session stays on one account; loss of that account follows CAP-S01 fail-closed/failover semantics; unrelated sessions cannot infer account identity.

### CAP-I04 — Backoff and probe controller

Deliverable: custom controller for Retry-After, jittered 1-minute to 6-hour backoff and exact-model minimal probes.

Acceptance: provider reset wins, probes never use a different model, success resets delay and resumes, attempts are bounded and auditable.

### CAP-R01 — Deterministic decision library

Deliverable: shared routing-decision library, production adapter and read-only dry-run API.

Acceptance: normalized input plus governance/state yields identical Decision Hash; spoofing is test-only; neither gateway-native behavior is misrepresented as this custom contract.

### CAP-O01 — Audit and telemetry

Deliverable: 250-entry complete-record ring and persistent heuristic store.

Acceptance: gateway hops correlate without account IDs; crash/restart semantics are tested; schema/migrations/aggregation are versioned; secret scanning passes.

### CAP-O02 — Backup and degraded mode

Deliverable: drain/backup/restore automation and independent LiteLLM/CLIProxyAPI degraded-state logic.

Acceptance: 15-minute drain never aborts solely for backup; failed backup degrades only affected scope; restore test and rollback evidence pass without production execution.

### CAP-O03 — Admission and diagnostics

Deliverable: seven-day calibration, bootstrap thresholds and secret-free diagnostic snapshots.

Acceptance: outliers are bounded, thresholds activate only between runs, unsafe host metrics reject, Operator dashboard explains every decision.

### CAP-E01 — Dual-gateway experiment controller

Deliverable: ephemeral isolated LiteLLM and CLIProxyAPI test topology.

Acceptance: no production network/secret resolution, fixed CPU/RAM limits, run-local writes only, admission failure is fail-closed.

### CAP-E02 — Experiment lifecycle

Deliverable: run/attempt state machine, idle/keep-alive, hard stop, reactivation and parallelism controls.

Acceptance: all CAP-R052 through CAP-R056 state transitions and negative cases pass deterministic tests.

### CAP-E03 — Evidence package

Deliverable: Markdown report, canonical JSON manifest, SHA-256 and authenticated package endpoint.

Acceptance: traversal/symlink/external mounts fail; finalization is immutable; expired runs are destroyed; package contains no runtime credentials.

### CAP-E04 — Reproducibility suite

Deliverable: versioned fixtures, reset endpoints, Playwright and API integration tests for both gateway hops.

Acceptance: Zen/Ollama direct paths, CLIProxyAPI forwarding, affinity, rollover, degraded modes and security controls are covered by required PR CI.

### CAP-A01 — Pilot package preparation

Deliverable: exact OpenCode configuration, provider compliance checklist, test matrix, evidence template and rollback steps using placeholders.

Acceptance: OpenCode has exactly one provider endpoint; every model alias is explicit; runtime commands are marked Operator-only; no credentials or services change.

### CAP-A02 — Agent adoption preparation

Deliverable: Slarti/Lydia staged-adoption and rollback runbook.

Acceptance: pilot acceptance is prerequisite, each client has isolated key scope, failure returns to prior provider configuration, future workers remain out of scope.

### CAP-X01 — Operator host/deployment gate

Operator action: approve candidate artifacts, deploy without production credentials, measure Pi5/rechenknecht resources, choose host and record Go/No-Go.

### CAP-X02 — Operator provider/credential gate

Operator action: approve provider terms and exact auth methods, provision/rotate/revoke real credentials and explicitly enable only required callback ports.

### CAP-X03 — Operator OpenCode pilot gate

Operator action: deploy approved chain, configure OpenCode only to LiteLLM, execute pilot and attach sanitized runtime evidence and rollback result.

### CAP-X04 — Operator agent-adoption gate

Operator action: enable Slarti and Lydia only after CAP-X03 acceptance, verify isolated credentials and approve final production state.

## Issue #74 disposition

Issue #74 is superseded by CAP-B01, CAP-I01, CAP-A01, CAP-X01, CAP-X02 and CAP-X03 after PR #131 merges. Runtime obligations remain open in their Operator-gated issues; no runtime evidence is claimed by CAP-P01/P02.

## Regression debt

A regression receives `<origin-task>-RF<n>`, references the introducing task, broken task, causing PR/commit and evidence. Open regression debt blocks regular merges in the same functional area unless an independent reviewer or Operator grants a documented time-limited waiver: 14 days, then 7, then 3; no further waiver after that.
