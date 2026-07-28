# Executable Backlog

This is a Plan-as-Code backlog, not an instruction to create child issues. Execution is tracked through PRs referencing #109 and the stable IDs below.

## JF-001 — Confirm deployed facts
Dependencies: none

Acceptance:
- Pi, QNAP NFS, frontproxy and Keycloak facts are evidenced in Gitea.
- No invented export path, UID/GID, port or plugin capability remains.
- Upstream ARM64 and SSO/plugin compatibility is reverified.

## JF-002 — Build safe Pi deployment
Dependencies: JF-001

Acceptance:
- Pinned Jellyfin container starts on Pi 5.
- Persistent and ephemeral paths are separated.
- Media mounts are read-only and startup fails closed when absent.
- Direct public container access is unavailable.

## JF-003 — Integrate frontproxy and TLS
Dependencies: JF-002

Acceptance:
- `jellyfin.hl.maier.wtf` works internally and externally.
- WebSockets, range requests and long streams pass tests.
- Existing DNS is unchanged.

## JF-004 — Implement Keycloak authorization
Dependencies: JF-002

Acceptance:
- Papa admin, parents/curators and child tiers derive from claims/groups.
- Local regular users do not exist.
- Break-glass `jellyfin-admin` is tested.
- Removed rights fail closed.

## JF-005 — Implement parental access model
Dependencies: JF-004

Acceptance:
- FSK pauschal access works.
- Unrated content is hidden from children.
- Permanent revocable curated grants work.
- 18th-birthday transition grants full regular visibility.

## JF-006 — Create core libraries
Dependencies: JF-002, JF-004

Acceptance:
- Films, series, music and music-videos use separate paths/libraries.
- No home-video or mixed library exists.
- Music is visible to all authenticated users.

## JF-007 — Execute controlled media migration
Dependencies: JF-006, issue #113

Acceptance:
- Batches contain at most 100 files.
- Sources remain untouched until verification and operator approval.
- Jellyfin never becomes the media mutator.

## JF-008 — Implement YouTube registry and approvals
Dependencies: JF-004, JF-006

Acceptance:
- Stable Channel IDs map declaratively to users/groups.
- Child requests and parent approvals/rejections work.
- Parents may add channels proactively.
- Parents see every child archive; children see only entitled archives.

## JF-009 — Deploy ytdl-sub pipeline
Dependencies: JF-008

Acceptance:
- Approved channels sync automatically in best available quality.
- Removing a channel stops future downloads without deleting existing files.
- Files remain until manual parent-approved deletion.

## JF-010 — Add conditional compatibility renditions
Dependencies: JF-009

Acceptance:
- Compatibility is probed before encoding.
- Secondary rendition is created only when needed.
- Original is never replaced.
- Jellyfin groups both as one item.

## JF-011 — Backup, restore and monitoring
Dependencies: JF-002, JF-004

Acceptance:
- Daily backup retains exactly the two newest verified successes.
- Cache, transcodes, media and reproducible renditions are excluded.
- Restore to replacement host succeeds.
- Storage, mount, service and resource failures are observable.

## JF-012 — Client and production acceptance
Dependencies: JF-003, JF-005, JF-006, JF-007, JF-010, JF-011

Acceptance:
- Authorization and playback matrices pass.
- Rollback and break-glass runbooks pass.
- Independent review finds no blocking issue.
- Execution manifest is frozen and hashed.

## JF-013 — Future stronger-host migration
Dependencies: JF-012; trigger: suitable always-on hardware available

Acceptance:
- State and stable mount paths migrate successfully.
- Proxy and Keycloak behavior remain unchanged.
- Hardware transcoding is tested, not assumed.
- Pi-specific renditions are removed only after approved validation.
