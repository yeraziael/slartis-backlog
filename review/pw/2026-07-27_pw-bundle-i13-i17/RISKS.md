# Risks — PW Bundle 2

## Architecture
- **Low.** Test file organization mirrors existing patterns. No new infrastructure.

## Security
- **Low.** Credentials loaded from env vars (`PW_E2E_ABS_USER`, `PW_E2E_ABS_PASSWORD`), never hardcoded or committed. Credential loader at `pi/audiobookshelf/scripts/load-playwright-credentials.sh` enforces `umask 077`.

## Operations
- **Medium.** Post-deployment smoke runs on main branch. If service tests fail after deployment, they block subsequent CI runs until resolved. Mitigation: `post-deploy` is a separate stage that can be skipped if needed.

## Migration
- **None.** No migration required.

## Compatibility
- **Low.** `test:platform` script now uses explicit dir args instead of `testDir: "."`. Tests in `platform/`, `evidence/`, `runner/` are all covered identically. No test was relying on `testDir: "."` scanning deeper than these directories.

## Maintainability
- **Low.** Page objects are self-contained. Adding a new service requires creating a new directory under `services/` — automatically included by `npm run test:service`.

## Rollback
- **Low.** All changes are additive (new files) or modifications to CI config. Reverting PR #106 restores previous state.
