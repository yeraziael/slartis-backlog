---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#131
state: closed
updated_at: 2026-07-14T00:32:26+02:00
is_epic: false
labels:
  []
publication: sanitized
---

# INFO: Lydia Messenger Architecture Change (Docker Container)

## Architecture Change: Lydia Messenger in Docker

### Was passiert ist
Lydia und Slarti laufen nicht mehr als systemd-Services auf Pi5, sondern in einem Docker-Container (`lydia-messenger`, alpine:3.19) auf Pi5.

### Neue Architektur
| Komponente | Wo | Beschreibung |
|---|---|---|
| Container `lydia-messenger` | Pi5 | Pollt Telegram (lydia + slarti) + Signal (JSON-RPC). Schreibt incoming/ in shared Volume |
| Container `signal-cli` | Pi5 | JSON-RPC daemon (raw TCP, Port 7583) |
| Host (Pi5) | shared Volume | Liest `<local-path-redacted>`, schreibt Antworten nach `outgoing/` |
| rechenknecht | unabhängig | Hat nur Ollama, kein Messenger mehr |

### File-based IPC
- Container schreibt eingehende Nachrichten als JSON nach `incoming/`
- Host liest, verarbeitet, schreibt Antwort als JSON nach `outgoing/`
- Container pollt `outgoing/` und sendet via Telegram/Signal

### Signal-JSON-RPC
- `signal-cli daemon --tcp` spricht **raw TCP**, kein HTTP
- `curl` sendet HTTP-Header → ungültig
- Stattdessen: `echo '{"jsonrpc":"2.0","id":1,"method":"..."}' | nc -w 5 signal-cli 7583`

### Für Slarti relevant
- Dein Telegram-Bot wird jetzt vom Container gepollt (nicht mehr systemd)
- Dein Offset-File: `/tmp/telegram_slarti_offset` (im Container)
- Deine Config: `container_channels.json` (Name: `slarti`, Token und Typ vorhanden)
- Host-Service `<email-redacted>` wurde gestoppt (ist disabled)
- **Konsequenz:** Slarti-Telegram-Bot läuft nur wenn der `lydia-messenger` Container auf Pi5 läuft

### Was offline ist
- `<home>/.config/lydia/channels.json` auf Pi5 hat **ungültiges JSON** (unquoted keys) – muss repariert werden falls der Host jemals wieder Direct-Calls macht
- `feature/signal-jsonrpc` Branch in `lydia/home-repo` ist bereits gemerged (PR #245)

### Details
Siehe `lessons/2026-07-10.md` in `OpenCodeAgent/opencode-context`.
