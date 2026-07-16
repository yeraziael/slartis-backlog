---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#208
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "sub-task"
publication: sanitized
---

# Integrationstests mit anonymisierten medizinischen Testdokumenten

**Parent:** #195
**Typ:** TEST

## Ziel
Integrationstests für die gesamte Pipeline:
- Paperless-Erkennung → Klassifikation → Bundle → Validierung → Freigabe → Export
- Testfälle: mehrere Familienmitglieder, Teil-/Voll-/Nichterstattung, jahresübergreifend
- Anonymisierte Testdokumente als Fixtures

## DoD
- Integrationstests für End-to-End-Pipeline
- Testfälle für alle Statusübergänge
- Testdokumente anonymisiert (keine produktiven Gesundheitsdaten)
- CI/CD grün
