# Experiment System

## Lifecycle

1. Experimenter defines the complete run before start.
2. Admission control predicts duration and checks host capacity.
3. Predicted duration above five minutes is rejected unless an Operator grants a run-specific override.
4. Separate LiteLLM and/or CLIProxyAPI test containers start with fixed hard resource limits.
5. Results remain available until explicit finish, 12 hours of idle time or the absolute duration limit.
6. Hard stop starts a 12-hour download-only window.
7. The service then destroys container state and package unless an Operator reactivates during that window.

## Run and attempts

Each run has one Run ID and up to three attempts. Restart increments `attempt-N`; resume keeps the current attempt. A fourth attempt requires a new Run ID.

The default absolute limit is seven days. An Operator may set or extend a concrete limit to at most 28 days from the extension time, including during a running run. Repeated extensions are allowed. During the download-only phase, the Operator may reactivate and choose resume or restart; resume is preselected. Resume requires a valid checkpoint, fixture version, image, governance version and artifacts.

## Idle behavior

Only state-changing experiment API actions, actual package downloads and explicit keep-alive count as activity. Dashboard presence, health, readiness, status polling, log reads, metrics, metadata reads, dry-runs and rejected calls do not.

The authenticated keep-alive resets idle lifetime to 12 hours only when nine hours or less remain. Earlier calls return `409 Conflict`, machine code `keep_alive_too_early`, `Retry-After` and `X-Experiment-Idle-Remaining`; they do not change activity state.

## Parallelism and overload protection

One experiment executes per run by default. Additional start requests return 429. The fifth consecutive 429 includes a detailed explanation of the limit, protective rationale, active experiment, remaining wait and Operator override path. The counter resets after a successful start or completion.

The Operator may set arbitrary run-specific parallelism. The UI warns when requested process count exceeds logical system threads. Resource limits remain hard and are not increased by this override.

## Resource envelope

- CPU: at most 50% of logical threads.
- RAM: `min(25% total RAM, 50% free RAM at container start)`.
- Limits are fixed for the run and cannot be overridden.
- Unsafe host load, memory pressure, swap, I/O wait or insufficient disk rejects admission.
- Thresholds derive from a rolling seven-day calibration window, use robust outlier handling and activate only between runs.
- Bootstrap thresholds remain conservative until sufficient history exists.

Every failed admission check creates a diagnostic snapshot containing Run ID, attempt, timestamp, computed limits, host metrics, active thresholds, rejection reason, retry recommendation and calibration basis.

## Fixtures and test endpoints

The `test-service` role may load versioned fixtures, reset the isolated test state and set spoofed quota, provider, telemetry, availability and quality values. Spoofing is nonpersistent, clearly distinguished from real state and marked as test in audit output. Production state and secrets remain unreachable. Fixtures cover both LiteLLM and CLIProxyAPI test containers.

## Reproducible package

The package is named `cliproxyapi-experiment-<run-id>.tar.gz` and includes:

- Markdown report
- versioned JSON manifest
- SHA-256 hash over the canonical JSON manifest
- Run ID, attempt history and timestamps
- repository, branch and commit SHA
- container images and digests (LiteLLM and/or CLIProxyAPI)
- global and local governance versions
- fixture versions
- configuration, flags and normalized inputs
- real and spoofed state declarations
- models, simulated accounts and Decision Hashes
- expected and actual results
- errors, retries and deviations
- host architecture and resource envelope
- reproducible start command
- logs, traces, screenshots and referenced artifacts

The report links to the manifest and hash. Schema validation and artifact existence checks are mandatory. External paths are refused at registration after canonical path resolution, including traversal, escaping symlinks and external mounts. Finalized run directories are immutable.
