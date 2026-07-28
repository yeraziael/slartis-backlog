# References and Provenance

## Internal
- #109 — canonical Jellyfin epic entry point
- #113 — one-time Library Curator cleanup and migration dependency
- #77 — hostname registry policy
- #55 — Keycloak authorization policy
- `docs/epics/audiobookshelf/` — neighboring media-service boundary and Plan-as-Code precedent
- `docs/epics/playwright/` — Plan-as-Code precedent
- Gitea `Homelab/Architecture` — deployed-state authority for Compose, hosts, networks, mounts, secrets and operational evidence

## Confirmed planning facts
- Primary host decision: Raspberry Pi 5.
- Available NAS for this project: QNAP TS-559 Pro II as storage, not transcoder.
- Synology DS1019+ is not part of the user's available infrastructure.
- CNAME for `jellyfin.hl.maier.wtf` already exists.
- Existing reverse proxy is `frontproxy`.
- NFS is required; SMB/CIFS is unnecessary.
- Planned mount namespace is `/mnt/ro/jellyfin/<library>`; directories are created during implementation.

## Upstream references to reverify during JF-001
- Jellyfin container deployment and ARM64 image support
- Jellyfin Keycloak/OIDC integration mechanism and claim mapping capabilities
- Jellyfin library/version grouping behavior
- Jellyfin client codec and subtitle compatibility
- ytdl-sub configuration schema and supported metadata generation

Upstream facts are time-sensitive and must be pinned to versions and access dates in the implementation PR. This planning file deliberately avoids claiming a specific plugin/version before that verification.
