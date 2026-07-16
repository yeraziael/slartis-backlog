---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#46
state: closed
updated_at: 2026-06-24T11:54:49+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

rule must have N successful applications before “trusted”


⸻


11.3 Drift detection
If:
rule success_rate < baseline_threshold
→ invalidate rule and retrain from raw MERs


⸻


12) SYSTEM EFFECT (IMPORTANT)
After enough merges:
You get:
1. “Zero-reasoning merges” for common patterns
imports
params
simple function edits
refactors with no semantic conflict
2. Worker load collapses
Only novel conflicts reach LLMs.
3. Slarti becomes nearly stateless
It routes and validates, nothing else.


⸻


13) FULL ARCHITECTURE AFTER SMMS
User
  ↓
Slarti Router
  ↓
Rebase Controller
  ↓
Conflict Analyzer
  ↓
SMMS Lookup
      ↓ yes
   Rule Engine → deterministic merge
      ↓ no
Conflict Resolver Worker (LLM)
  ↓
MER generation
  ↓
SMMS storage + compression
  ↓
Git integration


⸻


14) KEY INSIGHT (why this matters)
You are effectively building:
a learning merge compiler for software evolution
Not an agent system anymore — a history-compressing transformation layer over git evolution.


⸻
