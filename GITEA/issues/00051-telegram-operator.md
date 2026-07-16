---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#51
state: closed
updated_at: 2026-06-24T11:54:50+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Prefer dispatch based on queue depth and lock availability:
if worker idle and no lock conflict:
    assign next compatible task

if GPU queue grows:
    defer low-priority jobs

if CPU utilization is acceptable:
    allow small documentation or analysis tasks concurrently
With a single 980 Ti, running one GPU-intensive inference at a time is often the most predictable choice. If you need concurrency, consider overlapping LLM inference with non-LLM work (tests, Git operations, formatting) rather than running multiple heavy generations simultaneously.
Merge safety gate
Every worker result should pass:
✓ modified files ⊆ allowed scope
✓ formatter passes
✓ lint passes
✓ targeted tests pass
✓ no forbidden dependency additions
✓ no secrets introduced
✓ patch applies cleanly
Only then should Slarti permit integration.
Recommended orchestration rules
Slarti plans; workers implement.
Workers receive only minimal context.
One worker owns a file at a time.
Retry locally before escalation.
Return patches and structured status, not lengthy explanations.
Treat repeated conflict patterns as candidates for reusable merge rules.
Keep architecture decisions centralized in Slarti; keep implementation decentralized in workers.
Practical recommendation for your hardware
With your current machine, I would deploy:
1 persistent Ollama server hosting Qwen2.5-Coder 7B Instruct (or a similarly capable coding model that performs well in your environment).
2–4 lightweight worker processes that submit jobs to that shared server but are throttled so that only one GPU-heavy generation runs at a time.
Parallelize everything around the model—Git operations, testing, linting, queue management, and branch preparation—rather than trying to saturate the GPU with simultaneous large generations.
This design maximizes throughput on limited VRAM while preserving deterministic behavior and keeping Slarti’s own context footprint small.
