---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#197
state: open
updated_at: 2026-07-14T08:48:07+02:00
is_epic: false
labels:
  - "Werkzeuge"
  - "sub-task"
publication: sanitized
---

# PDF-Pipeline produktionsreif machen (generisches PDF-Tooling)

**Parent:** #195
**Typ:** SKILL (Blocker für #195)
**Repo:** Homelab/lydia-tools

## Ziel
Die vorhandene PDF-Pipeline (#6, Phasen 1-3) muss produktionsreif gemacht werden: PDF-Normalisierung, Zusammenführung, Validierung, Metadaten-Extraktion, Fehlerbehandlung, CI/CD.

## DoD
- PDF-Normalisierung (OCR, Vereinheitlichung) implementiert
- PDF-Zusammenführung (Merge mehrerer Dokumente) implementiert
- PDF-Validierung (nicht leer, nicht verschlüsselt, Seiten vollständig) implementiert
- Metadaten-Extraktion (Datum, Betrag, Text) implementiert
- Fehlerbehandlung für korrupte/verschlüsselte/leere PDFs
- CI/CD grün
- Tests für alle o.g. Punkte

**Blockiert:** #195, #201, #202
