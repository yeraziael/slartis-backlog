---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#27
state: closed
updated_at: 2026-07-03T11:56:19+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# messenger_michael.sh — OpenCodeAgent Fork

## Task
Eigenständiger Telegram-Bot-Fork für @Maier_wtf_HomelabBot als lydia-messenger@michael systemd-Instanz.

## Status
Auf Eis

## Key Points
- Läuft als User michael, Policy: nur @<operator>
- /exec an OpenCodeAgent (Binary)
- Eigene Ollama-Instanz mit GPU-Contention-Retry
- Vorarbeit erledigt: Token/creds, opencode Binary, task-queue existieren

## Open Questions
- opencode Binary direkt oder enqueue_task.py?
- LLM Router für Dispatch?
- systemd: User=michael oder User=lydia?
