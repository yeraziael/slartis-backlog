---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#10
state: closed
updated_at: 2026-07-14T23:18:09+02:00
is_epic: false
labels:
  []
publication: sanitized
---

# Signal-Bot Setup & Integration (konsolidiert)

> **Migriert von OpenCodeAgent/opencode-context#15** (2026-06-21)

---

## Ziel

Signal als zweiten Messenger-Kanal neben Telegram einbinden.

## Ausgangslage

- **SIM-Karte (o2 Prepaid) ist bestellt** – sobald sie da ist, kann der Prozess starten
- SIM kommt in **Nokia 105 4G** (nur SMS + Netzverfuegbarkeit)
- Agent fuehrt Setup vollautomatisch durch
- **Einzige User-Interaktion (2 Schritte):**
  1. SMS-PIN von der SIM-Karte an Agent weitergeben (Registration)
  2. 6-stelligen Code per Signal zurueckschicken (Trust-On-First-Use)

## Setup-Plan

1. **signal-cli installieren** (JSON-RPC-Daemon, systemd-User-Service)
2. **Registrierung**: `signal-cli -u +<NUMMER> register` -> Signal schickt SMS
3. **PIN abfragen**: Michael per Telegram bitten, die SMS-PIN mitzuteilen
4. **Verifizieren**: `signal-cli -u +<NUMMER> verify <PIN>`
5. **Trust-On-First-Use**: 6-stelligen Code generieren, Michael schickt ihn via Signal zurueck
6. **Watcher starten**: Analog Telegram-Watcher (`/tmp/signal_watcher.sh`)
7. **Policy**: Nur @<operator> darf Befehle geben (wie Telegram)

## Offene Punkte

- signal-cli ohne DBus auf rechenknecht nutzbar? (JSON-RPC-Daemon geht standalone)
- Telefonnummer + Vorwahl sobald SIM da (erwarten +49...)

## Referenzen

- Geschlossene Duplikate: #5 (altes Epic), #10 (alter Setup-Plan)
- Telegram-Watcher: `/tmp/telegram_watcher.sh`
- Repo: `OpenCodeAgent/opencode-context`
- signal-cli: https://github.com/AsamK/signal-cli

## Status

Wartet auf SIM-Karte
