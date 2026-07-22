# Playwright Execution Plan Review

## Decomposition Summary

The internal control plane contains one parent index (`#253`), six Sol-only
decision tickets, twenty-one low-cost implementation tickets, and one mandatory
ACP checkpoint. Each implementation ticket is bounded to one focused session
and one Gitea pull request.

The plan is frozen as `playwright-execution-plan-v1`. No implementation work
has started, and no ticket is ready before final SHA-bound review and explicit
operator approval.

## Dependency Graph

```text
PW-D01 -> PW-D02
PW-D01 -> PW-I01 -> PW-I02
PW-D02 + PW-I02 -> PW-I03 -> PW-I04 -> PW-I05
PW-I01..PW-I05 -> PW-ACP-CP1
PW-ACP-CP1 -> PW-D03 -> PW-I06 -> PW-I07 -> PW-I08
PW-I08 -> PW-D04 -> PW-I09 -> PW-I10 -> PW-I11
PW-I11 -> PW-D05 -> PW-I12 -> PW-I13 -> PW-I14 -> PW-I15
PW-I15 -> PW-I16 -> PW-I17 -> PW-I18
PW-I17 + PW-D06 -> PW-I19 -> PW-I20 -> PW-I21
```

The detailed dependency field in every ticket remains authoritative if this
diagram and an issue contract ever differ.

## Execution Index

| Key | Gitea | Initial status | Recommended model | Dependencies |
|---|---:|---|---|---|
| PW-D01 | #254 | FROZEN / FIRST AFTER APPROVAL | Sol high | none |
| PW-D02 | #255 | BLOCKED | Sol high | PW-D01 |
| PW-I01 | #256 | BLOCKED | DeepSeek V4 Flash Free | PW-D01, plan merged to default branch |
| PW-I02 | #257 | BLOCKED | DeepSeek V4 Flash Free | PW-I01 |
| PW-I03 | #258 | BLOCKED | DeepSeek V4 Flash Free | PW-I02, PW-D02 |
| PW-I04 | #259 | BLOCKED | DeepSeek V4 Flash Free | PW-I03, PW-D02 |
| PW-I05 | #260 | BLOCKED | DeepSeek V4 Flash Free | PW-I04 |
| PW-ACP-CP1 | #261 | CHECKPOINT DORMANT | Sol high | PW-I01, PW-I02, PW-I03, PW-I04, PW-I05 |
| PW-D03 | #262 | BLOCKED | Sol high | PW-ACP-CP1 release |
| PW-I06 | #263 | BLOCKED | DeepSeek V4 Flash Free | PW-ACP-CP1, PW-D03, PW-I05 |
| PW-I07 | #264 | BLOCKED | DeepSeek V4 Flash Free | PW-I06, PW-D03 |
| PW-I08 | #265 | BLOCKED | DeepSeek V4 Flash Free | PW-I07 |
| PW-D04 | #266 | BLOCKED | Sol high | PW-I08 |
| PW-I09 | #267 | BLOCKED | DeepSeek V4 Flash Free | PW-D04, PW-I08 |
| PW-I10 | #268 | BLOCKED | DeepSeek V4 Flash Free | PW-I09, PW-I05 |
| PW-I11 | #269 | BLOCKED | DeepSeek V4 Flash Free | PW-I10, PW-I09 |
| PW-D05 | #270 | BLOCKED | Sol high | PW-I11 |
| PW-I12 | #271 | BLOCKED | DeepSeek V4 Flash Free | PW-D05, PW-I10, PW-I08 |
| PW-I13 | #272 | BLOCKED | DeepSeek V4 Flash Free | PW-I12, PW-I11, synthetic identity provisioned |
| PW-I14 | #273 | BLOCKED | DeepSeek V4 Flash Free | PW-I13, controlled test data |
| PW-I15 | #274 | BLOCKED | DeepSeek V4 Flash Free | PW-I14, three synthetic identities |
| PW-I16 | #275 | BLOCKED | DeepSeek V4 Flash Free | PW-I15 |
| PW-I17 | #276 | BLOCKED | DeepSeek V4 Flash Free | PW-I16, PW-I15 |
| PW-I18 | #277 | BLOCKED | DeepSeek V4 Flash Free | PW-I17, post-deployment evidence |
| PW-D06 | #278 | BLOCKED | Sol high | PW-I17, Jellyfin epic readiness |
| PW-I19 | #279 | BLOCKED | DeepSeek V4 Flash Free | PW-D06, PW-I17 |
| PW-I20 | #280 | BLOCKED | DeepSeek V4 Flash Free | PW-I19, Jellyfin identities provisioned |
| PW-I21 | #281 | BLOCKED | DeepSeek V4 Flash Free | PW-I20, controlled Jellyfin media |

## Ordering Rationale

1. Resolve immutable runner and provenance contracts before code.
2. Establish a deterministic, service-independent platform core.
3. Stop after exactly five implementation tickets for an ACP quality review.
4. Add artifact security before any authenticated evidence can be published.
5. Establish synthetic identity and shared fixture contracts before service flows.
6. Prove Audiobookshelf before adding CI/deployment gates.
7. Adopt Jellyfin only after the platform has demonstrated reuse and evidence handoff.

## First Five Implementation Tickets

