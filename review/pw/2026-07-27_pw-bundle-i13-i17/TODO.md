# TODO — PW Bundle 2

## Open Items
- None. All 5 issues (PW-I13 through PW-I17) are fully implemented in this PR.

## Follow-Up Issues
- Fix pre-existing `__dirname` ESM issue in playwright platform tests (`sanitisation-spec.spec.ts`, `prerequisite-classification.spec.ts`) — requires converting `__dirname` to `import.meta.url` equivalents
- PW-I06 (evidence schema evolution) and PW-I07 (CI reports) — planned as next bundle

## Technical Debt
- Service test environment variables not documented in runbook (credential env vars are documented in `docs/audiobookshelf-oidc-verification.md`)

## Limitations
- Service tests require live credentials and a running Audiobookshelf instance — cannot execute in CI without external secrets
- Post-deploy stage is only active on main branch per `branch_rules`

## Decisions Still Required
- None for this bundle. All implementation decisions documented in respective issues.

## Items Deferred
- Runner: `service` mode with prereq checks (already exists as `service:<base-url>`)
- Runner: dynamic service name in forced manifest (always `playwright-platform` for forced outcomes — acceptable for error reporting)
