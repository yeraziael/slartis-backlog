# INSTRUCTIONS.md — GH-45 Media Upload Limits Review (revised)

This PR transports the exact source diff and evidence for GH-45 (Telegram
registration + homogeneous three-bridge stand) and the follow-up media-upload
limit fix, now bound to a real `Homelab/Architecture` source PR.

Review `docs/review/gh45-media-upload-limits/CHANGES.diff` against the
accompanying root-cause, risk, and testing evidence.

## Bound source change

- Gitea `Homelab/Architecture` PR #52
  (fix/gh45-synapse-max-upload-size -> main)
- Base SHA: 77d69f7f051f09d330b875fcf17263fc904f7443
- Head SHA: 4db6cec13229021cc099251cd6ea872b524a1ed9
- Diff SHA-256: fc19abc8516b3b63c6f0b2590fec4cd737ad4a6903295cf14b35b9af5628cf0d
- Changed file: pi/synapse/synapse.yaml.example

## Scope of this PR

Only the Synapse `max_upload_size: 100M` template addition is versioned. The
frontproxy `client_max_body_size` companions are runtime-only (applied on Pi5,
outside Git per BRIDGE-OPERATIONS.md) and are recorded as evidence, not as
repository files. CWA is excluded (separate scope).

## Gate

Approval records the config in the versioned `Homelab/Architecture` repository
(via PR #52). It does not authorize any new production recreation — the changes
are already deployed and verified live. If changes are requested, a corrective
source PR is required before merge into Architecture.

GH-45 is already operationally complete and closed; this PR only captures the
versioned record.
