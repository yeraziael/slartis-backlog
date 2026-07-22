# [EPIC] Playwright Plan-as-Code implementation orchestration

| Field | Value |
|---|---|
| Gitea issue | `slarti/backlog#253` |
| Source URL | https://gitea.hl.maier.wtf/slarti/backlog/issues/253 |
| State | `open` |
| Labels | `Systemarchitektur`, `epic` |
| Updated | `2026-07-22T18:51:59+02:00` |

## Exact Ticket Contract

# Playwright Plan-as-Code implementation orchestration

## Authority And Baseline

- Planning authority: `yeraziael/slartis-backlog/docs/epics/playwright/` at reviewed baseline `5f2de959a4fb21b07405c7be65066b3093fb14af`.
- Current remote observation during decomposition: GitHub PR #82 contains the complete plan but is not yet on `main`; every implementation ticket therefore has a mandatory default-branch merge gate.
- Implementation authority: `Homelab/Architecture`, default-branch baseline `ed54f11` during decomposition.
- ACP authority: `Homelab/ACP` release `v0.1.0-draft`, current main `6b5e8ec58cde1e193b9310c01fc68b6885de8df5`. `SPEC/` remains empty; accepted Pilot 57 findings and `Homelab/Architecture/AGENTS.md` control evidence/review behavior without inventing a parallel ACP.
- This issue tracks execution. GitHub is reviewer communication only.

## Frozen Plan State

- Freeze identifier: `playwright-execution-plan-v1`.
- Independent review: `yeraziael/slartis-backlog#83`, review `4756629751`, reviewed head `274ad202a8319728fc610870c92a3a79d19c22b9`.
- State: `FROZEN_AWAITING_FINAL_REVIEW_AND_OPERATOR_APPROVAL`.
- No decision or implementation ticket may start until the operator explicitly approves execution.
- After approval, PW-D01 is the first executable ticket; PW-I01 remains blocked by PW-D01 and the canonical-plan default-branch merge gate.
- Any ticket-body, dependency, model, checkpoint, evidence, or reviewer-workflow change invalidates the freeze and requires a new SHA-bound review.

## Execution Status Index

Summary: FROZEN AWAITING FINAL REVIEW AND OPERATOR APPROVAL = all work. FIRST EXECUTABLE AFTER APPROVAL = PW-D01. IN PROGRESS = none. IN REVIEW = none. COMPLETED = none. CHECKPOINT = dormant.

