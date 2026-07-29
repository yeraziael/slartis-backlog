# Roadmap

## M0 — Canonical migration

> **CAP-P01 status (2026-07-29):** Inventory, classification, migration matrix and upstream verification are **complete**. Independent review (CAP-P02) is **ready**. Six compliance blockers and a fundamental upstream scope mismatch identified — see `references.md`.

- Inventory PR #71, issue #74 and legacy `CLIProxyAPI-Homelab/` material.
- Classify inherited statements and produce source-to-target migration matrix.
- Verify current upstream, provider methods and host facts.
- Complete independent architecture and security review.

## M1 — Governance and contracts

- Implement stable requirement and decision validation.
- Add released governance loading, specificity precedence and classification challenge.
- Define commit trailers, checkpoint files and merge gates.
- Freeze machine-readable execution decomposition and hash.

## M2 — Production gateway foundation

- Pin image or reproducible build.
- Deploy internal-only service on the evidence-selected host.
- Add per-client credentials, provider/account isolation and management authorization.
- Implement routing audit and persistent heuristic telemetry.

## M3 — Routing pilot

- Connect OpenCode as the sole initial client.
- Validate OpenAI-required classes and free-model implementation path.
- Verify quota rollover, sticky sessions, Retry-After, backoff and model-specific probes.
- Do not add Slarti or Lydia until pilot acceptance is complete.

## M4 — Operations

- Implement maintenance drain, backup, degraded mode and restore verification.
- Add dashboard status, Operator controls and manual backup recovery.
- Calibrate host admission thresholds from rolling seven-day history.

## M5 — Experiment platform

- Add ephemeral test container and isolated test-service endpoints.
- Implement lifecycle, attempts, duration prediction, overrides, reactivation and retention.
- Implement Markdown/JSON package, schema validation, canonical hash and HTTP delivery.
- Add Playwright fixtures, reset endpoints and reproducibility tests.

## M6 — Agent adoption

- Enable Slarti and Lydia through OpenCode after pilot and operations gates pass.
- Add future workers only through separately reviewed scope.
- Begin quality-data collection and governance ranking proposals.

## M7 — Freeze and handover

- Resolve all blocking review findings.
- Record final execution manifest hash.
- Link merged implementation PRs and operational evidence.
- Mark superseded legacy planning without deleting provenance.