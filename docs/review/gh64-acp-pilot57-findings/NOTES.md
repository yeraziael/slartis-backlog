# GH-64 Scope And Risks

## Delivered

- `FINDINGS/README.md` — index, workflow, register table
- `FINDINGS/TEMPLATE.md` — reusable template for future pilots
- `FINDINGS/PILOT-57.md` — canonical findings F-57-001 through F-57-007
- `DECISIONS/README.md` — ADR-ready directory (empty register)
- `README.md` — updated to list new directories
- `CHANGELOG.md` — updated with findings bootstrap entry

## Not Performed

- No changes to ACP specification (SPEC/ remains `.gitkeep`)
- No schema changes
- No version bump
- No release
- No conformance test changes
- No runtime or deployment mutations

## Review Risks

- The ACP spec is still empty — this PR establishes the findings workflow
  before the protocol is fully written. Findings from this pilot will directly
  inform which ACP sections need to be drafted first.
- Severity ratings removed from canonical findings per review (PR #4).
- TEMPLATE.md aligned with category taxonomy (ACP/Prompt/Reviewer/Process).
- SHA-256 of CHANGES.diff: `4d1fbc349af7ca44d82f8689d8a8363a18145c9f0e8ef41bd38df31f71bc5207`
