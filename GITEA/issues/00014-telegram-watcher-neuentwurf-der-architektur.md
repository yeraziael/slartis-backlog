---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#14
state: closed
updated_at: 2026-07-15T01:12:36+02:00
is_epic: false
labels:
  - "Systemarchitektur"
  - "sub-task"
publication: sanitized
---

# Telegram Watcher – Neuentwurf der Architektur

## Goal
Komplette Neuentwicklung der Telegram-Watcher-Architektur.
Der alte Watcher (`telegram_lydia_watcher.sh`) wurde entfernt, weil er
monolithisch, schwer wartbar und ohne klare Trennung von Concerns war.

## Requirements
- Polling/Webhook für eingehende Nachrichten von @<operator>
- Command-Dispatch an Lydia oder Slarti (je nach Berechtigung)
- Policy-konform: Nur Chat-ID 163442721 darf Befehle erteilen
- Antwort/Status an User zurücksenden
- Logging für Observability
- Keine Monolithen – modulare Architektur (Handler pro Command)

## Non-Requirements
- Kein Multimedia-Processing
- Kein PDF-Formular-Filling (existiert separat)

## Constraints
- Läuft im Homelab (LAN)
- Token liegt in `<credential-path-redacted>` (Lydia) / `<credential-path-redacted>` (Slarti)
- Autostart via systemd user service

## Offene Fragen
- Soll der Watcher als Lydia-Prozess oder systemd-Service laufen?
- Soll Slarti eigene Kommandos per Telegram empfangen können?
- Rate-Limiting?

---
Erstellt als Teil der Block-3-Reorganisation (Watcher-Altlasten entfernt).
