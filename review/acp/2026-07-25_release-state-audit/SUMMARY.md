# Summary - ACP Release-State Audit

## Problem

ACP v0.2 and v0.3 were merged but never published as stable releases. The
canonical repository had no documented release gate, and its latest CI failure
was caused by an unpinned runtime dependency installation plus an overly broad
documentation-secret false positive.

## Goal

Make ACP's release state auditable, document the distinction between a merged
draft and a published release, and restore deterministic CI validation.

## Scope

- Post-merge review of `Homelab/ACP` PR #12, merged as `b65a9ad`.
- Release-state inventory, cross-system gap analysis, and v0.3.0 recommendation.
- ACP release gate documentation.
- CI dependency and documented-placeholder scanner fixes.

## Not In Scope

- Creating or moving ACP tags or Gitea releases.
- Publishing ACP v0.2 or v0.3.
- Resolving the canonical governance evidence-binding policy.
- Adding the credential-dependent post-publication release audit.

## Canonical References

- Canonical repository: `Homelab/ACP`
- Canonical PR: #12, `docs: audit ACP release state`
- Triggering follow-up: `Homelab/ACP#11`
- Policy dependency: `yeraziael/ai-governance#42`
