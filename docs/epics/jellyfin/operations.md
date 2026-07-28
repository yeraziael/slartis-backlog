# Operations

## Install
1. Verify NFS exports and create planned mountpoints during implementation.
2. Mount all libraries below `/mnt/ro/jellyfin/` and validate read-only semantics.
3. Create persistent Jellyfin state paths and ephemeral cache/transcode paths.
4. Deploy pinned ARM64 container configuration.
5. Attach to `frontproxy` and configure `jellyfin.hl.maier.wtf`.
6. Configure Keycloak integration and claim mappings.
7. Create libraries only after mount and authorization tests pass.

## Upgrade
- Back up current state first.
- Verify image/plugin compatibility and migrations.
- Upgrade in a controlled window.
- Run login, authorization, library and playback smoke tests.
- Roll back on database, plugin, SSO or playback regression.

## Backup
Daily backup includes configuration, database, users/settings, library definitions, required plugins and non-reproducible local metadata. Exclude cache, transcode workspace, media and reproducible compatibility renditions. Keep only the latest two verified successes.

## Restore
- Restore into an isolated test instance or new host.
- Reconnect the same logical read-only library paths.
- Verify database integrity, users, permissions, plugins and representative playback.
- Record evidence and recovery duration.

## Incident handling
- Missing NFS: stop/keep stopped; never rescan empty directories.
- Keycloak outage: use documented break-glass only for administration; do not create temporary local household users.
- Corrupt state: preserve evidence, restore newest verified backup, then older backup if necessary.
- Storage pressure: prune cache/transcodes first; do not auto-delete media.

## Host migration
Jellyfin is the first candidate for a stronger always-on host. Preserve logical mount paths, restore state, validate claims and playback, then switch proxy routing. Pi-specific compatibility renditions may be removed only after successful client testing and approved cleanup.
