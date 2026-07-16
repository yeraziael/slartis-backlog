---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#200
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "Werkzeuge"
  - "sub-task"
publication: sanitized
---

# Medizinische Dokumentklassifikation & Metadatenextraktion

**Parent:** #195
**Typ:** SKILL
**Repo:** Homelab/lydia-tools

## Ziel
Dokumenttyp-Klassifikation (Rechnung, Rezept, Verordnung, Bescheid, etc.) und Extraktion von:
- Rechnungsdatum, Rechnungsnummer, Bruttobetrag
- Rechnungsaussteller
- Leistungszeitraum
- Patientenzuordnung (unsicher → manual review)
- Bescheiddaten (Aktenzeichen, anerkannter Betrag, Erstattungsbetrag)

Nutzung der PDF-Pipeline (#196) für Metadaten + Ollama für unsichere Fälle.

## DoD
- Dokumenttyp-Klassifikation implementiert (regelbasiert + LLM-Fallback)
- Metadaten-Extraktion implementiert
- Unsichere Ergebnisse werden als "needs_review" markiert
- Tests mit anonymisierten Beispieldokumenten
- CI/CD grün
