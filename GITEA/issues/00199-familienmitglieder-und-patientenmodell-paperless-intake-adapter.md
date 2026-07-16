---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#199
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "Aufgaben"
  - "sub-task"
publication: sanitized
---

# Familienmitglieder- und Patientenmodell + Paperless Intake Adapter

**Parent:** #195
**Typ:** DEV
**Repo:** lydia/home-repo/runtime/medical-submissions/

## Ziel
- Familienmitglieder-Modell (Mehrpersonenfähigkeit ab MVP)
- Paperless-NGX API-Adapter: Pollt neue Dokumente, filtert medizinische Typen
- Dokument-Metadaten aus Paperless (Correspondent, Tags, Custom Fields, OCR-Text) übernehmen

## DoD
- Familienmitglieder-Tabelle/Config mit Name, Beihilfesatz, Versicherung
- Paperless Intake Adapter implementiert (API-Zugriff, Polling, Filter)
- Neue medizinische Dokumente werden erkannt und als "detected" markiert
- Unit-Tests für Adapter und Familienmodell
- CI/CD grün
