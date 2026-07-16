---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#207
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "Aufgaben"
  - "sub-task"
publication: sanitized
---

# Audit-Logging & Fehlerbehandlung

**Parent:** #195
**Typ:** DEV
**Repo:** lydia/home-repo/runtime/medical-submissions/

## Ziel
- Vollständiges Audit-Log aller Statusänderungen und Aktionen
- Strukturierte Fehlerbehandlung (keine stillen Fehler)
- Retry-Logik für externe Dienste (Paperless, Messenger)
- Fehlerzustände werden persistiert und sind einsehbar

## DoD
- Audit-Log implementiert (Zeitstempel, Submission-ID, Aktion, Ausführender, alter/neuer Status, Ergebnis, Fehlercode)
- Fehlerbehandlung für alle in #195 spezifizierten Fehlerfälle
- Keine stillen Verwerfungen
- Unit-Tests für Audit-Log und Fehlerpfade
- CI/CD grün
