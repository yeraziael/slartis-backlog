# Risks — ACP v0.2 Review Fix

## Mitigated Risks

| Risk | Mitigation |
|------|-----------|
| Unversioned action_ref silently registers wrong action | Version now mandatory; pattern rejects unversioned refs |
| Contract without rollback leaves state inconsistent | rollback required; `strategy: none` for irreversible actions |
| Contract without constraints executes indefinitely | constraints required; timeout_seconds mandatory |
| Cron trigger without cron field silently defaults | Schema rejects schedule without `cron` for cron type |
| Secret resolution fails silently | `secret_ref` requires normative resolution check |

## Residual Risks

| Risk | Severity | Mitigation Owner |
|------|----------|-----------------|
| Eddie runtime may not implement all normative MUSTs | Medium | Implementation phase |
| Test harness covers schema only, not runtime | Low | Runtime integration tests planned |
| Existing trigger definitions need migration from optional version | Low | ACP v0.2 is still draft; no production use yet |
