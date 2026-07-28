# Testing

## Static validation
- Markdown links and Mermaid syntax
- Stable ID uniqueness
- YAML schema validation
- Secret and private-metadata scan
- No undocumented child issues or runtime claims

## Container and storage
- ARM64 image starts on Pi 5
- State paths writable; media paths read-only
- Delete/rename attempts from container fail
- Missing NFS mount blocks startup
- Network interruption and recovery do not trigger destructive library reconciliation

## Authentication and authorization
Test at least:
- Papa: admin + all libraries
- Mama: parent/curator + all content, no system administration
- Child below rating: denied
- Child at rating: allowed
- Unrated title: denied to child
- Curated title: allowed until revoked
- Revoked title: denied again
- User reaching 18: full regular catalogue
- Music: available to all
- YouTube audience isolation
- Parents: access to all child YouTube libraries
- Removed Keycloak role: access removed at refresh/login
- Break-glass login works independently of Keycloak

## Playback matrix
For each actual client, test representative H.264/H.265/AV1 where present, AAC/AC3/EAC3 where present, subtitles, 1080p and available 4K samples. Record Direct Play, Direct Stream, software transcode, failure and resource use.

## YouTube pipeline
- Stable Channel ID mapping
- Child request and parent approval/rejection
- Proactive parent assignment
- Automatic ytdl-sub sync
- Best-quality original retained
- Secondary rendition only for incompatible originals
- Versions grouped as one item
- Channel removal stops new sync but retains files
- Manual deletion is audited

## Recovery
- Newest backup restore
- Older retained backup restore
- Restore to replacement host
- Proxy and Keycloak reconnection
- No media backup dependency
