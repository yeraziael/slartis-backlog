# Architecture - ACP Release-State Audit

## Release State Model

The change explicitly separates these states:

1. Implementation merged into the protected branch.
2. CI validated on the exact merge commit.
3. Immutable annotated Git tag created.
4. Gitea release published from that tag.
5. Runtime consumers pinned to the released tag and commit.

No earlier state implies a later state. In particular, a `-draft` value in
`VERSION` identifies a working line, not a published protocol release.

## External Dependency

The release gate deliberately blocks the first stable ACP release until
ai-governance defines a satisfiable evidence model. A release-prep commit cannot
contain its own final SHA while also being the commit named by an immutable tag.
The required policy decision is tracked by `yeraziael/ai-governance#42`.

## Runtime Boundary

The audit establishes that the installed `github-review` runtime skill matches
the governance source content, but records that this does not prove an ACP
release deployment. Runtime pinning remains a separate release gate.
