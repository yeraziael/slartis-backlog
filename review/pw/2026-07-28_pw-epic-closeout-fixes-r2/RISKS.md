# RISKS - Playwright Epic Closeout Fixes

| Area | Description | Likelihood | Impact | Mitigation |
|---|---|---|---|---|---|
| Architecture | Gitea runner mount layout could change and no mount may contain the repository path. | Low | High | Mount discovery fails closed before nested execution; bootstrap tests cover volume selection and reject broad inheritance. |
| Infrastructure | Duplicate global runner ID 3 shares the intended runner name and label but cannot execute the pinned Playwright image reliably. | High | High | Operator gate #284 removes the duplicate registration and requires a green merge-SHA Unit Tests rerun on runner ID 4. |
| Security | The CI job has Docker-socket access and can inspect the job container. | Existing | High | Nested containers import only the checkout mount; the browser is non-root and the checkout is read-only. |
| Security | The disposable results volume is mode `0777`. | Medium | Low | It contains test evidence only, is mounted only into ephemeral containers, uses a randomized name, and is removed by the exit trap. |
| Operations | Main-branch service jobs will fail until secrets, identities, media, and Jellyfin exist. | Certain | Medium | This is intentional fail-closed behavior; operator gate #283 defines prerequisites and evidence. |
| Compatibility | A future Gitea job may use a checkout layout that is not a mount ancestor. | Low | Medium | The runner emits a prerequisite error instead of falling back to a writable or invalid bind. |
| Maintainability | Generated workflow and Makefile could diverge from `ci-manifest.yaml`. | Low | Medium | Generator reproducibility and contract tests run in CI. |
| Evidence | A skipped authenticated test could be mistaken for production success. | Low | High | Post-deployment validation requires zero skipped and zero failed tests before artifact upload. |
| Evidence | Gitea 1.26.4 artifact REST API returns `total_count=0` despite successful uploads. | High | Medium | Manifest-content verification (0 failed/0 skipped) cannot be established through public API alone. Requires Gitea upgrade (≥1.27), filesystem access, or operator artifact download. |
| Runtime | Audiobookshelf or Jellyfin selectors may drift after application upgrades. | Medium | Medium | Service-specific suites, page objects, maintenance runbook, exact-SHA evidence, and separate job failures localize drift. |
| Migration | Operators must provision a larger explicit secret set. | Certain | Medium | Secret names and ownership are documented; values remain outside Git and review artifacts. |
| Rollback | Reverting the PR restores prior CI behavior but removes fail-closed service evidence and Gitea nested-Docker fixes. | Low | Medium | Revert the canonical PR commits as a unit; no persisted production data requires migration or rollback. |

## Residual Risk

PR-CI success proves repository and platform behavior on runner ID 4, not production service readiness or runner-fleet health.

Service gate `slarti/backlog#283` operator work is verified as executed (Run #978 success at SHA `fd797db...`, all 5 jobs green, both post-deployment smokes and artifact uploads successful). However, the manifest-content verification gap (`0 failed / 0 skipped` not independently provable through the Gitea 1.26.4 public API) prevents full DoD closeout. The `0 failed` is inferable with high confidence from job success (Playwright exits non-zero on failure). The `0 skipped` cannot be confirmed without artifact content inspection.

Residual risk remains open until runner gate #284 is resolved AND the manifest-content verification gap is closed (via Gitea upgrade, filesystem access, or operator artifact download).
