# Interfaces

## NFS
- Protocol: NFS only; SMB/CIFS is out of scope.
- Host paths: `/mnt/ro/jellyfin/<library>`.
- Mounts are read-only for Jellyfin.
- systemd/Compose ordering must ensure mounts exist before container start.
- A sentinel or mountpoint verification must prevent startup against empty local directories.
- UID/GID, export paths and mount options are implementation-time facts recorded in Gitea, not invented here.

## Reverse proxy and TLS
- Hostname: `jellyfin.hl.maier.wtf`.
- CNAME already exists.
- Container joins `frontproxy`; direct public container-port exposure is forbidden.
- Proxy must support WebSockets, byte-range requests, long-lived streams and large responses.

## Keycloak
Claims/groups must express:
- `jellyfin-admin`: Papa only, regular SSO account.
- `parents`: Mama and Papa; also curator rights.
- child age/FSK tier.
- curated title grants.
- YouTube audience memberships.

Rights removed in Keycloak must be removed at next login/token refresh; stale expansion must fail closed.

## Clients
Acceptance matrix must cover at least:
- Web browser
- iPhone/iPad
- tvOS/Apple TV where present
- other actual household clients discovered during implementation

Each client records Direct Play, Direct Stream, subtitle behavior, audio compatibility and fallback outcome.

## ytdl-sub
A versioned channel registry uses stable Channel IDs, not mutable names/handles. It generates subscriptions, target paths and audience-library mappings. Example schema:

```yaml
channels:
  - channel_id: UC_EXAMPLE
    source: https://www.youtube.com/@example
    audience:
      users: [ayden]
```

Parents implicitly receive access to every child audience. Existing downloads are never silently moved when audience changes; a reviewed migration proposal is required.

## Library Curator
Issue #113 owns initial cleanup and migration. It works in approved batches of at most 100 files, preserves sources until verification, and is not a permanent service.
