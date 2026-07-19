# GH-39 Scope And Risks

## Delivered

- Versioned operations runbook for Signal, Telegram, and WhatsApp
- Start/stop, health, isolation, resource, and regression gates
- Restricted backups for dedicated databases, persistent state, and registrations
- Deployment and rollback bound directly to clean, detached reviewed checkouts
- Active Synapse config, source template, and appservice-list backup/restore
- Per-bridge restart and health gate before the next bridge is stopped
- Checksum verification, restore, digest-pinned upgrade, and rollback contracts
- Safe log-evidence rules and operator blackbox procedure
- Focused test registered in manifest-generated Gitea PR CI

## Not Performed

- No live bridge, database, registration, Synapse, or account mutation
- No backup or restore was executed
- No WhatsApp deployment or QR account linking
- No runtime secrets or raw logs were read or published

## Review Risks

- This PR defines an operator contract; GH-40 must still execute it against the
  Pi5 and produce redacted runtime evidence.
- Registration and state archives contain credentials and require restrictive
  permissions and local handling.
- Restore and rollback remain unproven until an authorized operator exercise.
- WhatsApp bot usability and Epic GH-19 remain blocked until GH-40 completes.
