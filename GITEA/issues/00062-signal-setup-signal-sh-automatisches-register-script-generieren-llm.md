---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#62
state: closed
updated_at: 2026-06-30T10:39:23+02:00
is_epic: false
labels:
  []
publication: sanitized
---

# [Signal] setup_signal.sh — automatisches Register-Script generieren (LLM)

## Delegation an lokales LLM

### Task
Generiere `runtime/messenger/setup_signal.sh` — ein interaktives Bash-Script, das Signal-Registration automatisiert.

### Anforderungen
- signal-cli muss vorhanden sein (Pfad /opt/signal-cli/bin)
- `signal-cli -u <phone-redacted> register` ausführen
- User nach der SMS-PIN fragen (read)
- PIN verifizieren: `signal-cli -u <phone-redacted> verify <PIN>`
- Trust-On-First-Use: falls Captcha nötig, Code ausgeben und User bitten ihn per Signal zurückzusenden
- channels.json mit Signal-Pfad aktualisieren (Bereitschaft)
- systemd unit testen: `systemctl enable --now lydia-messenger@signal`
- Am Ende: Test-Nachricht an den Admin senden

### Output
- Script in: runtime/messenger/setup_signal.sh
- Ausführbar (chmod +x)
- bash -n sauber

### User-Daten
- Nummer: <phone-redacted>
- Admin-Chat-ID: 163442721 (@<operator>)
- Admin-Signal-Nummer: <phone-redacted> (gleiche Nummer, da SIM im Nokia)
