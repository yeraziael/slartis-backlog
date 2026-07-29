# CLIProxyAPI Plan as Code

**Canonical entrypoint:** this file  
**Tracking issue:** #110  
**Status:** Scope corrected; implementation not authorized  
**Current phase:** Architecture review and execution decomposition  
**Active task:** CAP-P01 — complete review after gateway-scope correction

## Purpose

The target system provides OpenCode with exactly one model-provider endpoint through LiteLLM. LiteLLM is the public-internal gateway and routing frontdoor for OpenCode Zen Free models, Ollama models, ordinary provider APIs and specialized downstream gateways.

CLIProxyAPI is retained as a downstream subscription bridge for provider access that depends on supported CLI/OAuth credentials, multi-account pools and sticky account routing. OpenCode does not connect to CLIProxyAPI directly.

This directory is authoritative for requirements, architecture, governance contracts, experiments, operations, testing, roadmap, backlog and decisions. Runtime deployment remains authoritative in the Homelab architecture repository.

## Progress dashboard

| Area | Status | Progress |
|---|---:|---:|
| Requirements | Scope correction drafted | 75% |
| Architecture | Scope correction required | 65% |
| Routing governance | Drafted | 75% |
| Experiment system | Drafted | 85% |
| Operations and backup | Drafted | 70% |
| Testing and evidence | Drafted | 60% |
| Execution backlog | Rework required | 55% |
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

- LiteLLM as the single OpenAI-compatible endpoint configured in OpenCode.
- Direct LiteLLM routing to OpenCode Zen Free and approved Ollama models.
- Direct LiteLLM routing to approved API-key providers where applicable.
- CLIProxyAPI as a private downstream backend for supported CLI/OAuth subscriptions and multiple accounts per provider.
- Task classification, model selection, quota handling, sticky routing and governance updates across the gateway chain.
- Keycloak-protected operator and experiment surfaces.
- Ephemeral experiment containers with reproducible reports and bounded host impact.
- Persistent production telemetry, backup, degraded mode and recovery.
- Repository checkpoint contracts for safe model switches.

## Non-goals

- Making CLIProxyAPI responsible for OpenCode Zen Free or Ollama connectivity.
- Exposing CLIProxyAPI directly as OpenCode's configured provider endpoint.
- Provider credential creation or storage in Git.
- Runtime mutation during planning.
- Bypassing provider terms, quotas or identity controls.
- Persisting prompts, responses, secrets or account identifiers in planning artifacts.
- Treating either gateway as a task queue; request retry or queueing belongs to clients such as OpenCode.

## Current next executable task

`CAP-P01`: reconcile architecture, governance, operations, testing, roadmap and backlog with CAP-D024; validate LiteLLM support for Zen Free and Ollama, validate CLIProxyAPI as a downstream OAuth/subscription bridge, and produce the independent architecture/security review without changing runtime state.

## Open decisions

- Exact LiteLLM and CLIProxyAPI versions or commits and image strategy.
- Whether LiteLLM-to-CLIProxyAPI uses one logical deployment per provider, account pool or model family.
- Session-affinity contract across LiteLLM and CLIProxyAPI.
- Final production host measurements and resource budget.
- Exact provider authentication methods and compliance status.
- Concrete bootstrap thresholds before seven days of host calibration data exist.
- Final API paths and schemas.

## Risks

- Provider terms may prohibit some subscription or CLI credential forwarding methods.
- LiteLLM and CLIProxyAPI protocol translations may not preserve every provider-specific feature.
- Multi-account subscription routing may break stateful sessions without end-to-end affinity.
- Upstream management or authentication behavior may change.
- Raspberry Pi resource pressure could affect unrelated services if admission controls fail.
- Incorrect task classification could waste paid quota or lower implementation quality.

## Local model overrides

None active. Any override must document scope, direction, rationale, affected task type and functional area, governance version and review reference.
