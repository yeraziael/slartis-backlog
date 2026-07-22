# PW-D01 Independent Review Instructions

## Review Target

Review Gitea PR `Homelab/Architecture#78` at exact source head
`2683d9542b21eaa2d70907f4306a023460774ee1`.

The source PR adds one proposed architecture decision for the Playwright runner
and project bootstrap contract. It does not implement or execute Playwright.

## Governance

- Work item: `slarti/backlog#254` (`PW-D01`).
- Frozen plan: `playwright-execution-plan-v1`.
- Frozen-plan approval: `yeraziael/slartis-backlog#83`, review `4757129666`,
  exact approved head `d1379fbb065b0888e1615bce49205384b3f1a4ba`.
- Architecture base: `ed54f1144f1df21af13c9a2a1fd5c685fa2a95ac`.
- Authoritative evidence: `slarti/backlog#254`, comment `4228`.

## Review Questions

1. Does the source choose one official Playwright image with the correct
   platform-specific immutable digest and matching package version?
2. Are Node, npm, package-manager, lockfile, Chromium, paths, mounts, commands,
   architecture, upgrade, and rollback decisions complete enough for PW-I01 to
   execute without invention?
3. Is the two-phase runner coherent: secret-free registry access only during
   dependency installation, then network-none browser execution using the
   invoking UID/GID?
4. Are the Docker isolation controls internally compatible and sufficiently
   explicit for this controlled local-content platform scope?
5. Does the decision stay within its one-file documentation scope and avoid
   implementation, runtime, account, secret, DNS, and deployment mutation?
6. Do `CHANGES.diff`, `manifest.json`, `CI.json`, `TESTING.md`, and the PR body
   all bind to the same source head and CI runs?

## Required Verdict

Submit a native GitHub `APPROVED` or `CHANGES_REQUESTED` review against the
exact review-package PR head. State the reviewed source head
`2683d9542b21eaa2d70907f4306a023460774ee1` in the review body.

Approval authorizes merge of the source decision by Eddie or the Operator only.
It does not authorize PW-I01, deployment, runtime execution, secrets, accounts,
DNS changes, or any later Playwright ticket. PW-I01 also remains blocked until
the canonical planning PR `yeraziael/slartis-backlog#82` is merged.

Any source-head or review-package-head change invalidates the verdict and
requires a new review.
