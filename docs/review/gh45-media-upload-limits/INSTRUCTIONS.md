# INSTRUCTIONS.md — GH-45 Media Upload Limits Review (revised, two-source-PR)

This PR transports the exact source diffs and evidence for GH-45 (Telegram
registration + homogeneous three-bridge stand) and the follow-up media-upload
limit fix, now bound to two real `Homelab/Architecture` source PRs.

Review `docs/review/gh45-media-upload-limits/CHANGES.diff` against the
accompanying root-cause, risk, and testing evidence.

## Bound source changes (exact)

- Gitea `Homelab/Architecture` **PR #52** (Synapse `max_upload_size: 100M`)
  - Base: 77d69f7f051f09d330b875fcf17263fc904f7443
  - Head: 4db6cec13229021cc099251cd6ea872b524a1ed9
  - Diff SHA-256: fc19abc8516b3b63c6f0b2590fec4cd737ad4a6903295cf14b35b9af5628cf0d
- Gitea `Homelab/Architecture` **PR #55** (frontproxy `client_max_body_size 100m`
  versioned + image digest pin)
  - Base: b208e7e5811f887ffc01d9b9ed7e73a8b42bfbd0
  - Head: 3126dce842fc03b194490dfd97963191fa8ef019
  - Merged: 0143129144abd3b60593ef759cc164c2d096baad
  - Diff SHA-256: 1759663132ac1981c46d7199497be0334e43453f3149886ad34cc36a29816daa

## Scope of this PR

Both the Synapse template addition AND the Matrix frontproxy body-size override
are versioned in `Homelab/Architecture` (PR #52 and PR #55 respectively). A host
rebuild from the repository therefore reproduces the working upload state. CWA
is excluded (separate scope).

## Gate

Approval records the config in the versioned `Homelab/Architecture` repository
(via PR #52 and PR #55). It does not authorize any new production recreation —
the changes are already deployed and verified live. If changes are requested, a
corrective source PR is required before merge into Architecture.

GH-45 is already operationally complete and closed; this PR only captures the
versioned record.
