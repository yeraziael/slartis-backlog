---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#205
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "Aufgaben"
  - "sub-task"
publication: sanitized
---

# Export Adapter (iPhone-Bereitstellung)

**Parent:** #195
**Typ:** DEV
**Repo:** lydia/home-repo/runtime/medical-submissions/

## Ziel
Bereitstellung der freigegebenen Einreichungspakete für den Zugriff vom iPhone.
Austauschbare Transportmethode: initial lokaler Exportordner, später iCloud/WebDAV/Nextcloud.

## DoD
- Lokaler Export-Adapter implementiert (konfigurierbarer Pfad)
- Temporäre Dateien werden nach konfigurierbarer Frist gelöscht
- Berechtigungen restriktiv
- Unit-Tests
- CI/CD grün
