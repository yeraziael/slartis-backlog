---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#67
state: closed
updated_at: 2026-06-30T13:07:28+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Signal: Contact-Card / Multi-Channel-Empfang debuggen

## Kontext
Lydia Messenger wurde auf Dual-Channel (Telegram + Signal) umgebaut:
- `messenger_lydia.sh` polled jetzt beide Kanäle
- `channels/channel_router.sh` routed Antworten zurück
- `signal_normalize()` erkennt inline Contact-Daten und vCard-Attachments
- `process_handler()` speichert Contact-Cards in `~/.config/lydia/signal_contacts.json`

## Problem
Signal-Textnachrichten funktionieren (z.B. `/status`).
Signal Contact-Cards kommen bei `signal-cli receive` nicht an — weder im Lydia-Archiv noch bei manuellem Poll.

## Bereits getestet
- `signal-cli -u <phone-redacted> -o json receive -t 10 --send-read-receipts` gibt leere Ausgabe zurück
- Account-Status: `<phone-redacted>: true` (registriert)
- Service läuft sauber, keine Errors im Journal

## Mögliche Ursachen
1. Contact-Card wird an falsche Nummer / falschen Chat geschickt
2. Signal-Delivery-Verzögerung oder Primary/Secondary-Device-Sync-Problem
3. signal-cli benötigt evtl. zusätzlichen Trust/Verifikation für Contact-Card-Attachments
4. Contact-Cards von Signal Desktop vs. Signal Mobile werden unterschiedlich behandelt

## Code-Stand
- `runtime/messenger/channels/signal.sh`: Contact-Card-Erkennung implementiert
- `runtime/messenger/messenger_lydia.sh`: Contact-Card-Handler implementiert
- Tests: `runtime/tests/test_messenger.sh` SC1–SC3 passen

## Nächste Schritte
1. Vom User eine normale Textnachricht an die Lydia-Signal-Nummer schicken lassen, um Delivery zu verifizieren
2. Contact-Card erneut senden und `signal-cli receive` direkt beobachten
3. Falls nötig: signal-cli mit `--debug` oder `--verbose` laufen lassen
4. Falls Delivery grundsätzlich klappt, aber Cards nicht: Signal-Envelope-Struktur für Contact-Cards loggen
