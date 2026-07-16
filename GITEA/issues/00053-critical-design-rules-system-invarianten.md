---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#53
state: closed
updated_at: 2026-06-30T16:01:52+02:00
is_epic: false
labels:
  - "project:homelab-agenten-ausbau"
publication: sanitized
---

# CRITICAL Design Rules — System-Invarianten

## Ursprung
Issues #40–#41 (Telegram: <operator>)

## Ziel
Systemweite Invarianten als dokumentierte Regeln + automatisierte Checks:
- Rule 1: Slarti liest niemals Code tief — nur Diffs, File-Listen, Testergebnisse
- Rule 2: Workers sind die einzigen Code-Resolver
- Rule 3: Bei Unsicherheit: Scope reduzieren, nicht erweitern
- Rule 4: Mehrere Lösungen → wähle (1) wenig Code, (2) wenig Dependencies, (3) deterministische Tests
- Rule 5: Nicht vorzeitig optimieren, nicht über Test-Requirements hinaus generalisieren

## Teilaufgaben
- [ ] Design-Rules als Dokument festhalten
- [ ] PR-Checklist mit Rule-Compliance
- [ ] Linter/Validator für Rule-Verstöße (optional)
