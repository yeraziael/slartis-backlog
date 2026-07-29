# Requirements

Requirement IDs are stable. Removal or semantic change requires an entry in `decisions.md`.

## Gateway and clients

- **CAP-R001:** OpenCode sees exactly one configured model-provider endpoint: LiteLLM.
- **CAP-R002:** Slarti and Lydia use the gateway chain indirectly through OpenCode; workers are added only through later approved scope.
- **CAP-R003:** All model traffic traverses LiteLLM. OpenCode Zen Free and Ollama are routed directly by LiteLLM; supported CLI/OAuth subscription traffic may be routed from LiteLLM to CLIProxyAPI.
- **CAP-R004:** Each client has an isolated, revocable LiteLLM credential and cannot inspect or disable unrelated clients or downstream provider accounts.
- **CAP-R005:** Neither LiteLLM nor CLIProxyAPI is a task queue. Downtime returns explicit failure; retry or queueing is a client responsibility.

## Providers, accounts and quota

- **CAP-R010:** The gateway portfolio initially includes OpenCode Zen Free and approved Ollama models through LiteLLM, plus supported CLI/OAuth subscription providers through CLIProxyAPI. Ordinary API-key providers and Gemini may be added only after provider-specific compliance and compatibility approval.
- **CAP-R011:** Multiple accounts, subscriptions or keys per provider are supported where the relevant downstream supports compliant pooling.
- **CAP-R012:** Accounts are consumed sequentially: prefer one account until quota exhaustion, then select the next eligible account.
- **CAP-R013:** Session-bound APIs use end-to-end sticky routing across LiteLLM and CLIProxyAPI.
- **CAP-R014:** Provider `Retry-After` or reset metadata is authoritative.
- **CAP-R015:** Without reset metadata, use jittered exponential backoff starting at one minute and capped at six hours.
- **CAP-R016:** A probe is a real minimal request using exactly the model required by the waiting task. Success resets backoff to one minute and resumes the task automatically.
- **CAP-R017:** CLIProxyAPI is private infrastructure reachable only by LiteLLM and approved operator paths; OpenCode clients do not receive direct CLIProxyAPI credentials.
- **CAP-R018:** A model exposed through LiteLLM must declare its backend type, provider identity, authentication class, compliance state and session-affinity requirements.
- **CAP-R019:** Failure or exhaustion of a CLIProxyAPI subscription pool must not silently reroute to a chargeable API provider unless released governance explicitly authorizes that fallback.

## Classification and routing

- **CAP-R020:** Routing is derived from task classification and released governance.
- **CAP-R021:** Model classes, task mappings and provider priorities are loaded from released governance; gateway configuration must not hard-code a separate class policy.
- **CAP-R022:** Free-model preference and fallback order are governance data. The gateway applies the active released order and availability constraints without embedding model names in application logic.
- **CAP-R023:** Dynamic alternatives require tool use, structured output, sufficient context, coding suitability, stable unattended operation and no known repository-work exclusion.
- **CAP-R024:** Manual and automatic overrides follow released governance and are audit-recorded; no gateway-local override may bypass a required operator confirmation.
- **CAP-R025:** Unclassified tasks are classified before LiteLLM routing by the approved client-side or governance component; neither LiteLLM nor CLIProxyAPI becomes the sole semantic classification authority without a later decision.
- **CAP-R026:** A routing component may challenge an OpenCode classification upward but never silently lower it. Unresolved disagreement is decided by the Operator.
- **CAP-R027:** Routing quality takes precedence over quota and cost when candidates are equally suitable.
- **CAP-R028:** The effective decision must be reproducible from normalized input, governance version and relevant system state.

## Governance

- **CAP-R030:** Only released governance is active; the latest released compatible version is selected automatically.
- **CAP-R031:** Running tasks adopt new governance only at a safe interruption point after a commit.
- **CAP-R032:** After governance change, classification and routing are revalidated. A required model change creates a checkpoint and commit.
- **CAP-R033:** Five repeated misclassifications of the same task type and functional area generate a versioned governance proposal.
- **CAP-R034:** Project-local rules may raise or lower model class but may not weaken security, secret, authorization or audit controls.
- **CAP-R035:** More specific rules win. Equal-specificity conflict selects the higher model class, logs the conflict and continues.

## Checkpoints and repository evidence

- **CAP-R040:** Before every model switch, the agent updates `docs/checkpoints/<task-id>.md` and commits checkpoint plus current work and Plan-as-Code dashboard state.
- **CAP-R041:** A checkpoint commit may be non-green if expected failures are documented, but may never be the final task commit.
- **CAP-R042:** Later regular commits reference checkpoint SHAs with repeatable `Resolves-Checkpoint:` trailers.
- **CAP-R043:** Merge and closure are blocked while unresolved checkpoints exist or the last task commit is a checkpoint.
- **CAP-R044:** Every implementation commit for an execution task records Model, Class, Task and Governance-Version trailers. Planning-only commits before execution-manifest freeze are excluded.

## Experiments

- **CAP-R050:** Experiments run in a separate ephemeral container, started only for experiment or Playwright runs.
- **CAP-R051:** The experiment container has separate configuration, database and test credentials and no production provider secrets.
- **CAP-R052:** Each run has a unique Run ID and at most three attempts. Restart increments `attempt-N`; resume does not.
- **CAP-R053:** The experiment must be declared before execution and is rejected when predicted runtime exceeds five minutes unless an Operator grants a run-specific override.
- **CAP-R054:** The default absolute run limit is seven days. Operator extensions require a concrete bound of at most 28 days from the extension time and may be repeated.
- **CAP-R055:** After hard stop, results remain downloadable for 12 hours. During this phase, an Operator may reactivate and choose resume (default) or restart.
- **CAP-R056:** One experiment executes per run by default. Additional starts return 429. The fifth consecutive 429 includes detailed human guidance.
- **CAP-R057:** Experiment results are not backed up or persisted by the service. The experimenter receives a complete package and owns persistence.

## Host protection

- **CAP-R060:** CPU is capped at 50% of logical threads.
- **CAP-R061:** RAM is capped at the lower of 25% total RAM and 50% of free RAM measured at container start.
- **CAP-R062:** CPU and RAM limits are hard protections and cannot be overridden by the Operator.
- **CAP-R063:** Admission is rejected during unsafe host load, memory pressure, swap activity, I/O pressure or insufficient disk.
- **CAP-R064:** Admission thresholds are calibrated automatically from a rolling seven-day history and activated only between runs.
- **CAP-R065:** Dry-runs are bounded by concurrency, rate and resource controls and must not be able to deny service to the Pi.

## Reporting and artifacts

- **CAP-R070:** Every run produces a Markdown report, versioned JSON manifest and SHA-256 hash over the canonical manifest.
- **CAP-R071:** Manifest schema validation is mandatory. Invalid manifests or missing referenced artifacts fail the run.
- **CAP-R072:** All artifacts must resolve inside `experiments/<run-id>/`; external paths, traversal, symlinks escaping the root and external mounts are refused.
- **CAP-R073:** The finalized run directory is delivered as `cliproxyapi-experiment-<run-id>.tar.gz` through an authenticated HTTP endpoint.
- **CAP-R074:** The Markdown report references the manifest and its hash instead of embedding the full JSON.
- **CAP-R075:** A failed admission check creates a secret-free diagnostic snapshot referenced by report and manifest.
