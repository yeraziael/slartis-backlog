# [PW-ACP-CP1] Mandatory ACP checkpoint after five implementation tickets

| Field | Value |
|---|---|
| Gitea issue | `slarti/backlog#261` |
| Source URL | https://gitea.hl.maier.wtf/slarti/backlog/issues/261 |
| State | `open` |
| Labels | `Systemarchitektur`, `sub-task` |
| Updated | `2026-07-22T18:24:50+02:00` |

## Exact Ticket Contract

Parent: #253

## Objective

Pause all Playwright execution after exactly five implementation tickets and evaluate the ACP pilot before PW-I06 or any later work begins.

## Authoritative Source Paths

- `yeraziael/slartis-backlog@5f2de959a4fb21b07405c7be65066b3093fb14af:docs/epics/playwright/` (planning baseline; verify the same documents are on the default branch before implementation)
- `Homelab/ACP@6b5e8ec58cde1e193b9310c01fc68b6885de8df5` / release `v0.1.0-draft`: `README.md`, `FINDINGS/PILOT-57.md`, `FINDINGS/TEMPLATE.md`
- `Homelab/Architecture/AGENTS.md` at the executor's base commit
- Internal tickets and independently reviewed PR/evidence for PW-I01 #256, PW-I02 #257, PW-I03 #258, PW-I04 #259, PW-I05 #260.

## In Scope

- Evaluate task self-containment, model selection, evidence sufficiency, failure classification, retries, escalation behavior and process friction across PW-I01 through PW-I05.
- Classify ACP disposition as exactly one of: `no change`, `clarification`, `backward-compatible refinement`, `breaking revision`.
- Produce a SHA-bound independent checkpoint verdict and an explicit release/hold decision for PW-I06.

## Explicit Non-Goals

- No Playwright implementation, retry of a child ticket, ACP edit, deployment or ticket-six preparation.
- No Playwright-specific rule may be added to ACP.

## Prerequisites

- All five implementation tickets PW-I01 through PW-I05 are merged and independently reviewed at exact head SHAs.
- Their final Gitea evidence comments and findings records are complete.

## Permitted Files Or Repository Areas

- Internal Gitea ticket comments only for checkpoint analysis and verdict.
- If a generic ACP change is approved, create a separate future `Homelab/ACP` issue/PR; do not modify ACP in this checkpoint.

## Normative Implementation Contract

- Activate only after the fifth implementation ticket completes; decision tickets do not count.
- No PW-I06-or-later branch, edit, delegation or retry may begin until this checkpoint records `release`.
- Distinguish task-contract ambiguity, missing prerequisite, implementation defect, test defect, infrastructure failure, evidence deficiency, model limitation, process friction, generic ACP candidate and domain-specific learning.
- Only broadly reusable agent-engineering findings may be generic ACP candidates.

## Acceptance Criteria

- Each of the seven evaluation dimensions has evidence and a verdict.
- Retry/escalation history is reconstructed from issue journals rather than worker summaries.
- ACP disposition and ticket-six release/hold decision are explicit.

## Required Tests

- Verify all five PR head SHAs, changed-file lists, required CI runs, independent verdicts and merge commits.
- Verify every acceptance criterion in each ticket has mapped evidence.

## Required CI Validation

- No new CI run is required for this control-plane ticket; all five source PR CI runs MUST be independently verified and green.

## ACP Phase Transitions

- `DORMANT -> ACTIVE` only after PW-I05 completion and review.
- `ACTIVE -> IN_REVIEW` after checkpoint evidence table is complete.
- `IN_REVIEW -> RELEASED` permits PW-I06; `IN_REVIEW -> HOLD` keeps all later tickets blocked.
- Any ACP change proposal is a separate work item and does not silently alter this pilot's pinned contract.

## Required ACP Evidence

- Five-ticket matrix: contract completeness, model, retries, failures, evidence, reviewer verdict and merge SHA.
- Aggregate findings by all ten required categories and preserve links to source tickets.
- Independent reviewer checkpoint verdict bound to this ticket's final analysis revision.

## Required Findings Record

Record findings in the internal Gitea ticket work journal and summarise them in the implementation PR. Use every category below, writing `none observed` when empty:

- `contract ambiguity`
- `missing prerequisite`
- `implementation defect`
- `test defect`
- `infrastructure failure`
- `evidence deficiency`
- `model limitation`
- `process friction`
- `generic ACP candidate`
- `domain-specific learning`

Unresolved contract ambiguity, missing prerequisite, implementation defect, test defect, infrastructure failure, evidence deficiency, or model limitation blocks completion. Process friction blocks only when it prevents contract or evidence compliance. Generic ACP candidates are copied to the five-ticket checkpoint, not directly encoded in ACP. Playwright-specific learning remains in this ticket, its PR, or the canonical Playwright plan and MUST NOT be added to ACP.

## Rollback Expectations

- A mistaken `release` is reverted by a `hold` comment before PW-I06 starts; if PW-I06 has started, stop it without merging and record process friction.
- ACP changes, if approved, use their own versioned PR and release rollback.

## Definition Of Done

- Checkpoint disposition and release/hold decision are recorded and independently reviewed.
- Parent execution index is updated; PW-I06 alone may become ready on release.

## Dependencies

- PW-I01 #256, PW-I02 #257, PW-I03 #258, PW-I04 #259, PW-I05 #260.

## Recommended Model

Sol high only for synthesis; independent reviewer supplies the checkpoint verdict.

## Escalation Conditions

- Any of five PRs lacks SHA-bound independent review or acceptance evidence.
- Findings indicate a breaking ACP revision or repeated model capability failure.
- Failure classification or retry history cannot be reconstructed.
