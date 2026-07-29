# Contracts

## Media immutability
Jellyfin receives read-only media. Delete, move, rename and metadata-sidecar mutation through Jellyfin are prohibited. External writers must be explicit, approved and audited.

Library Curator owns migration; ytdl-sub owns channel downloads. Both writers
must conform to [ingest-contract.md](ingest-contract.md); Jellyfin defines that
contract but does not execute either workflow.

## Availability
- Missing media mounts: fail closed before normal application start.
- Keycloak unavailable: existing sessions may follow documented token lifetime; new regular login must not fall back to local users.
- Break-glass access: local `jellyfin-admin` only, restricted and tested.
- Metadata provider failure: playback of existing indexed media remains available where possible; no destructive reconciliation.

## Authorization
- Authentication alone grants no library access.
- Missing/unmapped claims grant no expanded access.
- Unrated films/episodes are hidden from children unless curated.
- FSK permits pauschal access; curated grants add individual titles or defined groups.
- Grants remain until revoked.
- At 18, the regular catalogue becomes visible automatically.

## YouTube archive
- Approved channels sync automatically.
- Parents can approve/reject requests, change audience, or add channels proactively.
- Removing a channel stops future downloads but does not delete existing media.
- Existing media is deleted only after a manual parent-approved action.
- Best available original is canonical.
- Compatibility rendition is generated only when needed and never replaces the original.

## Backup
- Run daily.
- Keep the newest two verified successful state backups.
- Never evict a valid backup for an incomplete or unverified run.
- Restore evidence is required before production acceptance and after material schema/plugin changes.
