# CLIProxyAPI Plan as Code

**Canonical entrypoint:** this file  
**Tracking issue:** #110  
**Status:** Planning baseline captured; implementation not authorized  
**Current phase:** Canonicalization and independent review  
**Active task:** CAP-P01 — complete and review the Plan-as-Code baseline

## Purpose

CLIProxyAPI is the single provider gateway used by OpenCode. Slarti and Lydia consume model access through OpenCode; future workers may be added later. All provider traffic, including OpenCode Zen Free models, must pass through CLIProxyAPI.

This directory is authoritative for requirements, architecture, governance contracts, experiments, operations, testing, roadmap, backlog and decisions. Runtime deployment remains authoritative in the Homelab architecture repository.

## Progress dashboard

| Area | Status | Progress |
|---|---:|---:|
| Requirements | Drafted | 70% |
| Architecture | Drafted | 65% |
| Routing governance | Drafted | 75% |
| Experiment system | Drafted | 85% |
| Operations and backup | Drafted | 70% |
| Testing and evidence | Drafted | 60% |
| Execution backlog | Drafted | 55% |
| Independent review | Open | 0% |
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

`CAP-P01`: validate this baseline against PR #71, issue #74, the current upstream CLIProxyAPI release and released ai-governance. Produce a source-to-target migration matrix and independent architecture/security review without changing runtime state.

## Open decisions

- Exact upstream version or commit and image strategy.
- Final production host measurements and resource budget.
- Exact provider authentication methods and compliance status.
- Concrete bootstrap thresholds before seven days of host calibration data exist.
- Final API paths and schemas.

## Risks

- Provider terms may prohibit some subscription or CLI credential forwarding methods.
- Upstream management or authentication behavior may change.
- Raspberry Pi resource pressure could affect unrelated services if admission controls fail.
- Incorrect task classification could waste paid quota or lower implementation quality.

## Local model overrides

None active. Any override must document scope, direction, rationale, affected task type and functional area, governance version and review reference.