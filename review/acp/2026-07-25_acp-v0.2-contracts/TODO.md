# TODO — ACP v0.2 Contracts

## Open Items

- [ ] Eddie runtime implementation (separate Epic required)
- [ ] Migration mapping review: confirm existing cron/systemd tasks are correctly documented

## Follow-up Issues

- `yeraziael/ai-governance` requires a Change Request for Eddie implementation requirements (noted in canonical PR body)
- Homelab/ACP schema repository or CI integration for contract validation

## Technical Debt

- No runtime integration test for contracts
- Examples cover single-action flows only; multi-action orchestration examples deferred

## Known Limitations

- Execution Contract does not define cancellation/termination semantics for running actions
- Trigger Contract missing webhook authentication scheme definition (deferred to implementation)
- Sequence diagram in trigger-contract.md is ASCII-art; could be replaced with Mermaid

## Decisions Required Before Merge (already merged)

- N/A — this is a post-merge review bundle; all decisions were made during the canonical PR

## Deferred

- Blackbox test execution (requires Michael)
- Runtime integration tests (requires Eddie implementation)
