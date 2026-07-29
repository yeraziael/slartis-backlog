# Runtime Reconciliation

Reconciled: 2026-07-29

This document records only evidence that was actually produced by the Jellyfin
runtime closeout. It does not treat a healthy deployment, a Compose file, or a
passing smoke test as proof of untested product contracts.

## Evidence Basis

- Operator closeout: [slartis-backlog#129](https://github.com/yeraziael/slartis-backlog/issues/129), marked `COMPLETE` on 2026-07-29.
- Deployment Compose: [Homelab/Architecture PR #120](https://gitea.hl.maier.wtf/Homelab/Architecture/pulls/120), merged as `f6c4d8dbd2067a4fe5644197fc45d53519b8ff53`.
- Runtime smoke alignment: [Homelab/Architecture PR #130](https://gitea.hl.maier.wtf/Homelab/Architecture/pulls/130), merged as `fd797dbbe191c5ed81d34628886d9bedd96ccb4c`.
- Final workflow: Gitea Actions run `978` at source SHA `fd797dbbe191c5ed81d34628886d9bedd96ccb4c`; Audiobookshelf `23/23` and Jellyfin `5/5` passed, with `failed=0` and `skipped=0`.

The closeout records a healthy Jellyfin `10.11.11` ARM64 container, verified
HTTPS and `/health` responses, read-only production-media mounts, writable
synthetic test media, synthetic standard/admin/restricted identities,
restricted denial of the positive test library, and two verified configuration
backup archives. It also records credential-safe evidence publication.

## Workstream Status

| Workstream | Status | Evidenced | Remaining acceptance work |
| --- | --- | --- | --- |
| JF-001 | Partially evidenced | Pi 5, pinned ARM64 image, read-only container mounts, frontproxy/TLS and health endpoint | NFS export/UID/mount facts, fail-closed mount behavior, Keycloak and plugin compatibility |
| JF-002 | Partially evidenced | Pinned container, persistent config, read-only media mounts, no published container port, healthy runtime | Separate ephemeral paths and startup failure when an NFS mount is absent |
| JF-003 | Partially evidenced | `jellyfin.hl.maier.wtf` HTTPS and controlled-media playback smoke | WebSocket, range-request and long-stream acceptance |
| JF-004 | Not started | Break-glass and synthetic runtime identities only | Keycloak claims, roles, regular-user model and rights-removal behavior |
| JF-005 | Blocked by JF-004 | None | FSK, unrated-content, curated-grant and age-transition contracts |
| JF-006 | Partially evidenced | Four intended read-only media paths are mounted | Authorized core-library creation and music visibility contract |
| JF-007 | Blocked by JF-006 and #113 | No production media was touched | Approved, verified batches of at most 100 files |
| JF-008 | Blocked by JF-004 and JF-006 | None | Channel registry, audience grants and approval workflow |
| JF-009 | Blocked by JF-008 | None | ytdl-sub deployment and approved-channel synchronization |
| JF-010 | Blocked by JF-009 | None | Compatibility probing, secondary renditions and grouping |
| JF-011 | Partially evidenced | Two verified configuration archives, documented rollback, service health smoke | Daily two-generation retention, restore tests, replacement-host restore and monitoring |
| JF-012 | Blocked by incomplete dependencies | Bounded post-deployment authorization/playback smoke | Full authorization and client matrices, rollback/restore tests, independent review and frozen manifest |
| JF-013 | Deferred | None | Trigger only after JF-012 and suitable always-on hardware |

## Next Executable Work

JF-001 is the next workstream. It must close the listed fact and compatibility
gaps before JF-002 or JF-003 are considered complete. The already deployed
vertical slice remains available for non-destructive evidence gathering; this
reconciliation neither changes runtime configuration nor authorizes a
deployment.
