# Decision Log

- **CAP-D001 — Single gateway:** Superseded by CAP-D024. OpenCode uses one configured endpoint, but that endpoint is LiteLLM rather than CLIProxyAPI.
- **CAP-D002 — Client topology:** Slarti and Lydia consume through OpenCode; workers are later scope.
- **CAP-D003 — Sequential account consumption:** Prefer one account until exhausted, with sticky routing where required.
- **CAP-D004 — Reset authority:** Provider reset metadata is authoritative; otherwise use jittered 1-minute to 6-hour exponential backoff and model-specific real probes.
- **CAP-D005 — Classification authority:** Superseded in part by CAP-D024. OpenCode or an approved governance component classifies before gateway routing; CLIProxyAPI is not assumed to classify every task.
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
- **CAP-D024 — Gateway Scope Definition:** LiteLLM is the single model-provider endpoint configured in OpenCode and the policy-enforcement and routing frontdoor for the gateway chain. LiteLLM connects directly to OpenCode Zen Free, approved Ollama models and approved ordinary provider APIs. CLIProxyAPI remains a private downstream specialization for upstream-supported CLI/OAuth subscriptions, multiple subscription accounts and provider-specific sticky routing. CLIProxyAPI is not responsible for Zen Free or Ollama and is not exposed directly to OpenCode. End-to-end routing must preserve provider identity, authentication class, compliance state, quota semantics and session affinity. A subscription pool may not silently fail over to a chargeable API path without explicit released-governance authorization.
- **CAP-D025 — LiteLLM frontdoor topology:** OpenCode connects exclusively to LiteLLM. LiteLLM is the sole configured provider endpoint. CLIProxyAPI is reachable only through LiteLLM and approved operator paths. LiteLLM routes directly to Zen Free and Ollama; CLI/OAuth/subscription traffic is forwarded to CLIProxyAPI.
- **CAP-D026 — Independent gateway degraded modes:** LiteLLM and CLIProxyAPI may enter degraded mode independently. LiteLLM degraded blocks CLIProxyAPI routing but continues Zen Free and Ollama. CLIProxyAPI degraded blocks only subscription/OAuth backends.
- **CAP-D027 — Gateway-layer credential isolation:** Each gateway (LiteLLM and CLIProxyAPI) holds credentials only for its own provider scope. No gateway receives credentials for the other gateway's providers. OpenCode clients receive only LiteLLM credentials.
- **CAP-D028 — Governance-owned model policy:** Model classes, task mappings, free-model preference and fallback order come only from released governance. LiteLLM executes the resulting route; neither gateway embeds a competing model ladder.
- **CAP-D029 — Secure CLIProxyAPI baseline:** Plugins, control-panel download/update, cloaking, remote management and debug endpoints are disabled by default. CLIProxyAPI binds only to the private LiteLLM service path. Every additional OAuth callback port requires an explicit provider-specific decision.
- **CAP-D030 — Custom control functions:** Deterministic dry-run, Decision Hash, model-specific probes and the 250-entry cross-gateway audit ring are custom management-layer requirements, not assumed native LiteLLM or CLIProxyAPI features.
- **CAP-D031 — Sequential pool strategy:** Approved subscription pools use CLIProxyAPI `fill-first` routing. End-to-end sticky routing requires one normalized affinity key preserved by LiteLLM and consumed by CLIProxyAPI.

Open decisions remain listed in the canonical README.
