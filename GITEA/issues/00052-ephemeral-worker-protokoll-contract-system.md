---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#52
state: closed
updated_at: 2026-07-14T00:32:52+02:00
is_epic: false
labels:
  - "project:homelab-agenten-ausbau"
publication: sanitized
---

# Ephemeral Worker — Protokoll & Contract-System

## Ursprung
Issues #33–#39 (Telegram: <operator>)

## Ziel
Implementierung des Slarti↔Worker-Protokolls:
- Contract-basierte Task-Übergabe (Constraints + Schnittstellen + Akzeptanzkriterien)
- Lokale Worker-Ausführung mit Ollama
- Iterativer Test-Loop (Worker führt aus, testet, fixx)
- Kompaktes Diff-Format als Rückgabe

## Teilaufgaben
- [ ] Ollama Worker Prompt-Template definieren
- [ ] Contract-JSON-Schema festlegen
- [ ] Slarti-Task-Slicing (nur Contracts, kein Code-Kontext)
- [ ] Worker-Loop (execute → verify → retry → diff)
- [ ] Integration ins bestehende Lydia-Task-System

## Referenzen
- `runtime/messenger/ollama_helper.sh` — vorhandener Ollama-Lifecycle
- `runtime/messenger/llm_router.sh` — vorhandener Router
- `runtime/tasks/task_loop.sh` — vorhandene Task-Engine
