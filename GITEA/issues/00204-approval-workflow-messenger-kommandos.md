---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#204
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "Aufgaben"
  - "sub-task"
publication: sanitized
---

# Approval Workflow + Messenger-Kommandos

**Parent:** #195
**Typ:** DEV
**Repo:** lydia/home-repo/runtime/medical-submissions/

## Ziel
- Freigabe-Workflow über Messenger: Lydia sendet Freigabeanfrage, Operator approved/denies
- Messenger-Kommandos für Statusabfragen: Einreichungsstatus, offene Fälle, Fristen
- Absorbiert Funktionalität aus #12 (Erstattungsstatus-Analyse)

## DoD
- Approval Workflow implementiert (anfragen → genehmigen/ablehnen)
- Messenger-Kommandos: /status, /open, /einreichung <id>, /bestätigen
- Manuelle Einreichungsbestätigung mit optionalem Datum/Referenz
- Unit-Tests
- CI/CD grün
