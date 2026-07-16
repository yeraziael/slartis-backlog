---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#177
state: open
updated_at: 2026-07-14T00:35:49+02:00
is_epic: false
labels:
  - "Aufgaben"
  - "project:homelab-agenten-ausbau"
  - "ready"
  - "sub-task"
publication: sanitized
---

# Verify first nightly Eddie backup run

## Ziel

Die ersten vollstaendigen naechtlichen Pi-Backoffice-Laeufe nach dem Eddie-Cutover verifizieren, bevor Eddie als 100 Prozent produktiv gilt.

## Zu pruefen

- `ops.backup.paperless-francine` nach 01:00 erfolgreich abgeschlossen; aktuelles Exportarchiv vorhanden.
- `ops.backup.paperless` nach 03:00 erfolgreich abgeschlossen; aktuelles Exportarchiv vorhanden.
- `ops.backup.gitea` nach 04:00 erfolgreich abgeschlossen; aktueller Gitea-Dump vorhanden.
- `ops.backup.pi-boot` nach 04:15 erfolgreich abgeschlossen; Archiv und SHA-256-Pruefung vorhanden.
- Keine neue Eddie-Eskalation oder fehlgeschlagene Ausfuehrung aus diesen Schedules.
- Queue nach dem Fenster leer; fünf Templates bleiben aktiviert.

## Definition of Done

- Jeder der vier Backup-Jobs hat einen terminalen Status `completed` mit aktuellem Zeitstempel.
- Die erzeugten Artefakte sind lesbar und haben plausible, neue Zeitstempel.
- Eddie-Queue hat keine neuen `failed` oder `escalated` Jobs.
- Erst danach darf ein separater Cleanup der historischen Eskalationen vorbereitet werden; bis dahin bleiben sie als Audit-Historie erhalten.
