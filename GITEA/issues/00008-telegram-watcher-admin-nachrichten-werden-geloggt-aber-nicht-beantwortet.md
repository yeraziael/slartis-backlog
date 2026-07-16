---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#8
state: closed
updated_at: 2026-07-14T18:21:22+02:00
is_epic: false
labels:
  []
publication: sanitized
---

# Telegram Watcher: Admin-Nachrichten werden geloggt aber nicht beantwortet

> **Migriert von OpenCodeAgent/opencode-context#17** (2026-06-21)

---

## Problem

Der Telegram-Watcher (/tmp/telegram_watcher.sh) erkennt Admin-Nachrichten (@<operator>, Chat-ID 163442721) korrekt, antwortet aber nicht. Er loggt sie nur als ADMIN und geht davon aus, dass die opencode-Instanz die Commands verarbeitet.

Das fuehrt dazu, dass einfache Fragen unbeantwortet bleiben, wenn keine opencode-Instanz aktiv auf die Nachricht reagiert.

## Ursache

Watcher-Code Zeile 69-71:
```
if chat_id == admin_chat and not is_test:
    print(fADMIN: {username}: {text[:80]})
```

Der Watcher enthaelt keine Reply-Logik fuer Admin-Nachrichten.

## Gewuenschtes Verhalten (Diskussion offen)

1. Nur loggen (Status Quo) - erfordert dass immer eine opencode-Instanz parallel lauscht
2. Ollama-Rueckfall - Admin bekommt ebenfalls eine Ollama-Antwort, aber mit erweiterten Rechten
3. Command-Dispatch - Watcher erkennt Befehle (status, health, pipeline) und fuehrt sie direkt aus

## Kontext

- Watcher: /tmp/telegram_watcher.sh
- Policy: Issue #8
- Getestet in Session 2026-06-21 (Test-Modus lief, Admin-Nachricht blieb unbeantwortet)

## Status

Neu - muss diskutiert werden
