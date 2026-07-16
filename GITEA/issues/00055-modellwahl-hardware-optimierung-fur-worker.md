---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#55
state: closed
updated_at: 2026-06-30T22:11:41+02:00
is_epic: false
labels:
  - "project:homelab-agenten-ausbau"
publication: sanitized
---

# Modellwahl & Hardware-Optimierung für Worker

## Ursprung
Issues #49–#50 (Telegram: <operator>)

## Ziel
Empfehlung und Einrichtung des optimalen lokalen Modells für Worker auf vorhandener Hardware (32 GB RAM, GTX 980 Ti 6 GB VRAM):
- Modell-Auswahl: Code-Synthese + Instruction-Following + 6 GB VRAM
- Quantisierungsstrategie (Q4_K_M, Q5_K_M, etc.)
- Ollama-Konfiguration für Worker (context window, batch size)
- Fallback-Strategie bei GPU-Konflikten

## Teilaufgaben
- [x] Modelle installieren (deepseek-coder:6.7b + codellama:7b-code) — #68 closed
- [x] Modelle benchmarken (qwen2.5-coder, deepseek-coder, codellama) — siehe Kommentar
- [x] Optimale Quantisierungsstufe ermitteln — Q4_K_M ausreichend (alle Modelle passen in 6 GB)
- [x] Ollama-Konfiguration für Worker — num_ctx=2048, num_predict=512 gesetzt
- [ ] GPU-Contention-Lösung — erledigt via #54 (GPU Lock)

## Ergebnis
- **Primary: qwen2.5-coder:7b-instruct** — 2/3 PASS, 14.2 tok/s, marker-konform
- **Fallback: deepseek-coder:6.7b** — 2/3 PASS, 17.6 tok/s, zuverlässiger Code
- **NICHT: codellama:7b-code** — 1/3 PASS, ignoriert Marker, maxed 512 tok-Limit
- **Context-Window: num_ctx=2048** in worker_loop.sh (spart VRAM)

## Referenzen
- Ollama-Modelle lokal: qwen2.5-coder:7b, deepseek-coder:6.7b, codellama:7b-code, qwen2.5:3b, qwen3.5:4b, llama3.1
- GTX 980 Ti: 6 GB VRAM, Vulkan-Backend, ~36 tok/s
- Benchmark-Script: `runtime/tests/benchmark_models.sh`
