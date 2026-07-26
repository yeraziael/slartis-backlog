# Scope, Risks And Exclusions

## Included

- Exact Gitea ticket set and execution parent snapshot.
- Dependency graph and ordering rationale.
- Six Sol-only decision contracts and twenty-one low-cost implementation contracts.
- Five-ticket ACP checkpoint contract.
- Plan-to-ticket mapping, reviewer workflow and model recommendations.

## Excluded

- No changes to `Homelab/Architecture`.
- No Playwright project, runner, test, fixture, workflow or deployment code.
- No Gitea ticket execution.
- No ACP specification change.
- No secrets, accounts, Keycloak objects, containers, DNS or runtime mutation.

## Review Risks

- Planning PR #82 and PW-D01 are complete. The blocking risk is activation of
  the amended self-verification/self-merge workflow before independent review.
- Self-verification never supplies independent approval authority. Merge
  authority comes only from the Operator's standing epic authorization.
- ACP `v0.3.0` review-provenance semantics are binding.
- Ticket snapshots can become stale after Gitea edits. Any edit to #253-#281
  remains prohibited unless a later reviewed amendment changes ticket scope.
