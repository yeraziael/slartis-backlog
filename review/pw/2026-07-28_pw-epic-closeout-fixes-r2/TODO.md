# TODO - Playwright Epic Closeout Fixes Post-Merge Audit

## Runner Gate

- Complete `slarti/backlog#284` with Gitea administrator access.
- Remove or disable duplicate runner ID 3 without changing active runner ID 4.
- Rerun merge-SHA Unit Tests and record the successful runner ID, run ID, and job ID.

## Service Gate — Status (2026-07-29)

Operator gate `slarti/backlog#283` has been partially executed on the operator-approved current SHA `fd797dbbe191c5ed81d34628886d9bedd96ccb4c` (superseding the original merge SHA `11921fb...`). Verified evidence:

- [x] Deploy reachable HTTPS Jellyfin target under operator-approved hostname.
- [x] Provision synthetic Audiobookshelf and Jellyfin identities and controlled media/library data.
- [x] Provision the documented Gitea Actions secret names.
- [x] Run both main-branch service jobs at the current SHA `fd797db...`.
- [x] Run #978 success (5 jobs all success on runner ID 4).
- [x] Post-Deployment Audiobookshelf job #3634: smoke + upload-artifact success.
- [x] Post-Deployment Jellyfin job #3635: smoke + upload-artifact success.
- [x] Record run IDs, job IDs, source SHA, and artifact names — documented in this bundle's TESTING.md § Current Runtime Evidence.
- [ ] **Artifact manifest validation gap**: Gitea 1.26.4 REST API returns `total_count=0` for artifacts. The `action_artifact` database records and storage chunk integrity are not accessible through the public API on this instance. The `0 failed` is inferable from the jobs' `conclusion=success` (Playwright exits non-zero on failure). The `0 skipped` count **cannot be independently verified** without artifact content download, which is outside the credential-safe evidence scope. See TESTING.md § Current Runtime Evidence — Manifest Contents for the full analysis.

**Blocker**: The `zero failed / zero skipped` DoD element requires either:
- A Gitea version that exposes `action_artifact` metadata through the REST API (≥1.27 expected).
- Direct filesystem access to the Gitea data directory for `action_artifact` table queries and storage chunk integrity verification.
- An operator-approved artifact content download and inspection by a human reviewer.

## Known Limitations

- Gitea Run #906 verifies PR/platform CI only.
- Main Run #908 Unit Tests job #3290 fails on duplicate runner ID 3 before repository code; the rerun reproduces it.
- Main Run #908 service jobs #3292 and #3293 fail without operator prerequisites and produce no accepted runtime evidence.
- Epic #253 must not be described as fully runtime-closed while gates #283 or #284 remain open.
- Run #978 (SHA `fd797db...`) provides partial #283 evidence but the manifest-content verification gap remains unresolved.

## Review State

This bundle records a post-merge audit with additive current-runtime evidence for `slarti/backlog#283`. The service gate operator work is verified as executed but the manifest-content verification gap prevents full DoD closeout. Production closeout requires closing the artifact-content verification gap and runner gate #284.
