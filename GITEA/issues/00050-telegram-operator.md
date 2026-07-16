---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#50
state: closed
updated_at: 2026-06-24T11:54:49+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Given your hardware (32 GB RAM + GTX 980 Ti with 6 GB VRAM), I would not build a many-model GPU-resident system. The 980 Ti is likely to become the bottleneck. Instead, use one primary coding model, keep it warm, and scale concurrency conservatively.
High-level architecture
                    +----------------------+
                    |       Slarti         |
                    | Planner / Router     |
                    +----------+-----------+
                               |
                 +-------------+-------------+
                 |                           |
        TYPE C (architecture)       TYPE A/B (coding)
                 |                           |
                 |                    Job Queue (FIFO +
                 |                  priority + file locks)
                 |                           |
                 |         +-----------------+-----------------+
                 |         |                                   |
                 |   Worker Process 1                    Worker Process 2
                 |   (Ollama client)                   (Ollama client)
                 |         |                                   |
                 +---------+-----------+-----------------------+
                                       |
                               Single Ollama Server
                               (shared model instance)
                                       |
                                 GTX 980 Ti / CPU
The important distinction is that multiple workers do not require multiple model instances. They can share one Ollama server while Slarti controls scheduling.
Model routing policy
Task type
Model
Max concurrency
Notes
Boilerplate, formatting, comments
Lightweight model (optional)
2
Can fall back to primary model if unavailable
Small bug fixes
Qwen2.5-Coder 7B
1–2
Default route
Refactoring
Qwen2.5-Coder 7B
1
Avoid overlapping edits
Test generation
Qwen2.5-Coder 7B
2
Good candidate for batching
Merge conflict resolution
Qwen2.5-Coder 7B (or stronger model if available)
1
Run after implementation tasks
Architecture decisions
Slarti
N/A
Do not delegate blindly
On your hardware, one well-configured model is preferable to switching between several large models, because model loading latency and memory pressure can outweigh any specialization benefits.
Worker lifecycle
Each worker is ephemeral:
CREATE
  ↓
Acquire job
  ↓
Create git worktree or branch
  ↓
Load minimal context
  ↓
Generate patch
  ↓
Run formatter
  ↓
Run targeted tests
  ↓
Retry locally (bounded)
  ↓
Emit result
  ↓
Destroy worker state
The worker should never persist conversational history between jobs.
Queue priorities
priority:
  P0:
    - build break
    - failing tests on main
  P1:
    - bug fix
    - merge conflict
  P2:
    - feature implementation
  P3:
    - cleanup
    - style
    - documentation
Within the same priority, schedule shortest expected jobs first if you have reliable estimates.
File locking
Maintain a lock table keyed by repository paths:
locks:
  src/api.py:
    owner: task-1842

  src/auth/:
    owner: task-1848
Rules:
Workers touching overlapping files should not execute simultaneously.
Prefer locking at the narrowest practical scope (file or directory).
Release locks immediately after merge or cancellation.
Branch strategy
main

└── slarti/integration

    ├── worker/task-001
    ├── worker/task-002
    └── worker/task-003
Recommended merge flow:
Worker commits to its own branch.
CI/test gate executes.
Slarti validates policy compliance.
Fast-forward or squash into integration branch.
Integration branch merges into main.
Retry policy
attempt 1
    ↓
targeted repair
    ↓
attempt 2
    ↓
targeted repair
    ↓
attempt 3
    ↓
fail and escalate
Avoid unlimited retry loops.
Context budgeting
Keep prompts compact:
system_prompt:
  fixed: true

task_contract:
  target: 300-800 tokens

code_context:
  only touched files

response:
  unified diff
  short summary
Avoid sending unrelated repository history or broad architectural descriptions to workers.
Load balancing rules
