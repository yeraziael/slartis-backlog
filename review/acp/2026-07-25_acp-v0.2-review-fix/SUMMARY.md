# Summary — ACP v0.2 Review Fix (Findings 1-6)

## Problem

Review of the ACP v0.2 contracts (yeraziael/slartis-backlog#90) found 7 Major and 2 Minor findings. Findings 1-6 require corrective changes to the ACP specifications, schemas, and examples before the bundle can be finalized.

## Goal

Address findings 1-6 from the review:
1. Conditional required for cron/schedule sub-fields within `schedule` object
2. `webhook.secret` renamed to `webhook.secret_ref` with normative resolution
3. Immutable identity model: `(trigger_id, activation.version)` is the immutable pair
4. `action_ref` version suffix is now mandatory (was optional)
5. `constraints`, `rollback`, `success_criteria` are now required top-level fields
6. Add schema-level test harness (test_schemas.py) + CI integration

## Scope

- 13 changed files, 290 insertions, 41 deletions
- All in Homelab/ACP, branch `fix/acp-v0.2-review-findings`

## Not in Scope

- Bundle regeneration (Finding 7) — deferred until this corrective PR is merged
- Runtime implementation of any ACP contract fields
- Changes outside Homelab/ACP

## Affected Components

- `SCHEMAS/trigger-contract.json` — conditional schedule sub-fields, secret_ref, mandatory action_ref version
- `SCHEMAS/execution-contract.json` — added required fields (constraints, rollback, success_criteria)
- `SPEC/trigger-contract.md` — immutable identity model, updated field docs
- `SPEC/execution-contract.md` — updated field requirements
- `EXAMPLES/` — all 4 files updated for new schema
- `SCHEMAS/test_schemas.py` — new schema-level test harness
- `.gitea/workflows/ci.yaml` — schema test step added
- `CHANGELOG.md`, `VERSION` — version bump 0.2.0 → 0.2.1-draft

## Canonical References

- **Review Issue:** yeraziael/slartis-backlog#90
- **Original PR:** Homelab/ACP#6
- **Corrective PR:** Homelab/ACP#7
- **Repository:** Homelab/ACP (Gitea)
