---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#38
state: closed
updated_at: 2026-06-24T11:54:47+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Hier ist ein kompaktes, tokenoptimiertes Slarti↔Worker-Protokoll, das genau auf Kontextreduktion + lokale Rekursion + minimale Rückkanäle ausgelegt ist.
Ziel: Slarti sendet kein Codeverständnis, sondern nur operative Constraints + Schnittstellen + Akzeptanzkriterien.


⸻


1) Grundprinzip: „Contract statt Kontext“
Slarti darf niemals komplette Repos schicken.
Stattdessen:
Intent (was soll entstehen)
Boundary (wo im System)
Interface Contract (Signaturen / IO)
Acceptance Tests (Verifikation)
Hard Constraints (Style, libs, limits)
Worker rekonstruiert alles andere lokal.


⸻


2) Slarti → Worker: Task Envelope (Minimalformat)
{
  "task_id": "uuid",
  "intent": "short natural language goal",
  "scope": {
    "module": "path/to/module or component",
    "files_allowed": ["relative/file1", "file2"]
  },
  "interface_contract": {
    "inputs": "typed description",
    "outputs": "typed description",
    "side_effects": "none | limited | specified"
  },
  "constraints": {
    "language": "python|ts|go|...",
    "style": "idiomatic|strict|performance-focused",
    "deps": ["allowed libs only"],
    "no_network": true
  },
  "acceptance_criteria": [
    "bullet testable conditions",
    "must compile",
    "must pass pytest suite",
    "edge case handling"
  ],
  "test_spec": {
    "type": "pytest|jest|custom",
    "cases": [
      "input -> expected output",
      "edge case definitions"
    ]
  },
  "patch_mode": "unified_diff | full_file | function_only"
}


⸻


3) Worker Execution Loop (lokal, autonom)
Worker läuft als closed loop ohne Slarti-Rückfragen:
Schritt 1: Local Context Reconstruction
liest nur erlaubte Dateien
baut minimales AST/semantic map
Schritt 2: Plan (intern, nicht zurückmelden)
keine Tokenkosten für Slarti
Schritt 3: Implement
Codeänderung lokal
Schritt 4: Test Loop
run tests → fail → fix → rerun
repeat until pass or max_iterations reached
Schritt 5: Output Compression
Nur zurück an Slarti:
{
  "task_id": "uuid",
  "status": "success | partial | failed",
  "patch": "unified diff",
  "summary": "max 5-10 lines",
  "tests_run": 42,
  "failures": 0,
  "notes": "only deviations from spec"
}


⸻


4) Slarti Merge-Logik (ultra-leicht)
Slarti macht keine Interpretation, nur Validierung:
if acceptance_criteria_met:
    apply_patch()
else:
    reject_and_requeue()
Optional:
kein Debugging im Slarti
keine Code-Rekonstruktion


⸻


5) Token-Optimierung (entscheidender Teil)
Vorher (klassisch)
Slarti:
liest Code: ██████████
denkt: ████████
iteriert: ████████
Worker:
optional redundant
➡️ hohe Slarti-Kosten


⸻


Nachher (Contract System)
Slarti:
1x Task Envelope (klein)
1x Review (klein)
Worker:
volle Last lokal
➡️ Slarti-Kosten ≈ 80–95% reduziert


⸻


6) Kritischer Designpunkt (wichtig)
Der häufigste Fehler:
zu viel Kontext im intent oder scope
Wenn Slarti anfängt:
Code zu erklären
Architektur zu beschreiben
Dateien zusammenzufassen
→ verlierst du alle Tokenvorteile


⸻


7) Erweiterung: „Context Hashing“ (optional, sehr effizient)
Statt Code zu schicken:
"code_fingerprint": {
  "repo_hash": "abc123",
  "module_hash": "def456"
}
Worker nutzt lokal:
git checkout
hash verification
ensures alignment
Slarti spart nochmal massiv Tokens.


⸻


8) Erweiterung: Task-Klassifizierung (empfohlen)
Slarti sollte vorher klassifizieren:
TYPE A: trivial transformation → Worker
TYPE B: multi-file refactor → Worker
TYPE C: architectural decision → Slarti only
TYPE D: ambiguous → Slarti


⸻


9) Kurzfazit
Dieses System funktioniert nur, wenn du streng durchziehst:
Slarti = Planner + Validator (kein Code-Rekonstruktor)
Worker = vollständiger Code-Execution-Agent
Kommunikation = Contracts + Diff only


⸻
