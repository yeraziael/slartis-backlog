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
- All 7 canonical findings (F-57-001 through F-57-007) have been transferred
  to Homelab/ACP main at `cdc4007` (PRs #2 and #3).
- SHA-256 of CHANGES.diff: `f09af0bee4e7248eff0b0425afb33e6e4dd5f9791bc0ba1e60f7b6fdf6df849c`