| Key | Gitea | Status | Dependency gate |
|---|---|---|---|
| PW-D01 | [#254](https://gitea.hl.maier.wtf/slarti/backlog/issues/254) | FROZEN / FIRST AFTER APPROVAL | operator approval |
| PW-D02 | [#255](https://gitea.hl.maier.wtf/slarti/backlog/issues/255) | BLOCKED | PW-D01 |
| PW-I01 | [#256](https://gitea.hl.maier.wtf/slarti/backlog/issues/256) | BLOCKED | PW-D01 + plan merged to default branch |
| PW-I02 | [#257](https://gitea.hl.maier.wtf/slarti/backlog/issues/257) | BLOCKED | PW-I01 |
| PW-I03 | [#258](https://gitea.hl.maier.wtf/slarti/backlog/issues/258) | BLOCKED | PW-I02 + PW-D02 |
| PW-I04 | [#259](https://gitea.hl.maier.wtf/slarti/backlog/issues/259) | BLOCKED | PW-I03 + PW-D02 |
| PW-I05 | [#260](https://gitea.hl.maier.wtf/slarti/backlog/issues/260) | BLOCKED | PW-I04 |
| PW-ACP-CP1 | [#261](https://gitea.hl.maier.wtf/slarti/backlog/issues/261) | CHECKPOINT DORMANT | PW-I01..PW-I05 completed and independently reviewed |
| PW-D03 | [#262](https://gitea.hl.maier.wtf/slarti/backlog/issues/262) | BLOCKED | checkpoint release |
| PW-I06 | [#263](https://gitea.hl.maier.wtf/slarti/backlog/issues/263) | BLOCKED | checkpoint + PW-D03 + PW-I05 |
| PW-I07 | [#264](https://gitea.hl.maier.wtf/slarti/backlog/issues/264) | BLOCKED | PW-I06 + PW-D03 |
| PW-I08 | [#265](https://gitea.hl.maier.wtf/slarti/backlog/issues/265) | BLOCKED | PW-I07 |
| PW-D04 | [#266](https://gitea.hl.maier.wtf/slarti/backlog/issues/266) | BLOCKED | PW-I08 |
| PW-I09 | [#267](https://gitea.hl.maier.wtf/slarti/backlog/issues/267) | BLOCKED | PW-D04 + PW-I08 |
| PW-I10 | [#268](https://gitea.hl.maier.wtf/slarti/backlog/issues/268) | BLOCKED | PW-I09 + PW-I05 |
| PW-I11 | [#269](https://gitea.hl.maier.wtf/slarti/backlog/issues/269) | BLOCKED | PW-I10 + PW-I09 |
| PW-D05 | [#270](https://gitea.hl.maier.wtf/slarti/backlog/issues/270) | BLOCKED | PW-I11 |
| PW-I12 | [#271](https://gitea.hl.maier.wtf/slarti/backlog/issues/271) | BLOCKED | PW-D05 + PW-I10 + PW-I08 |
| PW-I13 | [#272](https://gitea.hl.maier.wtf/slarti/backlog/issues/272) | BLOCKED | PW-I12 + PW-I11 + provisioned identity |
| PW-I14 | [#273](https://gitea.hl.maier.wtf/slarti/backlog/issues/273) | BLOCKED | PW-I13 + controlled data |
| PW-I15 | [#274](https://gitea.hl.maier.wtf/slarti/backlog/issues/274) | BLOCKED | PW-I14 + three identities |
| PW-I16 | [#275](https://gitea.hl.maier.wtf/slarti/backlog/issues/275) | BLOCKED | PW-I15 |
| PW-I17 | [#276](https://gitea.hl.maier.wtf/slarti/backlog/issues/276) | BLOCKED | PW-I16 + PW-I15 |
| PW-I18 | [#277](https://gitea.hl.maier.wtf/slarti/backlog/issues/277) | BLOCKED | PW-I17 + operational evidence |
| PW-D06 | [#278](https://gitea.hl.maier.wtf/slarti/backlog/issues/278) | BLOCKED | PW-I17 + Jellyfin epic readiness |
| PW-I19 | [#279](https://gitea.hl.maier.wtf/slarti/backlog/issues/279) | BLOCKED | PW-D06 + PW-I17 |
| PW-I20 | [#280](https://gitea.hl.maier.wtf/slarti/backlog/issues/280) | BLOCKED | PW-I19 + provisioned identities |
| PW-I21 | [#281](https://gitea.hl.maier.wtf/slarti/backlog/issues/281) | BLOCKED | PW-I20 + controlled media |

## Dependency Order

`PW-D01 -> PW-D02/PW-I01 -> PW-I02 -> PW-I03 -> PW-I04 -> PW-I05 -> PW-ACP-CP1 -> PW-D03 -> PW-I06 -> PW-I07 -> PW-I08 -> PW-D04 -> PW-I09 -> PW-I10 -> PW-I11 -> PW-D05 -> PW-I12 -> PW-I13 -> PW-I14 -> PW-I15 -> PW-I16 -> PW-I17 -> PW-I18 and PW-D06 -> PW-I19 -> PW-I20 -> PW-I21`.

Decision tickets do not count toward the five implementation tickets. After PW-I05 is completed and independently reviewed, execution pauses before PW-I06 and the checkpoint becomes ACTIVE.

## Backlog And Requirement Mapping

| Canonical backlog item | Requirements | Internal execution tickets |
|---|---|---|
| PW-01 Runner | PWR-001..006, 010..013, 060..063 | PW-D01, PW-I01, PW-I02, PW-I03 |
| PW-02 Evidence | PWR-030..043, 050..052, 110..111 | PW-D02, PW-D03, PW-I04, PW-I06, PW-I07, PW-I08 |
| PW-03 Synthetic identities | PWR-020..025 | PW-D04, PW-I09 |
| PW-04 ABS unauth smoke | PWR-072..074, 090..093 | PW-D05, PW-I05, PW-I10, PW-I12 |
| PW-05 ABS OIDC | PWR-070..074 | PW-I11, PW-I13 |
| PW-06 ABS library/playback | PWR-080..082, 120..123 | PW-D05, PW-I14 |
| PW-07 ABS authorization | PWR-090..093 | PW-I15 |
| PW-08 CI/ACP handoff | PWR-100..103, 110..111 | PW-I16, PW-I17 |
| PW-09 Jellyfin | PWR-120..123 | PW-D06, PW-I19, PW-I20, PW-I21 |
| PW-10 Maintenance | M8 operations contract | PW-I18 |

Cross-cutting mapping: ACP evidence/findings apply to every ticket; Chromium-only MVP is PW-D01/PW-I01; failure classification is PW-I03/PW-I05; shared role/console fixtures are PW-I10; service onboarding is PW-D05/PW-D06.

## Model Allocation

- Sol high only: PW-D01, PW-D02, PW-D03, PW-D04, PW-D05, PW-D06 and PW-ACP-CP1 synthesis.
- Low-cost coding: PW-I01 through PW-I21, each one focused session and one PR. Any unresolved architecture question escalates to its Sol decision ticket or a new Sol-only ticket.

## Five-Ticket ACP Gate

- Count only PW-I01, PW-I02, PW-I03, PW-I04 and PW-I05.
- Require merge, complete ACP evidence and independent SHA-bound review for all five.
- Evaluate task quality, model choice, evidence, failure classification, retries, escalation and process friction.
- Verdict: `no change`, `clarification`, `backward-compatible refinement`, or `breaking revision`.
- No Playwright-specific rule enters ACP. Generic candidates require a separate versioned `Homelab/ACP` work item.

## GitHub Reviewer Communication Procedure

For each implementation PR, after the final internal Gitea evidence comment and transport validation, post one concise notification in the designated Playwright reviewer thread in `yeraziael/slartis-backlog` (PR #82 discussion until a successor thread is explicitly designated). Include:

1. Internal Gitea ticket reference.
2. Gitea implementation PR and exact head SHA.
3. Scope and changed-file summary.
4. Exact tests and required CI result/run IDs.
5. ACP evidence location.
6. Findings summary by category and whether any generic ACP candidate exists.

Do not copy ticket bodies, dependency maps or the full internal backlog to GitHub. Review verdicts are SHA-bound; a push requires a fresh notification and review.

## Status Maintenance

While frozen, no ticket state advances. After explicit operator approval, Slarti marks only PW-D01 READY. Thereafter exactly one next ticket becomes READY unless an explicitly reviewed independent decision permits parallel execution.
