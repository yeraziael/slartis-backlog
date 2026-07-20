# Scope And Risks

## Verified Root Cause

- Synapse emitted HTTP 429 with limiter `rc_joins_per_room` for the failed join.
- The affected portal has 921 current joined memberships and 1841 total
  membership events; two small portals with two and three joined members worked.
- Synapse's documented default burst is 10 joins per room.
- Synapse records successful joins in the shared room bucket, including joins
  observed while a bridge imports remote members.

## Delivered

- Retains the sustained per-room rate of one join per second.
- Raises only the per-room burst to 2048 for large initial portal imports.
- Adds a regression test that rejects the default burst of 10.
- Documents the measured exception and required portal-join blackbox.

## Security Tradeoff

One room may accept a larger short burst of joins. The sustained rate, user join
limits, registration closure, private-room boundary, and other Synapse limits are
unchanged. The configured burst covers the measured 921-member portal and a
maximum-size bridge group plus service membership without disabling the limiter.

## Not Performed

- No production configuration, container, database, registration, or secret was
  changed by the source patch.
- Eddie auto-merged the source after green Gitea CI and before external review
  acceptance. No Synapse recreation or operator blackbox was performed.
