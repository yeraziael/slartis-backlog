---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#198
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "Systemarchitektur"
  - "sub-task"
publication: sanitized
---

# ADR: Architektur, Datenmodell und Threat Model für medizinische Kostenverwaltung

**Parent:** #195
**Typ:** ADR

## Ziel
Architekturentscheidung für die medizinische Kostenverwaltung treffen:
- Datenmodell (MedicalExpenseCase, Submission, Reimbursement, TaxExpense) finalisieren
- Statusmodell aller Entitäten definieren
- Komponentenarchitektur (Module, Schnittstellen, Datenflüsse)
- Threat Model & Datenschutzkonzept für Gesundheitsdaten
- Entscheidung: eigenes medizinisches Subsystem in `lydia/home-repo` vs. separates Repo

## DoD
- ADR dokumentiert
- Datenmodell als JSON-Schema oder Python-Dataclasses spezifiziert
- Threat Model dokumentiert
- Datenschutz- und Secret-Konzept dokumentiert
- Status-Übergangsdiagramm dokumentiert
