# Summary - ACP Post-Publication Release Audit

## Problem

ACP had no machine-enforced binding between stable annotated tags and Gitea
releases. The canonical release policy's earlier evidence shape was
self-referential, no least-privilege credential was provisioned, and the audit
requirements in `RELEASE.md` were documentation only.

## Goal

Implement `Homelab/ACP#11` against the two-stage evidence model approved in
`yeraziael/ai-governance#42`: deterministic pull-request tests plus a read-only
post-publication audit of Git objects, Gitea release metadata, notes, assets,
pre-publication evidence and attestation ordering.

## Scope

- Canonical ACP PR #13, merged as `08fa86810c0794088180c2f671a61f9061dc005f`.
- Corrective ACP PR #14, merged as `fab8a749174f126648ea86a78ee3e78750c68321`.
- Review-scan correction PR #15, merged as
  `38baaf19568766e3911f63edd1509c8997030eab`.
- Thirteen deterministic conformance scenarios.
- Scheduled/manual Gitea Actions workflow.
- Least-privilege token and repository-secret provisioning.
- ADR-003 and operator runbook.
- Manual workflow dispatch 703 on final `main`.

## Not In Scope

- Creating or moving an ACP tag.
- Publishing or changing a Gitea release or release asset.
- Declaring any runtime consumer deployed or version-pinned.
- Publishing ACP v0.3.0.

## Canonical References

- Canonical repository: `Homelab/ACP`
- Issue: `Homelab/ACP#11`
- Source PRs: `Homelab/ACP#13`, `Homelab/ACP#14`, `Homelab/ACP#15`
- Final source commit: `38baaf19568766e3911f63edd1509c8997030eab`
- Governance dependency: `yeraziael/ai-governance#42`, PR #43
- Superseded review package: GitHub PR #93
