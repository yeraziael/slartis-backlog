# Jellyfin Plan-as-Code Epic

Issue: #109
Status: runtime vertical slice reconciled; product workstreams remain open
Authority: this directory defines WHAT/WHY; deployed facts remain authoritative in `Homelab/Architecture` on Gitea.

## Objective
Operate Jellyfin as the household media platform for films, series, music, music videos and person-bound YouTube archives. Audiobooks remain in Audiobookshelf; e-books remain in CWA; home videos are out of scope.

## Canonical decisions
- Primary host: Raspberry Pi 5, ARM64, Docker.
- Normal playback: Direct Play / Direct Stream.
- Pi software transcoding is a limited fallback only; no remote transcoding worker.
- Jellyfin is the first migration candidate for a future more powerful always-on host.
- Media is mounted read-only via NFS below `/mnt/ro/jellyfin/<library>`.
- External hostname: `jellyfin.hl.maier.wtf`; existing CNAME; container joins `frontproxy`.
- Regular authentication and authorization are fully derived from Keycloak.
- Only local account: break-glass `jellyfin-admin`.
- Papa is Jellyfin admin; Mama and Papa are `parents` and curators.
- Children receive age-based access plus curated permanent, revocable title grants.
- Music is open to all users.
- YouTube channel visibility is person/group-bound and managed declaratively.
- Daily configuration backup; retain only the last two verified successful backups.

## Document map
- [requirements.md](requirements.md)
- [architecture.md](architecture.md)
- [interfaces.md](interfaces.md)
- [contracts.md](contracts.md)
- [security.md](security.md)
- [operations.md](operations.md)
- [testing.md](testing.md)
- [ci.md](ci.md)
- [roadmap.md](roadmap.md)
- [backlog.md](backlog.md)
- [decisions.md](decisions.md)
- [references.md](references.md)
- [runtime-reconciliation.md](runtime-reconciliation.md)
- [plan.yaml](plan.yaml)

## Working rule
#109 is the only GitHub entry point. Do not create planning child issues. Plan changes and implementation progress are committed through pull requests referencing a stable `JF-*` workstream ID from `plan.yaml`.

## Non-goals
- No home-video library.
- No audiobook or e-book ownership.
- No media mutation by Jellyfin.
- No SMB/CIFS.
- No Tube Archivist service.
- No guaranteed hardware transcoding on the Pi.
- No runtime mutation as part of this planning commit.
