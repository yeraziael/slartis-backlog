---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#40
state: closed
updated_at: 2026-06-24T11:54:47+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

- If you are uncertain, do NOT expand scope; reduce solution complexity.
- If multiple solutions exist, choose the one with:
  (1) least code changes
  (2) least dependencies
  (3) highest test determinism

- Never optimize prematurely.
- Never generalize beyond test requirements.


⸻


6) Warum dieses Template Token-effizient ist (für Slarti)
Slarti sendet nur Envelope (~klein)
Worker übernimmt:
Kontextrekonstruktion lokal
Iteration lokal
Test loops lokal
Slarti bekommt nur:
diff
status
minimal summary
➡️ Slarti wird damit effektiv zu einem thin orchestrator, nicht mehr einem reasoning-heavy system.


⸻
