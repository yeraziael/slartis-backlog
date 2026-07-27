# Risks — PW Bundle 2

## Architecture
- **Low.** Test file organization mirrors existing patterns. No new infrastructure.

## Security
- **Low.** Credentials loaded from env vars (`PW_E2E_ABS_USER`, `PW_E2E_ABS_PASSWORD`), never hardcoded or committed. Credential loader at `pi/audiobookshelf/scripts/load-playwright-credentials.sh` enforces `umask 077`.

## Operations
- **Low.** Post-deployment smoke runs only on main branch (`if: github.ref == 'refs/heads/main'`). Fails closed when `CI=true` and no URL is provided.

## Migration
- **None.** No migration required.

## Compatibility
- **Low.** `test:platform` script now uses explicit dir args instead of `testDir: "."`. Tests in `platform/`, `evidence/`, `runner/` are all covered identically. No test was relying on `testDir: "."` scanning deeper than these directories.

## Maintainability
- **Low.** Page objects are self-contained. Adding a new service requires creating a new directory under `services/` — automatically included by `npm run test:service`.

## Rollback
- **Low.** All changes are additive (new files) or modifications to CI config. Reverting PR #106 restores previous state.
