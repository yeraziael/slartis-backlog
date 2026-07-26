# Playwright Execution Plan v2 Amendment

## Purpose

This amendment updates the execution governance of
`playwright-execution-plan-v1` without changing ticket scope, dependencies,
permitted files, acceptance criteria, tests, rollback contracts, finding
categories, or the Flash-Free suitability classification of PW-I01 through
PW-I21.

The amendment becomes active only after a new independent SHA-bound review of
the complete v2 package. Until then PW-D02 and every later ticket remain
blocked.

## Current Facts

- Planning PR #82 is merged as
  `7ae8e1cd468f4f9543f5c3e2ccdd0df05ba68b2b`.
- Frozen-plan PR #83 is merged as
  `22aeef5ed411a8893cd3c4e3f923196417f11ffc`.
- PW-D01 review PR #84 is merged as
  `07b40294786388e7a6498b39e52c354b29838626`.
- PW-D01 is complete in `Homelab/Architecture` at merge
  `a3b926bc16c6835eb0ae1ca8a9ca087ee5b4583d`.
- PW-D02 is the next ticket in the unchanged serial execution order.
- ACP review provenance is pinned to stable `v0.3.0`, peeled commit
  `7768e129b3fdc48ebf69ebd888225d2c37af0c71`.

## Operator Authorization

On 2026-07-26 the Operator authorized Slarti to execute the complete Playwright
epic, perform its reviews, and merge its exact reviewed heads. The Operator
also explicitly authorized Sol for PW-D02 through PW-D06, PW-ACP-CP1,
Playwright architecture, reviews, and orchestration. No subagents are
authorized or used; execution remains serial.

This standing authorization supplies merge authority. It does not transform a
self-verification into an independent review and does not authorize production
deployment, secrets, accounts, DNS, or service mutation outside a ticket's
separately satisfied operator and deployment gates.

No Gitea ticket body is changed before v2 activation. The v1 ticket snapshot is
therefore retained byte-for-byte with the same canonical hash. This amendment
is the sole superseding authority layer; after activation, each child issue
receives a comment referencing the reviewed amendment before execution starts;
the frozen ticket bodies remain unchanged.

## Superseded Reviewer Workflow

For PW-D02 through PW-D06, PW-I01 through PW-I21, and PW-ACP-CP1, the following
v1 clauses are superseded wherever they appear in the frozen ticket snapshot:

| v1 clause | v2 replacement |
|---|---|
| Independent reviewer accepts the exact PR head. | Slarti records an ACP v0.3 `self-verification` bound to the exact PR head with verdict `consistency-verified`. |
| Review approval supplies merge authority. | Self-verification supplies no approval authority; the Operator's standing epic authorization supplies merge authority. |
| Eddie/operator performs every merge. | Slarti may merge the exact self-verified head after all gates below pass. |
| GitHub notification is a blocking independent-review handoff. | GitHub notification is an optional audit mirror; Gitea remains authoritative for execution and evidence. |
| PW-ACP-CP1 requires independent verdicts for PW-I01 through PW-I05. | PW-ACP-CP1 requires exact-head self-verifications, green CI, merge commits, and complete evidence for PW-I01 through PW-I05. |

## Mandatory Self-Verification Gate

Before each merge, all of the following are blocking:

1. The ticket's dependencies and source gates are satisfied.
2. The actual changed files equal the permitted scope.
3. Every required local test and required CI job is successful at the exact PR
   head; an absent job is not a pass.
4. The final Gitea evidence comment contains every required field and all ten
   finding categories.
5. No unresolved blocking finding remains.
6. Slarti posts a structured ACP verdict using
   `schema: acp.review-verdict.v2`, `review_type: self-verification`,
   `review_basis: pull-request`, and `verdict: consistency-verified`.
7. The verdict includes the mandatory disclaimer that self-verification is not
   independent review and carries no external quality authority.
8. The verdict's `reviewed_commit` equals the current full PR head SHA. Any push
   invalidates it and requires a new self-verification.
9. Merge uses the exact verified head and is followed by merged-main CI and
   post-merge state verification where the ticket requires them.

Self-verification must never use `approved`, `approval`, or an independent
review type. A merge is authorized by the Operator's standing instruction, not
by the verdict.

## Unchanged Invariants

- The dependency graph and serial order are unchanged.
- No parallel branch starts unless a later reviewed amendment changes the
  graph.
- PW-I01 through PW-I21 remain bounded implementation tickets. They may not
  invent architecture and must stop on ambiguity.
- PW-D02 through PW-D06 and PW-ACP-CP1 remain Sol architecture/synthesis work.
- PW-ACP-CP1 remains a hard gate before PW-I06.
- Gitea remains the execution authority; GitHub remains an audit and planning
  surface.
- Runtime, deployment, account, secret, DNS, and production actions retain
  their existing separate gates.

## Activation

The v2 amendment is active only when a native independent review binds the
final amendment PR head and the PR is merged unchanged. The Gitea parent issue
must then record the v2 freeze identifier and mark only PW-D02 ready.
