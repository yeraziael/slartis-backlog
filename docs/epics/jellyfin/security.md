# Security

## Identity and roles
- Keycloak is the source of truth for every regular identity, role and library entitlement.
- Papa: Jellyfin administrator and parent/curator.
- Mama: parent/curator, not system administrator.
- Children: age-derived access plus explicit curated grants.
- Local account `admin`: break-glass only; no daily use.

## Fail-closed rules
- Missing or invalid age/FSK information hides content from children.
- Missing or malformed authorization claims grant no expanded access.
- Failed NFS validation blocks startup.
- SSO failure must not expose a local-account fallback to regular users.
- The public service path must not expose a local profile picker or local
  credential form. Unauthenticated regular users are redirected to Keycloak
  `homelab` instead.

## Break glass
- The only local Jellyfin account is named `admin`.
- Its password is stored on the Raspberry Pi host at `/home/michael/.creds/breakglassAdmin/jellyfin`.
- The secret file content MUST NOT be committed, copied into Compose, emitted to logs or included in evidence artifacts.
- The implementation MUST verify restrictive ownership and permissions before accepting the deployment.
- The secret is read only where required for initial provisioning, controlled recovery or an approved rotation workflow.
- Restrict direct use as far as Jellyfin/proxy capabilities allow.
- Test the account on a defined schedule and after authentication changes.
- Audit every use and rotate the password after emergency use.

## Network
- Public traffic enters only through `frontproxy` with TLS.
- Container ports are not publicly published.
- NFS exposure is limited to required hosts/networks.
- Admin endpoints follow the same SSO and authorization model.

## Plugins and supply chain
- Use an explicit plugin allowlist.
- Pin container image versions/digests where operationally supported.
- Review plugin compatibility and security before upgrade.
- No plugin may become an undocumented authorization source.

## Privacy
- Do not commit media titles, watch history, child preferences, secrets or token material.
- Test fixtures use synthetic names and media.
- Logs should avoid unnecessary path/title disclosure and follow retention policy.
