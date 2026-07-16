---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#202
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "Aufgaben"
  - "sub-task"
publication: sanitized
---

# Submission Bundle Service + PDF Package Builder

**Parent:** #195
**Typ:** DEV
**Repo:** lydia/home-repo/runtime/medical-submissions/

## Ziel
- Submission Bundle erstellen (Gruppierung zusammengehöriger Dokumente)
- PDF-Package Builder: Kopie der Original-PDFs ins Paket, Zielverzeichnis-Struktur
- Zusammenführung mehrerer PDFs pro Ziel (Beihilfe/Barmenia) via #196
- Zielbestimmung (Beihilfe, Barmenia, beide, manuelle Prüfung)

## DoD
- Bundle-Service implementiert
- Package Builder erzeugt Verzeichnisstruktur pro Ziel
- PDFs werden korrekt kopiert/zusammengeführt
- Zielbestimmung konfigurierbar
- Unit-Tests
- CI/CD grün
