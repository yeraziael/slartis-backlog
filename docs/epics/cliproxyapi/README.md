# CLIProxyAPI Plan as Code

**Canonical entrypoint:** this file  
**Tracking issue:** #110  
**Status:** CAP-P01 complete; baseline verified against upstream; compliance blockers identified
**Current phase:** Independent review preparation
**Active task:** CAP-P02 — prepare and conduct independent architecture and security review

## Purpose

CLIProxyAPI is the single provider gateway used by OpenCode. Slarti and Lydia consume model access through OpenCode; future workers may be added later. All provider traffic, including OpenCode Zen Free models, must pass through CLIProxyAPI.

This directory is authoritative for requirements, architecture, governance contracts, experiments, operations, testing, roadmap, backlog and decisions. Runtime deployment remains authoritative in the Homelab architecture repository.

## Progress dashboard

| Area | Status | Progress |
|---|---|---:|---:|
| Requirements | Drafted, needs upstream realignment | 70% |
| Architecture | Drafted, upstream scope mismatch identified | 65% |
| Routing governance | Drafted, upstream provider model incompatible | 75% |
| Experiment system | Drafted | 85% |
| Operations and backup | Drafted | 70% |
| Testing and evidence | Drafted | 60% |
| Execution backlog | Updated for CAP-P01 findings | 65% |
| Upstream verification | Complete — v7.2.104 | 100% |
| Compliance blockers | 6 documented | 100% |
| Independent review | Ready for CAP-P02 | 10% |
| **Overall merged execution progress** | **Not started** | **0%** |

A task contributes 100% to overall execution progress only after implementation, verification, review, approval and merge. Internal task progress is tracked separately.

## Authority model

- Planning, requirements, roadmap, backlog and decisions: this directory.
- Global model and security governance: released versions from `yeraziael/ai-governance`.
- Project-local additions: released local rules documented here; they may raise or lower model class but may never weaken security, secret, authorization or audit controls.
- Runtime deployment, Compose, secrets, networks and operational evidence: Homelab architecture repository.
- Execution state and acceptance evidence: linked execution issues and pull requests.

## Document index

- [Requirements](requirements.md)
- [Architecture](architecture.md)
- [Routing and governance](governance.md)
- [Experiment system](experiments.md)
- [Operations](operations.md)
- [Testing and evidence](testing.md)
- [Roadmap](roadmap.md)
- [Executable backlog](backlog.md)
- [Decisions](decisions.md)
- [References and migration map](references.md)

## Scope

- Provider and account routing through a single CLIProxyAPI endpoint.
- Task classification, model selection, quota handling, sticky routing and governance updates.
- Keycloak-protected operator and experiment surfaces.
- Ephemeral experiment containers with reproducible reports and bounded host impact.
- Persistent production telemetry, backup, degraded mode and recovery.
- Repository checkpoint contracts for safe model switches.

## Non-goals

- Provider credential creation or storage in Git.
- Runtime mutation during planning.
- Bypassing provider terms, quotas or identity controls.
- Persisting prompts, responses, secrets or account identifiers in planning artifacts.
- Treating CLIProxyAPI as a task queue; request retry or queueing belongs to clients such as OpenCode.

## Current next executable task

`CAP-P02`: conduct independent architecture and security review based on CAP-P01 findings. Verify upstream compliance, assess OAuth credential forwarding model, evaluate plugin system risks, and produce a Go/No-Go recommendation.

## Open decisions

- Whether the Plan-as-Code redefines CLIProxyAPI purpose from "model provider gateway" to "CLI subscription OAuth gateway" (upstream scope mismatch).
- Whether the upstream OAuth credential forwarding model is acceptable under provider terms of service.
- Whether to disable plugins entirely or require a forked/non-default Compose.
- Which of the 6 upstream ports to expose vs block at the network boundary.
- Whether to disable upstream Management API + Control Panel or integrate with planned Keycloak+dashboard.
- How to route OpenCode Zen Free through an upstream that has no Zen Free concept.
- Whether the high upstream release cadence (multiple versions/day) is compatible with pinned-version requirements.
- Exact pinned upstream version or commit and image strategy (blocked by above decisions).
- Final production host measurements and resource budget (requires runtime deployment).
- Concrete bootstrap thresholds before seven days of host calibration data exist.

## Risks

- **Upstream scope mismatch**: CLIProxyAPI is a CLI subscription OAuth gateway, not a model provider gateway. Fundamental replanning may be required.
- **Provider terms**: OAuth credential forwarding for subscriptions (Claude Code, Codex, Grok Build) may violate provider terms of service.
- **Plugin system**: Dynamic library plugins allow arbitrary in-process code execution. No upstream confinement mechanism known.
- **High release cadence**: Multiple versions per day make pinned-version maintenance expensive.
- **Control Panel external dependency**: Management panel assets downloaded from GitHub at runtime; auto-update enabled by default.
- **Raspberry Pi resource pressure**: 6 exposed ports and plugin system increase attack surface and resource usage beyond original estimates.
- **Incorrect task classification** could waste paid quota or lower implementation quality.

## Local model overrides

None active. Any override must document scope, direction, rationale, affected task type and functional area, governance version and review reference.