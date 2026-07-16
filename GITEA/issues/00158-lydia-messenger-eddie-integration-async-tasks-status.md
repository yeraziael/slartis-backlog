---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#158
state: closed
updated_at: 2026-07-13T18:29:00+02:00
is_epic: false
labels:
  - "ready"
  - "sub-task"
publication: sanitized
---

# Lydia Messenger: Eddie-Integration (async-Tasks + /status)

# Lydia Messenger: Eddie-Integration

**Parent:** slarti/backlog#157 (Eddie EPIC)
**Status:** Specification
**Priorität:** Hoch

## Hintergrund

Lydia's Messenger-Prozessor verarbeitet aktuell alle Telegram-Kommandos direkt:
- `/prompt`, `/generate` → gehen direkt an Ollama/ImageGen auf rechenknecht
- `/status`, `/register` etc. → lokal auf Pi5

Mit Eddie als zentralem Scheduler/Dispatcher sollen async-KI-Tasks via Eddie geroutet werden.
Eddie entscheidet WANN und WER ausführt, Lydia enqueued die Tasks bei Eddie via REST API.

## Scope

### 1. Command-Klassifikation

**Sync (bleiben direkt im Processor):**
- `/status`, `/help`, `/register`, `/users`, `/pending`, `/accept`, `/deny`
- `/alias`, `/tools`, `/enable`, `/disable`, `/logs`
- Kein Eddie-Umweg, da blockierend und sofort beantwortbar

**Async (werden via Eddie geroutet):**
- `/prompt <frage>` → Eddie dispatched an Ollama-Executor
- `/generate avatar/wallpaper/from_picture` → Eddie dispatched an ImageGen-Executor
- `/models` → Eddie fragt Ollama-Status ab (oder direkt, da read-only)

### 2. Eddie-API-aufrufe aus dem Processor

Der Processor ruft bei Erkennung eines async-Kommandos:

```
POST /api/v1/jobs
{
  "type": "one-shot",
  "executor": "lydia",
  "priority": 50,
  "params": {
    "command": "prompt",
    "args": ["<frage>"]
  },
  "timeout": 300,
  "notify": {
    "channel": "telegram",
    "chat_id": "<original-chat-id>"
  }
}
```

Eddie antwortet mit `{"id": "<job-uuid>", "status": "queued"}`.

### 3. Ergebnis-Rückweg

Nach Ausführung schreibt der Executor (Lydia/Vekling) das Ergebnis via:
```
POST /api/v1/jobs/<id>/result
{ "output": "...", "status": "completed" }
```

Eddie benachrichtigt den ursprünglichen Kanal (Telegram) mit dem Ergebnis.
Alternativ pollt der Processor nach Abschluss — Mechanismus muss im ADR-konformen API-Design festgelegt werden.

**Offen:** Callback (Eddie pushed) vs Polling (Lydia fragt nach) vs hybrid.

### 4. /status-Integration

Der `/status`-Command muss Eddie's Health einbeziehen:

```
GET /api/v1/status
→ { "healthy": true, "queue_depth": 3, "active_jobs": 1, "uptime": "2h" }
```

Darstellung im Telegram-Status:
```
📊 Status
Eddie: ✅ aktiv (1 Job läuft, 3 in Queue)
Ollama: ✅
GPU: ⏸ idle
```

### 5. Fallback

Wenn Eddie nicht erreichbar ist:
- Async-Kommandos werden mit "Eddie nicht verfügbar, bitte später" abgelehnt
- Sync-Kommandos funktionieren weiter (keine Eddie-Abhängigkeit)
- `/status` zeigt Eddie als ❌ nicht erreichbar

### 6. Migration

- Schritt 1: Eddie-API-Calls im Processor vorbereiten (mit Feature-Flag)
- Schritt 2: Async-Tasks parallel an Eddie + direkt senden (Dual-Run)
- Schritt 3: Direkt-Route entfernen, nur noch via Eddie

## Abgrenzung

- Messenger-Polling (Telegram, Signal) bleibt im lydia-messenger-Container
- Nur die *Verarbeitung* async-Kommandos wechselt zu Eddie
- Eddie's API muss existieren, bevor dieser Task umgesetzt werden kann
