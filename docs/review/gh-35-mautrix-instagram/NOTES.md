# GH-35 Scope And Risks

## Delivered

- Separate Instagram Compose service and persistent path
- Dedicated database, appservice ID, bot, ghost namespace, and registration path
- Digest-pinned `ig-v26.07` multi-arch image with explicit ARM64 selection
- Full config generated from the pinned image and converted to safe Homelab
  placeholders
- Debug and file logging disabled to reduce credential exposure risk
- Focused test registered in manifest-generated Gitea PR CI
- Runbook with registration, account-risk, and resource-measurement contracts

## Not Performed

- No Pi deployment or live Instagram container creation
- No live database or appservice registration
- No Synapse restart or configuration rollout
- No Instagram login or account cookie handling
- No DNS, firewall, proxy, secret, or external-account mutation

## Review Risks

- Meta Terms-of-Service compliance remains unknown.
- Meta may restrict the account or require checkpoints.
- Cookie login material is high-value and must stay runtime-only.
- The Synapse registration path is prepared in source but must only be deployed
  after the real registration file exists.
- Resource limits are proposed contract values, not measured Instagram runtime
  consumption; CPU, RSS, Swap, and Storage require later deployment evidence.
- Matrix end-to-bridge encryption support does not establish Instagram transport
  encryption.
