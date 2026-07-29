# Roadmap

## M0 — Canonical migration

- Inventory PR #71, issue #74 and legacy `CLIProxyAPI-Homelab/` material.
- Classify inherited statements and produce source-to-target migration matrix.
- Verify current upstream, provider methods and host facts.
- Validate LiteLLM support for Zen Free and Ollama.
- Validate CLIProxyAPI as a downstream OAuth/subscription bridge.
- Complete independent architecture and security review.

## M1 — Governance and contracts

- Implement stable requirement and decision validation.
- Add released governance loading, specificity precedence and classification challenge.
- Define commit trailers, checkpoint files and merge gates.
- Freeze machine-readable execution decomposition and hash.

## M2 — LiteLLM foundation

- Pin LiteLLM image or reproducible build.
- Deploy LiteLLM as the internal-only production frontdoor on the evidence-selected host.
- Add per-client LiteLLM credentials.
- Implement LiteLLM routing to Zen Free and approved Ollama models.
- Implement LiteLLM routing to approved API-key providers.
- Add LiteLLM-to-CLIProxyAPI forwarding for subscription/OAuth backends.
- Implement routing audit and persistent heuristic telemetry for LiteLLM.

## M3 — CLIProxyAPI downstream

- Pin CLIProxyAPI image or reproducible build.
- Deploy CLIProxyAPI as private downstream backend.
- Implement provider/account isolation, credential management and CLI/OAuth authentication.
- Implement sequential quota rollover and sticky routing within CLIProxyAPI.
- Implement Retry-After, backoff and model-specific probes for subscription backends.

## M4 — Routing pilot

- Connect OpenCode to LiteLLM as the sole configured endpoint.
- Validate OpenAI-required classes and free-model implementation path.
- Verify end-to-end quota rollover, sticky sessions, Retry-After, backoff and model-specific probes.
- Verify LiteLLM-to-CLIProxyAPI forwarding for subscription-bound traffic.
- Do not add Slarti or Lydia until pilot acceptance is complete.

## M5 — Operations

- Implement maintenance drain, backup, degraded mode and restore verification for both gateways.
- Add dashboard status, Operator controls and manual backup recovery per gateway.
- Calibrate host admission thresholds from rolling seven-day history.

## M6 — Experiment platform

- Add ephemeral LiteLLM and CLIProxyAPI test containers and isolated test-service endpoints.
- Implement lifecycle, attempts, duration prediction, overrides, reactivation and retention.
- Implement Markdown/JSON package, schema validation, canonical hash and HTTP delivery.
- Add Playwright fixtures, reset endpoints and reproducibility tests.

## M7 — Agent adoption

- Enable Slarti and Lydia through OpenCode after pilot and operations gates pass.
- Add future workers only through separately reviewed scope.
- Begin quality-data collection and governance ranking proposals.

## M8 — Freeze and handover

- Resolve all blocking review findings.
- Record final execution manifest hash.
- Link merged implementation PRs and operational evidence.
- Mark superseded legacy planning without deleting provenance.
