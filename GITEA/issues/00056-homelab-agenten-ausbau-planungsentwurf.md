---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#56
state: closed
updated_at: 2026-06-30T22:14:12+02:00
is_epic: false
labels:
  - "project:homelab-agenten-ausbau"
publication: sanitized
---

# Homelab-Agenten-Ausbau — Planungsentwurf

## Überblick
Projekt zum systematischen Ausbau der Homelab-Agenten-Infrastruktur basierend auf der Slarti/Worker-Zwei-Ebenen-Architektur.

## Meilensteine

### M1: Foundation (aktuell)
- ✅ Worker-Protokoll & Contract-System (#52 — closed)
- ✅ CRITICAL Design Rules (#53 — closed)
- ✅ Worker-Dispatch & GPU-Scheduling (#54 — implemented)
- ✅ Modellwahl & Hardware-Optimierung (#55 — benchmarked, qwen2.5-coder:7b selected)
- ✅ Benchmark-Modelle pullen (#68 — closed by @michael)

### M2: Resilience (geplant)
- Failure-Recovery
- Multi-Worker-Parallel-Scheduler

### M3: Advanced (geplant)
- Autonomer Git-Rebase + Conflict-Resolution

### M4: Zukunft (geplant)
- Semantic Merge Memory System (SMMS)

## M1 Status: 5/5 ✅ COMPLETE
- Commits: 9dcf051..3ad46bf (9 commits pushed)
- 2 neue Komponenten: gpu_lock.sh, worker_queue.sh
- 1 Benchmark: benchmark_models.sh
- 3 Test-Suites: test_messenger 21/21, test_worker 15/15, test_worker_dispatch 30/30

## Herkunft
Abgeleitet aus den Telegram: <operator>-Issues #33–#51.

## Organisation
- Label: `project:homelab-agenten-ausbau`
- Milestone: M1: Foundation (#18)
