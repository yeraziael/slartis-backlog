# Routing and Governance

## Effective hierarchy

Specificity precedence:

1. repository + task type + functional area
2. task type + functional area
3. task type
4. functional area
5. global rule

Equal-specificity conflicts select the higher model class, preserve execution and emit a conflict event. A governance task is generated after five repeats for repository + task type or three repeats for repository + task type + functional area.

## Classification challenge

OpenCode supplies classification when possible. The governance layer or an approved component may propose an upward correction before LiteLLM routing. Neither LiteLLM nor CLIProxyAPI becomes the sole semantic classification authority without a later decision. OpenCode reviews the proposal. Operator decides unresolved disagreement. Five repeated errors for the same task type and functional area generate a versioned governance change proposal.

Dynamically discovered functional areas must be assigned to an existing parent area and approved in dedicated governance review before activation.

## Model quality evidence

Governance ranking and measured results jointly determine quality. A ranking proposal may be generated after at least five completed reviews with at least two review steps per model.

Measured signals:

- review rounds
- weighted finding severity
- post-merge regression debt
- test failures
- rework by another model
- clean acceptance rate

Initial finding weights:

| Severity | Weight |
|---|---:|
| Critical | 8 |
| Major | 4 |
| Minor | 2 |
| Nit | 1 |

Regression debt is never below 12 points. Severity multipliers are 1.0 minor, 1.5 major and 2.0 critical. Age multipliers are 1.0 for 0–7 days, 1.25 for 8–14, 1.5 for 15–30 and 2.0 beyond 30 days. Security/secret/authorization violations, data-integrity or irreversible-data defects and complete service outage are at least critical.

Performance regression is measured against a verified baseline: up to 10% nit, above 10–25% minor, above 25–50% major, above 50% or materially higher timeout/abort rate critical.

## Baselines and task size

Baselines are separated by repository × model × task type × functional area × task size. Sizes are XS, S, M, L and XL. Plan-as-Code supplies initial size; the approved governance component may propose at most one class up or down before LiteLLM selects a route. Gateways may report evidence for a later proposal but do not reclassify an in-flight request. Operator decides unresolved objections.

Before 20 completed tasks in a size class, inference is observation-only. Afterwards proposals may be made. Heuristics update in batches of 20 new tasks per class using P75 as primary, P50 as reference and P90/P95 for outliers.

## Released governance adoption

Only released governance is active. A new release becomes active for running tasks at the next safe interruption point after a commit. The task is reclassified and rerouted through the gateway chain. A required model switch produces a repository checkpoint before work continues.

## Audit and telemetry

- Routing audit: global ring buffer of 250 complete assignment entries, annotated with gateway hop (LiteLLM or CLIProxyAPI).
- Heuristic telemetry: persistent local database on the Pi; included in Homelab backup but not committed.
- Git contains schemas, migrations, configuration, reproducible aggregation logic and a human-readable explanation of only the latest heuristic change.
- Each explanation records timestamp, old and new rule, data basis, percentiles, expected effect and review reference.
