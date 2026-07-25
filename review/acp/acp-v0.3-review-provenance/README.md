# Agent Coordination Protocol (ACP)

## Purpose

This repository is the **authoritative source** for the Agent Coordination
Protocol (ACP) — a provider-, model-, transport- and platform-independent
protocol for agent collaboration, review, and handoff.

ACP defines the formal state machine, review package schema, verdict format,
execution contract, trigger contract, review provenance, and conformance
requirements for coordinating Planer, Implementerer, Reviewer, Eddie, and
Executors across heterogeneous agent systems.

## Authoritative Source Rule

- The ACP specification lives **here**, not in issues, chat logs, or other repos.
- Issues and PR descriptions may reference ACP terms but must never redefine them.
- Changes to ACP require a PR against this repository plus a passing conformance
  suite.
- The current release is the single source of truth — working copies are drafts.

## Repository Structure

```
README.md              — This file
SPEC/                  — ACP core specification and state machine
  execution-contract.md  — Execution Contract (Slarti → Lydia)
  trigger-contract.md    — Trigger Contract (Slarti → Eddie → Lydia)
  review-provenance.md   — Review Provenance (verdict types, commit binding)
SCHEMAS/               — Versioned JSON/YAML schemas for artifacts
CONFORMANCE/           — Conformance test suite and fixtures
EXAMPLES/              — Example artifacts (review packages, verdicts, handoffs)
FINDINGS/              — Pilot findings and observations (drives ACP revisions)
DECISIONS/             — Architectural decisions derived from findings
CHANGELOG.md           — Versioned changelog
VERSION                — Current version string
```

## Releases

Releases are created via Gitea's release function. Each release is bound to an
exact commit SHA. All external references must point to a release, not to a
branch.

## License

Homelab internal — not for public distribution.
