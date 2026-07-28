# TODO - Playwright Epic Closeout Fixes Post-Merge Audit

## Runner Gate

- Complete `slarti/backlog#284` with Gitea administrator access.
- Remove or disable duplicate runner ID 3 without changing active runner ID 4.
- Rerun merge-SHA Unit Tests and record the successful runner ID, run ID, and job ID.

## Service Gate

- Complete operator gate `slarti/backlog#283` without placing secret values in issues, logs, commits, or artifacts.
- Deploy a reachable HTTPS Jellyfin target under an operator-approved hostname.
- Provision synthetic Audiobookshelf and Jellyfin identities and controlled media/library data.
- Provision the documented Gitea Actions secret names.
- Run both main-branch service jobs at the exact merged Architecture SHA.
- Verify artifacts `playwright-audiobookshelf-evidence` and `playwright-jellyfin-evidence`.
- Require each schema-valid manifest to report zero failed and zero skipped tests.
- Record the run IDs, job IDs, source SHA, and artifact names in a final closeout review.

## Known Limitations

- Gitea Run #906 verifies PR/platform CI only.
- Main Run #908 Unit Tests job #3290 fails on duplicate runner ID 3 before repository code; the rerun reproduces it.
- Main Run #908 service jobs #3292 and #3293 fail without operator prerequisites and produce no accepted runtime evidence.
- Epic #253 must not be described as fully runtime-closed while gates #283 or #284 remain open.

## Review State

This bundle records a post-merge audit. Production closeout requires both operator gates and an independent review of the resulting exact-SHA evidence.
