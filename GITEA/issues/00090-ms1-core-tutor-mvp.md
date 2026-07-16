---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#90
state: closed
updated_at: 2026-07-03T07:55:15+02:00
is_epic: false
labels:
  - "Aufgaben"
  - "ready"
publication: sanitized
---

# MS1: Core Tutor MVP

> **Epic: #89 (Lydia-Tutor-Skill)** | Destilliert aus #72–#74

---

## Ziel

Plugin `tutor/` in Lydia einbauen: `/tutor <topic>` aktiviert den Tutor-Modus per Telegram, nutzt Paperless-ngx als Wissensbasis und speichert Lernfortschritt in Git.

## Arbeitspakete

- [ ] Plugin `tutor/` anlegen mit `init.sh` (registriert `/tutor`-Handler nach bestehendem Plugin-Muster)
- [ ] `/tutor <topic>` → Lydia erkennt Kommando, wechselt User in Tutor-Modus
- [ ] Model-Routing: Default `qwen3.5:4b`, für Mathe/Code/Logik automatisch `qwen2.5-coder:7b-instruct`
- [ ] Paperless-ngx RAG: Bestehende Paperless-Pipeline nutzen, Top-5 relevante Chunks in den Prompt
- [ ] Git-Session-Log: Nach jeder Tutor-Sitzung Fortschritt in `runtime/data/tutor/users/{chat_id}/` committen
- [ ] State-Management: Pro User merken ob im Tutor-Modus; `/exit` zum Verlassen, nach Timeout Auto-Exit
- [ ] Tutor-Prompt-Template (Deutsch): Lernstand + RAG-Kontext + Schritt-für-Schritt-Erklärung + Beispiele

## Akzeptanzkriterien

1. Nutzer schreibt `/tutor physik kinematik` → Lydia antwortet mit Tutor-Einleitung + Thema
2. Nachrichten im Tutor-Modus werden mit Lernkontext + RAG beantwortet (kein normaler Chat)
3. `/exit` verlässt den Modus und speichert Session-Log
4. Session-Log erscheint als Commit im home-repo

## Technische Basis

- Plugin-Engine: `runtime/plugins/plugin_engine.sh`
- Muster-Plugins: `echo`, `example`, `imagegen`
- Paperless-Integration: `paperless_agent/pipeline/`
- Ollama: `localhost:11434`
