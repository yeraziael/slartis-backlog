---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#42
state: closed
updated_at: 2026-06-24T11:54:48+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Gut, dann erweitern wir das System jetzt in zwei Richtungen, die in der Praxis entscheidend sind:
Failure-Recovery + Resilience Layer
Multi-Worker Parallel Scheduler (Batch + Queueing + Conflict Control)
Ich halte das bewusst wieder implementierungsnah.


⸻


1) FAILURE-RECOVERY SYSTEM (Slarti + Worker Robustheit)
Ziel
Verhindern, dass:
flaky tests
unvollständige patches
partial failures
merge conflicts
das System in manuelle Debug-Schleifen zwingt.


⸻


1.1 Worker Failure Contract (standardisiert)
Wenn Worker scheitert, MUSS er strukturiert zurückmelden:
{
  "task_id": "uuid",
  "status": "failed",
  "failure_stage": "context | implementation | test | merge",
  "error_type": "compile_error | test_failure | unknown | dependency_block",
  "failed_tests": [
    "test_name_1",
    "test_name_2"
  ],
  "root_cause_hypothesis": "short technical guess",
  "patch_attempts": 3
}
Wichtig:
keine langen Diagnosen
nur strukturierte Failure-Klasse


⸻


1.2 Slarti Recovery Policy (kein Debugging, nur Re-tasking)
IF worker status == failed:

    IF failure_stage == test:
        → re-issue TASK with stricter acceptance criteria

    IF failure_stage == implementation:
        → reduce scope (split into smaller TYPE A tasks)

    IF failure_stage == context:
        → improve contract precision (NOT add more code context)

    IF failure_stage == dependency_block:
        → enforce dependency constraints or switch strategy

NEVER:
    - debug code manually
    - inspect full diffs deeply
    - attempt patch correction directly


⸻


1.3 Retry Control (Anti-loop explosion)
max_retries_per_task = 2

IF retries exceeded:
    → escalate to TYPE C (architecture decision)


⸻


2) MULTI-WORKER PARALLEL SCHEDULER
Jetzt der Skalierungsblock.


⸻


2.1 Task Queue Model
Slarti führt eine Queue:
{
  "queue": [
    {
      "task_id": "1",
      "priority": 1,
      "type": "A",
      "status": "pending"
    }
  ]
}


⸻


2.2 Worker Pool Model
Worker_1 (Ollama instance)
Worker_2
Worker_3
...
Worker_N
Jeder Worker:
isoliert
stateless
eigener git branch


⸻


2.3 Scheduling Strategy
RULE: Chunk by dependency graph, not files
IF tasks independent:
    → parallel dispatch

IF tasks share files:
    → sequential lock per file-group


⸻


2.4 File Locking System (wichtig für Merge-Sicherheit)
{
  "file": "src/api.py",
  "locked_by": "task_id",
  "state": "locked | free"
}


⸻


2.5 Conflict Prevention Rule
No two workers may modify the same file unless:

- changes are additive only
OR
- merge strategy = rebase required


⸻


2.6 Parallel Execution Flow
1. Slarti decomposes into TASKS
2. Dependency graph computed
3. Independent tasks → parallel workers
4. Dependent tasks → sequential queue
5. Each worker:
      → executes loop
      → writes branch
6. Slarti merge gate per branch
7. Final merge into main


⸻


2.7 Deadlock Handling
IF file lock > timeout:
    → force unlock
    → reassign task with updated context hash


⸻


3) COMBINED SYSTEM BEHAVIOR
Jetzt hast du ein vollständiges System:
Slarti:
planner
router
queue manager
merge gate
failure recovery controller
Workers:
full local reasoning
test-driven execution
patch generation
isolated git branches


⸻


4) PERFORMANCE + TOKEN EFFECT
Vorher (monolithisches reasoning)
Slarti konstant im Kontext
wiederholte Codeanalyse
iterative debugging
→ stark wachsender Tokenverbrauch


⸻


Nachher (distributed execution model)
Slarti:
O(1) pro Task
Worker:
O(n) lokal, aber irrelevant für Slarti-Kosten
→ Skalierung wird horizontal statt kontextgebunden


⸻


5) WICHTIGSTER DESIGNPUNKT (oft übersehen)
Dieses System funktioniert nur, wenn strikt gilt:
Slarti darf niemals in Worker-Debugging abrutschen.
Sobald Slarti beginnt:
Logs zu interpretieren
Code zu korrigieren
Diff-Details zu analysieren
→ verlierst du den gesamten Architekturvorteil.


⸻
