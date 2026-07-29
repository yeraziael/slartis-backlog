# Requirements

## Scope

| ID | Requirement | Verification |
|---|---|---|
| JF-REQ-001 | Jellyfin serves films, series, music, music videos and approved YouTube archives. | Library inventory |
| JF-REQ-002 | Audiobooks remain owned by Audiobookshelf; e-books by CWA; home videos are excluded. | Configuration review |
| JF-REQ-003 | Runtime is Docker on Raspberry Pi 5 ARM64 until an approved host migration. | Compose/runtime evidence |
| JF-REQ-004 | Media libraries are NFS-mounted read-only below `/mnt/ro/jellyfin/<library>`. | Mount and container inspection |
| JF-REQ-005 | Jellyfin may write only config, database, cache, metadata and transcode workspace. | Permission tests |
| JF-REQ-006 | Missing NFS mounts prevent a normal Jellyfin start. | Failure test |
| JF-REQ-007 | Internal and external access are supported through the existing frontproxy. | Playback matrix |
| JF-REQ-008 | External hostname is `jellyfin.hl.maier.wtf`; no DNS change is required. | DNS/proxy evidence |
| JF-REQ-009 | Regular authentication, roles and library rights derive exclusively from Keycloak `homelab`. An unauthenticated request redirects to Keycloak; no local profile picker or local credential form is reachable. | Authorization tests |
| JF-REQ-010 | The only local user is break-glass `jellyfin-admin`. | Account audit |
| JF-REQ-011 | Papa is admin; Mama and Papa are `parents` and curators. | Claim mapping tests |
| JF-REQ-012 | Child access follows age/FSK; unrated content is fail-closed. | Negative authorization tests |
| JF-REQ-013 | Curated title grants are permanent until revoked and extend, never reduce, pauschal access. | Grant/revoke tests |
| JF-REQ-014 | At age 18 all regular content is visible; no FSK-21 tier exists. | Birthday transition test |
| JF-REQ-015 | Music is visible to every authenticated household user. | Access matrix |
| JF-REQ-016 | YouTube visibility is channel-to-user/group based; parents can see all child archives. | Access matrix |
| JF-REQ-017 | Children may request channels; parents may approve, reject, alter audience or add channels proactively. | Workflow tests |
| JF-REQ-018 | Approved channels synchronize automatically using ytdl-sub. | Scheduled sync evidence |
| JF-REQ-019 | YouTube originals use best available quality and remain until manual parent-approved deletion. | Download/audit tests |
| JF-REQ-020 | A compatible secondary version is generated only when the original fails the declared Direct-Play profile. | Media probe tests |
| JF-REQ-021 | Secondary versions are reproducible and may be deleted after migration to capable hardware. | Cleanup runbook test |
| JF-REQ-022 | Pi software transcoding is best-effort only; no remote worker is planned. | Resource/failure tests |
| JF-REQ-023 | Jellyfin is the first planned service migration to a stronger future always-on host. | Roadmap review |
| JF-REQ-024 | Configuration/state backups run daily and retain only the newest two verified successes. | Backup inspection |
| JF-REQ-025 | Cache, transcode workspace, media and reproducible secondary versions are excluded from config backup. | Backup manifest |
| JF-REQ-026 | Metadata and file mutation are performed only by controlled external workflows; #113 governs initial cleanup/migration. | Boundary review |
| JF-REQ-027 | No secret, token, private media title inventory or personal viewing history is committed to Git. | Secret/privacy scan |
