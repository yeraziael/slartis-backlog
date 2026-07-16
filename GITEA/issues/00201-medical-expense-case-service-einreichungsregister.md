---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#201
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "Aufgaben"
  - "sub-task"
publication: sanitized
---

# Medical Expense Case Service + Einreichungsregister

**Parent:** #195
**Typ:** DEV
**Repo:** lydia/home-repo/runtime/medical-submissions/

## Ziel
Kern-Service für medizinische Kostenfälle:
- MedicalExpenseCase anlegen, aktualisieren, Status verwalten
- Einreichungsregister für Beihilfe Bund und Barmenia
- Statusübergänge (detected → classified → needs_review → ready → submitted → reimbursed → closed)
- Persistente Speicherung (JSON-Datei oder SQLite)

## DoD
- MedicalExpenseCase CRUD implementiert
- Einreichungsregister (pro Kostenträger) implementiert
- Status-Machine implementiert
- Persistente Speicherung vorhanden
- Unit-Tests für Statusübergänge und CRUD
- CI/CD grün
