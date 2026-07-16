---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#218
state: closed
updated_at: 2026-07-14T23:18:09+02:00
is_epic: false
labels:
  - "FLASH_FREE"
  - "sub-task"
publication: sanitized
---

# Synapse PostgreSQL Daten- und Volume-Konzept

Parent: #212. Depends on: #217.

## FLASH_FREE packet
Repo: `architecture`; branch: `feat/synapse-storage-contract`; create `docs/matrix/storage-and-retention.md` and update `pi/compose/synapse-poc.yml` only if required.
Implement: document and encode separate DB, media, config, signing-key and backup paths; owners, quotas, retention and growth alarms. PostgreSQL stays private.
Tests first: `pi/tests/test_synapse_storage.sh` checks required mounts, no host DB port, no secret-bearing paths in assets.
Do not: create host directories or touch data.
Done: restore inputs are enumerated and compatible with #235/#241.

## Vekling-Ausfuehrung

Worktree: <local-path-redacted>

Vor dem Editieren: `git status --short --branch` im Worktree.

Lokaler Nachweis: Fuehre jeden im Paket genannten fokussierten Test aus dem Repository-Root aus. Anschliessend aus demselben Worktree zwingend:

    make ci
    git diff --check

Ein Test aus einem anderen Verzeichnis oder nur ein zusammengefasster Testbericht gilt nicht als Nachweis.
