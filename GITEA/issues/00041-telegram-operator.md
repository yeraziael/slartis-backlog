---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#41
state: closed
updated_at: 2026-06-24T11:54:48+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

4) CRITICAL DESIGN RULES (System-wide invariants)
Diese Regeln machen das System überhaupt erst token-effizient:


⸻


RULE 1 — Slarti never reads code deeply
Slarti sieht:
diffs
file lists
test results
Nicht:
vollständige Dateien
vollständige Module


⸻


RULE 2 — Workers are the only code reasoners
Alle echten Implementierungen passieren lokal.


⸻


RULE 3 — No iterative debugging in Slarti
Wenn Fehler:
→ neue Task generieren, nicht debuggen


⸻


RULE 4 — Context shrink is mandatory
Wenn Slarti Kontext expandiert:
→ System verliert Tokenvorteil vollständig


⸻


5) SYSTEM ARCHITECTURE RESULT (kompakt)
User Request
    ↓
Slarti Router (classification + compression)
    ↓
Worker (local reasoning + execution + tests)
    ↓
Git branch (isolated)
    ↓
Slarti Merge Gate (structural validation only)
    ↓
Main repo


⸻


6) Warum dieses Design wirklich Token spart
Vorher
Slarti:
liest Code
versteht Code
debuggt Code
re-iteriert Code
→ O(n²) Kontextverbrauch bei komplexen Repos


⸻


Nachher
Slarti:
1x compression
1x validation
Worker:
übernimmt gesamte O(n) Komplexität lokal
→ Slarti wird konstant im Tokenverbrauch


⸻
