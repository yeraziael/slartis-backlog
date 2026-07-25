# Follow-Ups - ACP Post-Publication Release Audit

## Required At First Stable Release

- Commit pre-publication evidence in the release-preparation commit.
- Publish the stable annotated tag and Gitea release with a full-SHA target.
- Upload payload assets and `release-attestation.yaml`.
- Manually dispatch the post-publication audit and retain the successful run ID.
- Record runtime-consumer pins separately from publication evidence.

## Operations

- Rotate `ACP_RELEASE_AUDIT_TOKEN` according to the runbook without adding
  write scopes.
- Investigate any scheduled-run failure before treating a release as conformant.

No implementation blocker remains for `Homelab/ACP#11`.
