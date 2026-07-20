# Review Instructions

- Review target is Gitea PR #51 at exact head
  `29705bda2db24da7341b1290a83efd92cdf364c5`.
- Confirm `rc_joins_per_room.per_second` remains at the Synapse default `1.0`.
- Confirm only `rc_joins_per_room.burst_count` increases, from `10` to `2048`.
- Confirm the hardening test rejects the previous burst and pins both values.
- Evaluate the bounded security tradeoff described in `NOTES.md`.
- Eddie auto-merged the source as release
  `77d69f7f051f09d330b875fcf17263fc904f7443` before external acceptance.
- Approval permits deployment eligibility only; it does not itself authorize
  production Synapse recreation. Requested changes require a corrective PR.
- Runtime deployment must use the merged release, create a backup, and verify
  Synapse restart count plus existing bridge regressions.
