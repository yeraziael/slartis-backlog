# CI and Release Gates

## Pull-request validation
- Validate Markdown links, Mermaid and YAML.
- Enforce stable ID uniqueness and required document presence.
- Scan for secrets, tokens, private host credentials and personal media metadata.
- Validate Compose syntax once runtime artifacts exist in Gitea.
- Verify image architecture and pinned version/digest policy.
- Scan images and approved plugins for known vulnerabilities.

## Deployment gates
1. Plan review approved.
2. NFS mount and fail-closed tests pass.
3. Keycloak claim/role tests pass.
4. Parent/child authorization matrix passes.
5. Representative client playback matrix passes.
6. Backup and restore evidence passes.
7. Rollback path is documented and tested.
8. No runtime secret is present in Git or CI artifacts.

## Evidence
Runtime evidence belongs with deployed architecture/execution records, not in planning prose. Evidence must identify version, host, date, test case and result without leaking private media inventory.

## Change control
Every implementation PR references #109 and one or more `JF-*` workstream IDs. A failed mandatory gate blocks deployment. Exceptions require an explicit ADR and operator approval.
