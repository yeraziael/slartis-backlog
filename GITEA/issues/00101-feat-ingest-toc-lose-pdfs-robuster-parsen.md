---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#101
state: closed
updated_at: 2026-07-03T09:37:31+02:00
is_epic: false
labels:
  []
publication: sanitized
---

# feat(ingest): ToC-lose PDFs robuster parsen

## Hintergrund
Docs ohne Inhaltsverzeichnis-Marker (z.B. 5564, 5566) lieferten nur 3 generische Topics via Phase B single-pass LLM.

## Geliefert (gemerged)
- Phase 2 Fallback in _ingest_extract_headings: Subsection-Scan via ^[0-9]+\\.[0-9]+ + Wort-Filter + monotone Dedup
- Phase 3: Top-Level-Straggler aus Major-Lücken (Majors ohne Subsections)
- Merge: Numerischer Key-Sort für korrekte Dokument-Reihenfolge
- Fix: echo -e Blankzeilen-Bug
- Fix: Doppelte Extraction (chunked ueberschrieb Phase 2b)
- Fix: INGEST_MAX_CHARS=300000 (war 12000)

## Offen
- Prompt-Tuning: Phase-A Extraktion pro Chunk produziert nur ~7 unique Topics (erwartet 40-60)
- Auto-Detect: ToC-lose Docs automatisch mit Fallback erkennen
- Issue #100: Slarti→Gitea→Lydia Dispatch fuer vollautomatischen Ingest
