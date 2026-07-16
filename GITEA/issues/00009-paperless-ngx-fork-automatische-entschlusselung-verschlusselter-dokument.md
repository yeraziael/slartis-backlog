---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#9
state: open
updated_at: 2026-07-14T21:19:36+02:00
is_epic: false
labels:
  - "Werkzeuge"
  - "clarifying"
publication: sanitized
---

# Paperless-ngx Fork: Automatische Entschlüsselung verschlüsselter Dokumente beim Import

**Blocked by:** #113 (Tests First)

**Goal:** Fork Paperless-ngx to auto-decrypt password-protected PDFs during import using an absender-key store.
**Status:** Design complete, implementation pending.
**Next:** Create `decrypt` Django app with key store model + `pre_consume` import hook using pikepdf.
