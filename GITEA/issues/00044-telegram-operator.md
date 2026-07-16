---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#44
state: closed
updated_at: 2026-06-24T11:54:48+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

if all files resolved:
    git add .
    git commit -m "rebase resolved by distributed workers"
    mark branch as rebased
else:
    escalate remaining TYPE 4 conflicts


⸻


10) FAILURE MODES + RECOVERY
10.1 AST parsing failure
→ fallback to structured diff merge (line-aware)
10.2 repeated conflict loop
→ reduce scope to smallest function unit
10.3 ambiguous semantic merge
→ escalate to Slarti TYPE C


⸻


11) KEY OPTIMIZATION IDEA (important)
This system only works efficiently if:
You NEVER do:
full-file rewriting in Slarti
human-like reasoning about merges
manual diff interpretation
You ALWAYS do:
AST-first merging
file-scoped workers
deterministic conflict classification


⸻


12) RESULTING SYSTEM BEHAVIOR
Before:
Slarti resolves merges manually
repeated context loading
high token burn + cognitive load
After:
merges become deterministic distributed jobs
Slarti only routes and approves
conflict resolution becomes parallelizable compute


⸻


13) FINAL ARCHITECTURAL SUMMARY
Slarti
  → Task decomposition
  → Routing

Worker
  → implementation

Rebase Controller
  → git orchestration

Conflict Analyzer
  → classification

Conflict Resolver Workers
  → AST-based merging

Slarti
  → final gate only


⸻
