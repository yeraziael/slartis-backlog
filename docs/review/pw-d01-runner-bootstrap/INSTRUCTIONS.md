# PW-D01 Independent Review Instructions

## Review Target

Review corrective Gitea PR `Homelab/Architecture#79` at exact source head
`5e4e566ab143f3e1a3f9b6a7bbd8b5798dc1bacb`.

The prior source PR `#78` was merged by policy before independent review. The
decision remained explicitly `Proposed`; corrective PR `#79` resolves the final
self-audit findings and is WIP to prevent another premature merge. It changes
only the decision and does not implement or execute Playwright.

`CHANGES.diff` presents the complete effective PW-D01 decision from the
pre-decision Architecture base through the corrective head, not only the
correction delta. The Gitea PR itself provides the correction-only diff.

## Governance

- Work item: `slarti/backlog#254` (`PW-D01`).
- Frozen plan: `playwright-execution-plan-v1`.
- Frozen-plan approval: `yeraziael/slartis-backlog#83`, review `4757129666`,
  exact approved head `d1379fbb065b0888e1615bce49205384b3f1a4ba`.
- Corrective base: `3180722ba546dfd9d5434b4d3d71d32eb82ebd43`.
- Effective review base: `ed54f1144f1df21af13c9a2a1fd5c685fa2a95ac`.
- Authoritative evidence: `slarti/backlog#254`, comment `4240`.

## Review Questions

1. Can PW-I01 execute literally without choosing a script, test input, lock
   policy, discovery rule, Docker argument, security boundary, or lifecycle?
2. Do the official image, platform digest, Node/npm, package integrity,
   Chromium revision, and all command occurrences agree?
3. Are general dependency egress, network-none tests, private shared memory,
   mounts, capabilities, non-root UID/GID, read-only state, tmpfs, environment,
   and cleanup assumptions accurate and non-contradictory?
4. Are every deferred seam and the narrow implementation freedom explicit,
   with no hidden architecture choice left in later sections?
5. Is upgrade/rollback atomic across every version-coupled file and verifiable
   against an available prior digest?
6. Is every normative requirement observable through PW-I01 tests or external
   change-control evidence?
7. Does the decision fix only architecture interfaces rather than writing the
   later implementation?
8. Do all package artifacts bind to source PR `#79`, exact corrective head, CI
   runs `661`/`662`, and evidence comment `4240`?

## Required Verdict

Submit a native GitHub `APPROVED` or `CHANGES_REQUESTED` review against the
exact review-package PR head. State the reviewed source head
`5e4e566ab143f3e1a3f9b6a7bbd8b5798dc1bacb` in the review body.

Approval authorizes removing WIP and merging corrective source PR `#79` by Eddie
or the Operator only.
It does not authorize PW-I01, deployment, runtime execution, secrets, accounts,
DNS changes, or any later Playwright ticket. PW-I01 also remains blocked until
the canonical planning PR `yeraziael/slartis-backlog#82` is merged.

Any source-head or review-package-head change invalidates the verdict and
requires a new review.