| Ticket | Gitea | Scope | Recommended model |
|---|---:|---|---|
| PW-I01 | #256 | Runner/package bootstrap and static contract | DeepSeek V4 Flash Free |
| PW-I02 | #257 | Controlled Chromium self-test and context isolation | DeepSeek V4 Flash Free |
| PW-I03 | #258 | Deterministic result/exit-code semantics | DeepSeek V4 Flash Free |
| PW-I04 | #259 | Evidence manifest schema and generator | DeepSeek V4 Flash Free |
| PW-I05 | #260 | Prerequisite classification and fail-closed gate | DeepSeek V4 Flash Free |

These five are intentionally deterministic and service-independent. Their
contracts include exact paths, tests, CI evidence, rollback, findings taxonomy,
and escalation conditions suitable for low-cost execution.

## Sol-Only Decisions

| Ticket | Gitea | Why Sol is required |
|---|---:|---|
| PW-D01 | #254 | Selects immutable image, package manager, versions and invocation contract before bootstrap code. |
| PW-D02 | #255 | Defines trusted provenance sources and mixed-result precedence before evidence implementation. |
| PW-D03 | #262 | Resolves trace sanitisation feasibility and Gitea retention mechanics before artifact publication. |
| PW-D04 | #266 | Fixes realm, role membership and password handoff boundaries before provisioning code. |
| PW-D05 | #270 | Pins Audiobookshelf journeys, selectors and controlled data so service executors do not explore live UI architecture. |
| PW-D06 | #278 | Confirms Jellyfin readiness, identities, selectors and controlled media before second-service adoption. |

## ACP Checkpoint

`PW-ACP-CP1` (`#261`) activates only after PW-I01
through PW-I05 are merged and independently reviewed at exact head SHAs. It
blocks every PW-I06-or-later branch, edit, delegation, or retry until the
checkpoint records `release`.

The checkpoint evaluates task self-containment, model selection, evidence,
failure classification, retries, escalation, and process friction. Its ACP
disposition is exactly one of `no change`, `clarification`,
`backward-compatible refinement`, or `breaking revision`. Playwright-specific
findings remain domain records; only broadly reusable agent-engineering findings
may become separate ACP refinement candidates.

## Plan-To-Ticket Mapping

| Canonical backlog item | Requirements | Execution tickets |
|---|---|---|
| PW-01 Runner | PWR-001..006, PWR-010..013, PWR-060..063 | PW-D01, PW-I01, PW-I02, PW-I03 |
| PW-02 Evidence | PWR-030..043, PWR-050..052, PWR-110..111 | PW-D02, PW-D03, PW-I04, PW-I06, PW-I07, PW-I08 |
| PW-03 Synthetic identities | PWR-020..025 | PW-D04, PW-I09 |
| PW-04 ABS unauthenticated smoke | PWR-072..074, PWR-090..093 | PW-D05, PW-I05, PW-I10, PW-I12 |
| PW-05 ABS OIDC | PWR-070..074 | PW-I11, PW-I13 |
| PW-06 ABS library/playback | PWR-080..082, PWR-120..123 | PW-D05, PW-I14 |
| PW-07 ABS authorization | PWR-090..093 | PW-I15 |
| PW-08 CI/ACP handoff | PWR-100..103, PWR-110..111 | PW-I16, PW-I17 |
| PW-09 Jellyfin | PWR-120..123 | PW-D06, PW-I19, PW-I20, PW-I21 |
| PW-10 Maintenance | M8 operations contract | PW-I18 |

Cross-cutting requirements: ACP evidence/findings apply to every ticket;
Chromium-only MVP is PW-D01/PW-I01; failure classification is PW-I03/PW-I05;
shared role and console fixtures are PW-I10; service onboarding contracts are
PW-D05 and PW-D06.

## Reviewer Workflow

1. Review this package and exact ticket snapshots, not the Gitea issue list alone.
2. Check each ticket for self-contained scope, non-goals, allowed paths, tests,
   CI, ACP evidence, findings, rollback, dependencies, model and escalation.
3. Record review on this GitHub PR against the exact head SHA.
4. Request changes for any ambiguous architecture delegated to a low-cost model.
5. Approval authorizes ticket execution planning only. It does not authorize
   implementation, merge, deployment, secrets, accounts or runtime mutation.
6. During execution, each Gitea PR receives one concise GitHub reviewer
   notification with internal ticket, PR/head SHA, scope, tests/CI, ACP evidence
   location and findings summary. The full backlog is not duplicated again.
7. Implementation review prioritises contract compliance, model routing, ACP
   checkpoint quality, and evidence generation. Playwright-specific details are
   reviewed only where they affect the authoritative requirement or security
   contract.

## Assumptions

- Gitea `slarti/backlog` remains the execution tracker.
- `Homelab/Architecture` keeps `ci-manifest.yaml` as CI source of truth.
- The official Playwright container can run ephemerally on rechenknecht; PW-D01
  must verify image architecture and immutable digest before implementation.
- Existing Audiobookshelf OIDC authority remains compatible with synthetic users;
  PW-D04 verifies the exact provisioning and handoff contract.
- ACP `v0.1.0-draft` has no normative `SPEC/`; accepted Pilot 57 findings and
  repository instructions are used without claiming a new ACP specification.

## Open Questions

- Playwright plan PR #82 is still open and must reach the default branch before PW-I01.
- Exact runner image digest/package contract: PW-D01.
- Trusted evidence provenance/result precedence: PW-D02.
- Safe trace sanitisation and enforceable retention: PW-D03.
- Synthetic identity/password handoff: PW-D04.
- Audiobookshelf selectors and controlled test data readiness: PW-D05.
- Jellyfin epic, OIDC and controlled media readiness: PW-D06.
