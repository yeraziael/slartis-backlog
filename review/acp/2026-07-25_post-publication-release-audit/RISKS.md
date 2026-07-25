# Risks - ACP Post-Publication Release Audit

## Addressed

- **Self-reference:** the attestation cannot hash or list itself.
- **Moving release target:** stable releases require a full peeled commit SHA,
  not `main` or another branch.
- **Publication-event race:** daily/manual audit runs only after attestation
  upload; it does not run on release creation.
- **Credential exposure:** token scope is `read:repository`, the value exists
  only in a repository secret, and no command or artifact records it.
- **False deployment claim:** runtime state is explicitly outside audit scope.
- **Reserved secret prefix:** workflow and runbook use the verified valid name
  `ACP_RELEASE_AUDIT_TOKEN`.

## Residual

- No stable ACP release exists yet, so the first real stable attestation remains
  the production proving event for non-empty tag inventory.
- Gitea Actions and API behavior remain an infrastructure dependency; the daily
  rerun detects later drift but cannot prevent an operator from publishing an
  initially incomplete release.
- Token rotation is an operator process and must preserve the documented scope.
