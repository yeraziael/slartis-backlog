# Decisions

## JF-ADR-001 — Primary runtime on Raspberry Pi 5
Status: accepted

Jellyfin starts on the always-on Pi 5 using ARM64 Docker. Limited software transcoding is tolerated but not guaranteed. Jellyfin becomes the first migration candidate for stronger future hardware.

## JF-ADR-002 — Read-only NFS media
Status: accepted

QNAP media is mounted through NFS only under `/mnt/ro/jellyfin/<library>`. Jellyfin cannot mutate media. SMB/CIFS is excluded.

## JF-ADR-003 — Separate libraries
Status: accepted

Films, series, music, music videos and generated YouTube audience libraries are separate. Home videos and mixed libraries are excluded.

## JF-ADR-004 — Keycloak owns regular authorization
Status: accepted

Keycloak controls all regular users, roles and library entitlements. Papa is admin. Mama and Papa are parents/curators. The only local user is break-glass `jellyfin-admin`.

## JF-ADR-005 — Age and curation model
Status: accepted

FSK grants pauschal child access. Missing ratings fail closed. Parents can add permanent, revocable title/group grants. At 18 all regular media is visible.

## JF-ADR-006 — Music open to all
Status: accepted

Music does not use age filtering and is visible to every authenticated household user.

## JF-ADR-007 — ytdl-sub rather than Tube Archivist
Status: accepted

YouTube downloads use declarative ytdl-sub subscriptions. Jellyfin remains the only playback interface and no second archive server/database is introduced.

## JF-ADR-008 — Audience-set YouTube libraries
Status: accepted

Stable Channel IDs map to user/group audiences. Parents inherit visibility into child archives. Children may request channels; parents decide and may add channels proactively.

## JF-ADR-009 — Original quality plus conditional compatibility version
Status: accepted

Download the best available original. Generate a second version only when the original is incompatible with the declared Pi/client Direct-Play profile. The original remains canonical.

## JF-ADR-010 — External and internal access through frontproxy
Status: accepted

Use existing `jellyfin.hl.maier.wtf` CNAME and attach the container to `frontproxy`. No direct public container port.

## JF-ADR-011 — Two-generation verified backup
Status: accepted

Back up application state daily and retain only the two newest verified successes, analogous to Paperless. Reproducible data and media are excluded.

## JF-ADR-012 — Initial migration delegated to #113
Status: accepted

The Library Curator is a one-time controlled cleanup/migration project using batches of at most 100 files. No permanent curator service is planned.
