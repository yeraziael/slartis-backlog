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

- Planning PR #82 is open rather than merged to `main`; PW-I01 explicitly blocks
  on the default-branch merge gate.
- ACP `0.1.0-draft` has no normative state machine. Ticket transitions are
  repository control states, not a parallel ACP specification.
- Ticket snapshots can become stale after Gitea edits. Any edit to #253-#281
  requires regenerating this package and a new SHA-bound review.
