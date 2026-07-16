---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#206
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "Aufgaben"
  - "sub-task"
publication: sanitized
---

# Erstattungszuordnung + Eigenanteilsberechnung + Steuerliche Jahresauswertung

**Parent:** #195
**Typ:** DEV
**Repo:** lydia/home-repo/runtime/medical-submissions/

## Ziel
- Beihilfebescheide und Barmenia-Abrechnungen erkennen und zuordnen (via #199)
- Erstattungsbeträge extrahieren und MedicalExpenseCase zuordnen
- Eigenanteil berechnen: Rechnungsbetrag - Beihilfe - Barmenia = Eigenanteil
- Offene Fälle, Teil- und Nichterstattungen identifizieren
- Steuerliche Jahresliste: nicht erstattete Kosten pro Jahr als CSV/JSON/PDF
- Datums- und Fristen-Übersicht

## DoD
- Erstattungszuordnung implementiert (automatisch + manuelle Korrektur)
- Eigenanteilsberechnung korrekt für Teil-/Voll-/Nichterstattung
- Steuerliche Jahresauswertung als CSV, JSON und PDF exportierbar
- Offene-Fälle-Übersicht implementiert
- Unit-Tests für Berechnungen
- CI/CD grün
