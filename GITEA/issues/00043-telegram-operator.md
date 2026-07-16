---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#43
state: closed
updated_at: 2026-06-24T11:54:48+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Below is a distributed, autonomous Git rebase + conflict resolution worker design that fits your Slarti/Worker architecture. It is designed to eliminate Slarti from any semantic merge reasoning and reduce conflicts to a purely procedural resolution system executed locally.


⸻


1) SYSTEM GOAL
Create a worker that can:
detect merge conflicts during rebase/merge
classify conflict types deterministically
resolve conflicts locally when safe
escalate only irreducible semantic conflicts
produce a clean rebased branch ready for Slarti’s merge gate


⸻


2) POSITION IN YOUR ARCHITECTURE
Slarti (orchestrator)
   ↓
Worker (implementation)
   ↓
Rebase Worker (THIS SYSTEM)
   ↓
Conflict Resolver Worker (sub-agent)
   ↓
Clean branch
   ↓
Slarti merge gate (structural only)


⸻


3) CORE COMPONENTS
3.1 Rebase Controller Worker
Responsible for:
executing git rebase
detecting conflicts
spawning conflict resolution jobs
Input: base_branch, feature_branch
Output: rebased_branch OR conflict_tasks


⸻


3.2 Conflict Analyzer (deterministic classifier)
Classifies conflicts into 4 buckets:
TYPE 1 — AUTOMATIC MERGE SAFE
whitespace
formatting
import ordering
non-overlapping edits
TYPE 2 — STRUCTURAL NON-CONFLICT
same function touched, but different lines
resolvable via line-level merge heuristics
TYPE 3 — SEMANTIC CONFLICT (RESOLVABLE)
same function modified differently
requires AST-based merge strategy
TYPE 4 — SEMANTIC CONFLICT (NON-RESOLVABLE)
logic contradiction
incompatible API changes
requires escalation to Slarti TYPE C


⸻


3.3 Conflict Resolver Worker (AST-driven)
This is the key component.
Responsibilities:
parse both versions (base + feature)
build AST diff
merge at semantic node level (not text level)
regenerate patched file


⸻


4) INPUT CONTRACT
4.1 Rebase Task Envelope
{
  "task_id": "uuid",

  "base_branch": "main",
  "feature_branch": "worker/task_123",

  "strategy": "rebase | merge",

  "files_scope": [
    "src/module_a.py",
    "src/module_b.py"
  ],

  "conflict_resolution_mode": "auto | ast | strict_manual_escalation",

  "language": "python | ts | go",

  "test_command": "pytest -q"
}


⸻


5) REBASE CONTROLLER LOGIC
checkout(feature_branch)

try:
    git rebase base_branch
    return SUCCESS

except CONFLICT:
    conflicted_files = git diff --name-only --diff-filter=U

    for file in conflicted_files:
        classify_conflict(file)

    dispatch conflict tasks to Resolver Workers


⸻


6) CONFLICT RESOLUTION WORKER (CORE ENGINE)
6.1 System Prompt (Worker)
You are a Git Conflict Resolution Worker.

Your task is to resolve merge conflicts using semantic understanding of code structure.

You must:
- use AST-level reasoning where possible
- avoid line-based naive merging unless safe
- never introduce new features or logic
- preserve both branches' intent when compatible
- ensure code compiles and passes tests

You must NOT:
- escalate to high-level architectural changes
- rewrite modules beyond conflict region
- add new dependencies

Output must be a unified diff only.


⸻


6.2 Resolution Algorithm
FOR each conflicted file:

    parse base version → AST_B
    parse feature version → AST_F

    diff AST_B vs AST_F

    FOR each conflicting node:

        IF safe merge (no logic overlap):
            auto merge

        ELSE IF same function modified:
            attempt AST patch merge

        ELSE IF incompatible logic:
            mark as SEMANTIC_CONFLICT_NON_RESOLVABLE
            escalate

    generate patched file


⸻


7) ESCALATION RULE (critical safety)
IF conflict type == TYPE 4:
    send to Slarti:

    {
      "task_id": "...",
      "type": "ARCHITECTURAL_CONFLICT",
      "conflict_summary": "...",
      "files": [...],
      "suggested_resolution_options": 2-3 minimal alternatives
    }
Slarti does NOT debug — only chooses strategy.


⸻


8) DISTRIBUTED EXECUTION MODEL
Parallel resolution:
Conflicted Files:
    file_1 → resolver_worker_1
    file_2 → resolver_worker_2
    file_3 → resolver_worker_3
No shared state except git index.


⸻


9) FINAL INTEGRATION PHASE
After all conflicts resolved:
