# Risks — ACP v0.2 Contracts

## Architecture

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Contracts introduce parallel mechanism to existing task-loop | Low | Medium | Alignment mapping documents how each existing mechanism maps to the new contracts |
| Contract scope creep (unified vs. separate contracts) | Low | Low | ADR-001 explicitly documents the decision and consequences |

## Security

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Execution contract exposes internal action names | Low | Low | ACP is internal Homelab specification; no public exposure |
| Trigger contract schedules leak operational patterns | Low | Low | Same as above |

## Operations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Eddie implementation diverges from contract spec | Medium | High | JSON Schemas provide machine-validable enforcement |
| Lydia rejects valid contracts due to schema mismatch | Medium | Medium | Examples cover both valid and invalid cases |

## Migration

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Existing cron/systemd jobs not migrated | High | Medium | Documented as explicit exclusion; follow-up governance issue needed |
| Legacy task definitions incompatible with v0.2 | Low | Medium | Backward compatibility is maintained by additive design |

## Compatibility

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Schema changes in future ACP versions break v0.2 contracts | Low | High | Semantic Versioning governs contract schema changes |

## Maintainability

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Contracts become stale if not adopted by runtime | Medium | Medium | ACP is a living specification; adoption tracked via Epic issues |

## Rollback

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| No rollback plan for already-merged changes | N/A | Low | Changes are additive and specification-only; no runtime effect |
