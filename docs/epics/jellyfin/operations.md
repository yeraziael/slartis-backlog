# Operations

## Install
1. Verify NFS exports and create planned mountpoints during implementation.
2. Mount all libraries below `/mnt/ro/jellyfin/` and validate read-only semantics.
3. Create persistent Jellyfin state paths and ephemeral cache/transcode paths.
4. Verify that `/home/michael/.creds/breakglassAdmin/jellyfin` exists on the host with restrictive ownership and permissions; never print or copy its content into logs or repository files.
5. Provision or verify the sole local break-glass account named `admin` without creating additional local household users.
6. Deploy pinned ARM64 container configuration.
7. Attach to `frontproxy` and configure `jellyfin.hl.maier.wtf`.
8. Configure Keycloak integration and claim mappings.
9. Create libraries only after mount and authorization tests pass.

## Upgrade
- Back up current state first.
- Verify image/plugin compatibility and migrations.
- Upgrade in a controlled window.
- Run login, authorization, library and playback smoke tests.
- Roll back on database, plugin, SSO or playback regression.

## Backup
Daily backup includes configuration, database, users/settings, library definitions, required plugins and non-reproducible local metadata. Exclude cache, transcode workspace, media, reproducible compatibility renditions and the host-side break-glass password file. Keep only the latest two verified successes.

## Restore
- Restore into an isolated test instance or new host.
- Reconnect the same logical read-only library paths.
- Re-establish the host-side break-glass secret separately; it is not restored from the Jellyfin application backup.
- Verify the local `admin` account without exposing the password in evidence.
- Verify database integrity, users, permissions, plugins and representative playback.
- Record evidence and recovery duration.

## Incident handling
- Missing NFS: stop/keep stopped; never rescan empty directories.
- Keycloak outage: use the documented local `admin` account only for administration; do not create temporary local household users.
- Break-glass use: record purpose and time, restore normal SSO operation, then rotate the password stored at `/home/michael/.creds/breakglassAdmin/jellyfin`.
- Corrupt state: preserve evidence, restore newest verified backup, then older backup if necessary.
- Storage pressure: prune cache/transcodes first; do not auto-delete media.

## Host migration
Jellyfin is the first candidate for a stronger always-on host. Preserve logical mount paths, restore state, provision a new host-side break-glass secret at the documented path or an explicitly approved successor path, validate claims and playback, then switch proxy routing. Pi-specific compatibility renditions may be removed only after successful client testing and approved cleanup.