# Decision Log

- **CAP-D001 — Single gateway:** OpenCode uses only CLIProxyAPI; all provider traffic traverses it.
- **CAP-D002 — Client topology:** Slarti and Lydia consume through OpenCode; workers are later scope.
- **CAP-D003 — Sequential account consumption:** Prefer one account until exhausted, with sticky routing where required.
- **CAP-D004 — Reset authority:** Provider reset metadata is authoritative; otherwise use jittered 1-minute to 6-hour exponential backoff and model-specific real probes.
- **CAP-D005 — Classification authority:** OpenCode classifies first; CLIProxyAPI may challenge upward; Operator resolves disagreement.
- **CAP-D006 — Quality priority:** At equal suitability, quality outranks quota and cost.
- **CAP-D007 — Released governance only:** Latest released compatible governance is active; running tasks switch only after a commit.
- **CAP-D008 — Repository checkpoints:** Every model switch creates and commits `docs/checkpoints/<task-id>.md`; merge requires later resolution trailers.
- **CAP-D009 — Canonical progress:** Every Plan-as-Code epic uses a top-level README dashboard updated after every task and checkpoint.
- **CAP-D010 — Separate experiment container:** Experiments never run inside the production container and never receive production provider secrets.
- **CAP-D011 — Ephemeral ownership:** The service does not back up experiment output; the experimenter owns persistence after HTTP package delivery.
- **CAP-D012 — Reproducible evidence:** Markdown report plus versioned JSON manifest and canonical SHA-256 are mandatory.
- **CAP-D013 — Artifact confinement:** Only canonical paths beneath the run directory are accepted; external paths are refused.
- **CAP-D014 — Lifecycle:** Explicit finish or 12-hour idle ends a run; default hard limit is seven days with Operator-bounded extensions and 12-hour download-only phase.
- **CAP-D015 — Attempts:** At most three attempts per Run ID; restart increments attempt, resume does not.
- **CAP-D016 — Runtime prediction:** More than five predicted minutes is rejected unless a run-specific Operator override exists.
- **CAP-D017 — Hard host envelope:** CPU is 50% of threads; RAM is the lower of 25% total and 50% free at start; no override exists.
- **CAP-D018 — Automatic admission calibration:** Host thresholds use a rolling seven-day history and activate only between runs.
- **CAP-D019 — Operator duration control:** Each extension requires a concrete limit no more than 28 days from extension time and may be repeated.
- **CAP-D020 — Reactivation:** During download-only phase, Operator may reactivate and choose resume by default or restart.
- **CAP-D021 — Dry-run protection:** Dry-runs do not extend idle lifetime and are rate, concurrency and resource bounded.
- **CAP-D022 — Backup semantics:** Drain for up to 15 minutes; never abort a running request solely for backup; failed backup enters degraded mode.
- **CAP-D023 — Governance locality:** Project-local model rules may move class up or down but cannot weaken security, secrets, authorization or audit.

Open decisions remain listed in the canonical README.