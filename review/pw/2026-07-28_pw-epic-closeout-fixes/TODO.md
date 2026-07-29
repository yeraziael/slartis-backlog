# TODO - Playwright Epic Closeout Fixes

## Before Canonical Merge

- Obtain an independent review of this SHA-bound bundle.
- Route any blocking or major findings back to `Homelab/Architecture#109`.
- Regenerate the bundle if canonical PR #109 head changes.

## After Canonical Merge

- Synchronize the canonical Architecture `main` checkout immediately after merge.
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
- Post-deployment jobs #3282 and #3283 were skipped in feature-branch context and are not runtime evidence.
- Epic #253 must not be described as fully runtime-closed while operator gate #283 remains open.

## Review State

This bundle records self-verification only. Canonical merge and production closeout require independent review and the separate operator runtime evidence.
