---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#203
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "Aufgaben"
  - "sub-task"
publication: sanitized
---

# Validation Engine + Dublettenprüfung + Manifest Generator

**Parent:** #195
**Typ:** DEV
**Repo:** lydia/home-repo/runtime/medical-submissions/

## Ziel
- Validierung der Submission Bundles (PDF valide, nicht leer, Seiten vollständig, Metadaten vorhanden)
- Dublettenprüfung (SHA-256, Paperless-ID, Rechnungsnummer + Betrag + Patient)
- Manifest Generator (pro Zielpaket: manifest.json + sha256sums.txt)

## DoD
- Validation Engine mit konfigurierbaren Checks implementiert
- Dublettenprüfung implementiert (Erkennung, Warnung, Block)
- Manifest Generator implementiert (JSON + SHA-256)
- Unit-Tests für Validierung, Dubletten, Manifest
- CI/CD grün
