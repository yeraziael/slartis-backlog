# Playwright — Architecture

## Component Model

```
                    ┌─────────────────────────────────────┐
                    │         Planner / Reviewer           │
                    │  defines coverage, acceptance gates  │
                    └──────────────┬──────────────────────┘
                                   │ requirements, scope
                                   v
                    ┌─────────────────────────────────────┐
                    │              Slarti                  │
                    │  designs suites, versions fixtures   │
                    └──────────────┬──────────────────────┘
                                   │ test code, config
                                   v
                    ┌─────────────────────────────────────┐
                    │        Vekling / CI Runner           │
                    │  executes against deployment cand.   │
                    └──────────────┬──────────────────────┘
                                   │ results, artifacts
                                   v
                    ┌─────────────────────────────────────┐
                    │          Evidence Bundle             │
                    │  manifest + traces + screenshots     │
                    └──────────────┬──────────────────────┘
                                   │ evidence
                                   v
                    ┌─────────────────────────────────────┐
                    │        Reviewer / Merge Gate         │
                    └─────────────────────────────────────┘
```

## Responsibilities

### Planner / Reviewer

- Defines acceptable coverage boundaries per service epic.
- Sets acceptance gates for UI-level test results.
- Evaluates evidence quality, not routine click paths.
- Retains authority over architecture, security posture, subjective UX and merge decisions.
- A passing UI suite MUST NOT override failing lower-layer tests.

### Slarti

- Designs and versions service-specific Playwright suites.
- Maintains shared fixtures, helpers and platform configuration.
- Diagnoses and resolves test failures.
- Ensures evidence binding and provenance integrity.
- Reviews and merges platform changes in `Homelab/Architecture`.

### Vekling / CI Runner

- Executes Playwright suites against the exact deployment candidate.
- Runs in an ephemeral, pinned container — no persistent state.
- Produces machine-readable evidence bound to source and runtime state.
- Reports pass, fail or prerequisite_error deterministically.

### CI Runner (Gitea Actions)

- Hosted on `rechenknecht` (Pi5 is not suitable for browser test execution).
- Invokes Playwright container as a service or step.
- Retains evidence artifacts per run.
- Applies retry policy for known transient infrastructure conditions.

### Service Under Test

- The Homelab service being verified (e.g., Audiobookshelf, Jellyfin).
- Must be reachable from the runner network.
- Must expose endpoints that Playwright can interact with over HTTPS.

### Keycloak

- Provides OIDC authentication for all Homelab services.
- Hosts synthetic test identities in a dedicated test realm or test group.
- Must be reachable from the runner network for OIDC login flows.

## Trust Boundaries

```
┌─────────────────────────────────────────────────────────┐
│                    External Network                      │
│  (Internet)                                              │
│                                                          │
│  ┌──────────────┐     HTTPS      ┌──────────────────┐   │
│  │  Vekling /   │ ──────────────→│  Frontproxy       │   │
│  │  CI Runner   │                │  (TLS termination)│   │
│  └──────────────┘                └────────┬─────────┘   │
│                                           │              │
└───────────────────────────────────────────┼──────────────┘
                                            │ HTTP
                         ┌──────────────────┼──────────────────┐
                         │  Trust Boundary  │  Internal Network │
                         │  ┌───────────────▼──────────────┐   │
                         │  │     Service Under Test       │   │
                         │  │  (Audiobookshelf / Jellyfin) │   │
                         │  └───────────────┬──────────────┘   │
                         │                  │ OIDC             │
                         │  ┌───────────────▼──────────────┐   │
                         │  │         Keycloak             │   │
                         │  └──────────────────────────────┘   │
                         └────────────────────────────────────┘
```

### Trust Boundary 1: Runner ↔ Frontproxy

- All runner-to-service traffic goes through frontproxy (TLS termination).
- Runner never accesses services directly on internal ports.
- Frontproxy is the sole entry point for browser tests.

### Trust Boundary 2: Runner ↔ Keycloak

- Runner authenticates via OIDC Authorization Code Flow.
- Synthetic credentials injected at runtime, never stored in images or code.
- Keycloak validates token issuer, signature, audience and expiry.

### Responsibility Boundary: Platform vs Service

| Responsibility | Owner |
|---|---|
| Runner definition, container image, config | Platform (shared) |
| OIDC login fixture, user fixtures | Platform (shared) |
| Evidence manifest generator | Platform (shared) |
| Console-error capture helper | Platform (shared) |
| Service-specific page objects | Service suite |
| Service-specific test journeys | Service suite |
| Controlled test data setup | Service epic |
| Coverage requirement definition | Service epic |

## Runtime Deployment

The runner MAY execute in two contexts:

1. **Operator-invoked (local):** Operator runs Playwright from a workstation or `rechenknecht` against the live Homelab deployment.
2. **CI-invoked (automated):** Gitea Actions triggers the Playwright container as part of a workflow, targeting the deployed service or a staging instance.

In both contexts, the runner container is ephemeral, the Playwright image is pinned by digest, and secrets are injected via environment variables at container start.
