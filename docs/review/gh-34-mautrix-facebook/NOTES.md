# GH-34 Scope And Risks

## Delivered

- Digest-pinned, ARM64-specific internal Compose contract
- Full config generated from the selected v26.07 image and converted to safe
  Homelab placeholders
- Dedicated database, bot, ghost namespace, persistent path, and registration
  path
- Matrix encryption supported but not forced
- Focused test registered in manifest-generated Gitea PR CI
- Versioned runbook including the current `/docker-run.sh -g` image behavior

## Not Performed

- No Pi deployment or live container creation
- No live database or appservice registration
- No Synapse restart or configuration rollout
- No Meta login or account cookie handling
- No DNS, firewall, proxy, secret, or external-account mutation

## Review Risks

- Meta Terms-of-Service compliance remains unknown.
- Meta may restrict the account for suspicious activity.
- Cookie login material is high-value and must stay runtime-only.
- The Synapse registration path is prepared in source but must only be deployed
  after the real registration file exists.
- Resource limits are proposed contract values, not measured Facebook runtime
  consumption.
