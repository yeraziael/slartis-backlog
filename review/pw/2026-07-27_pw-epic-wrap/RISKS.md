# RISKS — Epic #253 Partial Wrap-up

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Audiobookshelf browser regressions in PW-I13–PW-I15 are undetected because the cited platform run failed and the service step was skipped. | Medium | High | Run both Playwright stages successfully at an exact source SHA before complete closeout. |
| Jellyfin browser regressions in PW-I19–PW-I21 are undetected because the cited CI stopped before Playwright execution. | High | High | Fix `check-scripts`, then execute and retain successful Jellyfin browser evidence. |
| Post-deployment behavior is unverified because Run #871 failed and Run #892 skipped the smoke job. | High | High | Produce a successful `main`-branch Post-Deployment Smoke run against the deployed target. |
| Merge status is mistaken for runtime verification. | Medium | High | Keep the per-ticket merge and verification states separate in `SUMMARY.md`. |

Runner isolation, sanitisation gates, and the zero-retry flake policy remain implemented controls, but they do not mitigate the missing execution evidence. See `docs/playwright-operations.md` for the operations runbook.
