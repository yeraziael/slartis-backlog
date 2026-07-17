# Risiken und technische Schulden

## Bekannte technische Schulden

1. **Synapse-Konfiguration enthält Placeholder** — `synapse.yaml.example`
   muss vor Deployment substituiert werden. Kein automatisiertes
   Config-Template-Rendering vorhanden.
2. **PostgreSQL-Passwort in .env.example** — Der Compose-Stack erwartet
   Secrets via Docker-Secrets-Mechanismus, aber der PoC nutzt env-Vars.
   Produktiv-Umstellung auf Docker-Secrets ist dokumentiert aber nicht
   automatisiert.
3. **Keine Federation-Tests** — Federation ist deaktiviert, aber ein
   versehentliches Aktivieren wäre nicht durch CI abgedeckt.
4. **E2EE nicht unterstützt** — Lydia als Bot kann E2EE-Räume nicht
   verarbeiten. Das ist eine bewusste Entscheidung (siehe ADR), aber
   schränkt die Nutzung für vertrauliche Kommunikation ein.
5. **Adapter-State in JSON-Datei** — Der Sync-Cursor wird in einer
   JSON-Datei persistiert. Bei gleichzeitigem Schreibzugriff könnte
   State verloren gehen (derzeit Single-Process-Architektur).

## Follow-up-Issues

- **Federation-Option dokumentieren** — Sollte später Federation gewünscht
  sein, muss Port 8448 freigegeben und die Well-Known-Konfiguration aktiviert
  werden
- **Synapse-Version automatisiert aktualisieren** — Derzeit manuelles
  Image-Digest-Pinning
- **E2EE für Bot-Konten** — Erfordert ein separates Issue, wenn Bedarf
  entsteht
- **Voice-Transkription** — Audio-Attachments werden erfasst, aber nicht
  transkribiert (separates Issue)
- **Bridge-Loop-Tests im Parallelbetrieb** — Test S15 ist dokumentiert,
  aber nicht automatisiert

## Nicht-Ziele

- **Kein Ersatz für Gitea Issues** — Matrix transportiert Befehle und
  Benachrichtigungen, aber Task-Status bleibt in Gitea
- **Keine automatische Benutzerregistrierung** — Alle Konten werden
  administrativ angelegt
- **Keine vollständige Telegram/Signal-Ablösung** — Beide bleiben als
  externe Fallback-Kanäle aktiv
- **Kein öffentlicher Zugang** — Matrix ist nur intern oder über VPN
  erreichbar
- **Keine WhatsApp-Bridge** — Nicht im Scope (separate Entscheidung)
- **Kein Deployment aus CI** — CI validiert nur; Deployment bleibt
  manuelle Operator-Aktion
