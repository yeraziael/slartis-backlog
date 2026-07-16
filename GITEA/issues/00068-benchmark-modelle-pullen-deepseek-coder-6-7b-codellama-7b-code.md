---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#68
state: closed
updated_at: 2026-06-30T18:19:17+02:00
is_epic: false
labels:
  []
publication: sanitized
---

# Benchmark-Modelle pullen (deepseek-coder:6.7b + codellama:7b-code)

## Task
Benchmark-Modelle auf dem Worker-Host pullen für Issue #55 (Modellwahl & Hardware-Optimierung).

## Hintergrund
Die Modelle werden für das Benchmarking benötigt, um qwen2.5-coder:7b-instruct gegen Alternativen zu vergleichen.
Beide Pulls sind in der letzten Session nach 5 Minuten ge-timeoutet.

## Ausführung
Läuft als slarti-User (sudo?). Ollama läuft als systemd-Service (ollama.service).

```bash
ollama pull deepseek-coder:6.7b
ollama pull codellama:7b-code
```

## Modell-Details
| Modell | Größe | VRAM (Q4_K_M) | Use-Case |
|---|---|---|---|
| deepseek-coder:6.7b | ~4.0 GB | ~5.0 GB | Code-Synthese |
| codellama:7b-code | ~3.8 GB | ~4.8 GB | Code-Erklärung + Refactoring |

## Blocker für
- #55 — Modellwahl & Hardware-Optimierung für Worker

## Verwandte Issues
- #55: Modellwahl & Hardware-Optimierung
- #54: Worker-Dispatch & GPU-Scheduling
- #53: Design Rules (closed)
- #52: Ephemeral Worker (closed)
