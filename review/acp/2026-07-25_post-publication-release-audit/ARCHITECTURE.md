# Architecture - ACP Post-Publication Release Audit

## Decision

ADR-003 separates the implementation into two execution planes:

1. Credential-free deterministic fixtures run on every push and pull request.
2. A read-only authenticated workflow runs daily and by manual dispatch after
   the post-publication attestation asset exists.

The authenticated workflow does not use `release: published`. The attestation
can only be produced after the hosting-platform release exists, so a release
event can race ahead of the required asset upload.

## Binding Model

For every `vMAJOR.MINOR.PATCH` tag, the audit binds:

- annotated tag object ID;
- fully peeled commit;
- Gitea release tag and immutable full-SHA target;
- non-empty release notes and SHA-256;
- exact payload-asset set and SHA-256 hashes;
- pre-publication evidence path in the peeled commit;
- attestation timestamp after tag and release creation.

The attestation is a release asset but is excluded from its own `assets` list.
Runtime deployment and runtime version pins remain a separate state.

## Credential Boundary

The Actions repository secret is `ACP_RELEASE_AUDIT_TOKEN`. Gitea rejects names
using its reserved `GITEA_` prefix. The stored credential has only
`read:repository`; no raw value appears in Git, logs or this review package.
