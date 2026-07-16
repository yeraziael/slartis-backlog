---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#54
state: closed
updated_at: 2026-06-30T22:11:41+02:00
is_epic: false
labels:
  - "project:homelab-agenten-ausbau"
publication: sanitized
---

# Worker-Dispatch & GPU-Scheduling

## Ursprung
Issue #51 (Telegram: <operator>)

## Ziel
Queue-basiertes Dispatch-System für Worker mit GPU-Contention-Management:
- Prioritäts-Queue (GPU-lastige vs. CPU-only Tasks)
- Lock-basierte GPU-Zuteilung (verhindert gleichzeitige Ollama-Instanzen)
- Deferral niedriger Prio bei GPU-Überlast
- Parallele CPU-Tasks während GPU idle

## Teilaufgaben
- [x] GPU-Lock-Management erweitern → `runtime/hardening/gpu_lock.sh`
- [x] Priority-Queue für Worker-Tasks → `runtime/dispatch/worker_queue.sh`
- [x] Scheduling-Logik → `spawn_generation()` chain + `worker_scheduler_poll()` in `task_loop.sh`
- [x] Integration mit existierender FIFO-Queue → `gpu_is_busy()` checkt worker_queue_gpu_busy

## Implementierung (2026-06-30)
- gpu_lock.sh: File-basierte Sperre `/tmp/lydia-gpu.lock` mit acquire/release/holder
- worker_queue.sh: JSON-Queue mit running/gpu_busy flags, GPU/CPU Aufgaben-Detektion
- handler_ephemeral_worker: async enqueue (kein direkter Ollama-Call mehr)
- spawn_worker(): dequeued + GPU lock check + worker_loop execution
- worker_scheduler_poll(): Daemon-poling im task_loop alle 15s
- test_worker_dispatch.sh: 30/30 PASS (keine Regressionen)

## Tests
- test_worker_dispatch.sh: 30/30 PASS
- test_messenger.sh: 21/21 PASS
- test_worker.sh: 15/15 PASS

## Status (2026-06-30)
### Erledigt im Rahmen von #52/#53/#55
- Worker-Protokoll & Contract-System implementiert (#52 — closed)
- Design Rules: DESIGN_RULES.md, PR_CHECKLIST.md, rule_validator.sh (#53 — closed)
- Ollama-Modelle auf RAID0 verschoben (<local-path-redacted>) — Root-Disk von 87% auf 78% befreit
- Hardware-Analyse: GTX 980 Ti (6 GB VRAM), ~36 tok/s für qwen2.5-coder:7b-instruct via Vulkan

## Blocked by
- #68 — Benchmark-Modelle müssen erst installiert sein
