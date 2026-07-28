# KitchenOwl Plan as Code

Single issue entrypoint: #112

This directory is the authoritative implementation plan for the KitchenOwl household inventory and shopping extension. GitHub issues are not used as a parallel work breakdown. Progress, decisions, dependencies and acceptance criteria live in versioned files here.

## Navigation

- `plan.yaml` — machine-readable workstream graph, status and dependencies
- `requirements.md` — consolidated functional contract
- `architecture.md` — target architecture, trust boundaries and integrations
- `roles-and-notifications.md` — Keycloak roles, Signal/Matrix flows and escalation rules
- `forecasting-and-inventory.md` — stock, consumption, season, weather and calibration rules
- `acceptance.md` — end-to-end acceptance criteria and release gates

## Operating rules

1. #112 is the only GitHub issue used as entrypoint.
2. Every implementation change must reference a workstream ID from `plan.yaml`.
3. Decisions are changed by pull request, never only in issue comments.
4. A workstream may move to `done` only when all linked acceptance criteria pass.
5. Historical behavior and operator overrides must remain auditable.
6. All automation is fail-closed where an incorrect stock mutation could occur.

## Status model

`planned -> ready -> in_progress -> blocked -> review -> done`

The plan is complete enough to begin architecture and bootstrap work. Remaining detail discovered during implementation must be captured as amendments to these files, not as new planning issues.