# Matrix Server — Implementierungs-Review

## Ziel

Aufbau eines eigenen Matrix-Homeservers (Synapse + PostgreSQL + Keycloak OIDC)
auf dem Raspberry Pi 5 als primären internen Kommunikationskanal für Lydia,
Slarti und Veklinge. Telegram und Signal bleiben als externe Fallback-Gateways
erhalten.

## Motivation

- **Externe Abhängigkeit:** Telegram und Signal sind nicht selbst kontrolliert
- **Fragmentierte Nachrichtenverarbeitung:** Signal-cli ist wartungsintensiv,
  Telegram und Signal haben unterschiedliche Limits
- **Kein interner Kanal:** Kein einheitlicher, selbst betriebener
  Kommunikationsweg für Agenten
- **Chunking, State und Error-Handling** müssen für jeden Kanal separat
  implementiert werden

## Umfang

Das Epic umfasst 25 Subtasks (#215–#245) in 7 Phasen:

1. **CI/Merge-Basis** (#242, #243) — Architecture PR-Gates, Eddie Auto-Merge
2. **ADR + PoC** (#215, #217) — Synapse-Entscheidung, ARM64-PoC
3. **Daten/Volumes** (#218, #219) — PostgreSQL, Synapse Docker-Compose
4. **Proxy/OIDC/Client** (#220–#222, #244, #245) — Reverse Proxy, Discovery,
   Keycloak, Element, TURN
5. **Adapterkette** (#223–#233) — Identitäten, Räume, Envelope, Inbound/
   Outbound, Sync-Cursor, Chunking, Attachments, Approvals, Bridge-Loop-Prävention
6. **Hardening/Monitoring/Backup/CI** (#234–#237, #241) — Security, Monitoring,
   Backup, Release-Profil
7. **Parallelbetrieb/Freigabe** (#238–#240) — 7-Tage-Test, Runbook, Primary
   Channel Declaration

## Betroffene Komponenten

| Komponente | Repository | Änderung |
|---|---|---|
| Synapse | architecture | Neues Docker-Compose, Config, PoC |
| PostgreSQL | architecture | Docker-Compose, Volume-Konzept |
| Coturn (TURN) | architecture | Neues Docker-Compose, Config |
| Element Web | architecture | Neues Docker-Compose, Config |
| nginx-proxy | architecture | Neue Location-Blöcke, ACME |
| Keycloak | architecture | OIDC-Client-Template |
| Lydia Messenger | home-repo | Matrix-Adapter (Python) |
| Lydia CI | home-repo | CI-Gates, Generator-Tests |
| Lydia Security | home-repo | Secret-Scan, Channels-Config |
| Monitoring | home-repo | Health-Endpunkt, Alerts |
| Backup | architecture | Backup-Script, Restore-Guide |
| Release Management | architecture | Release-Profil, Manifest |

## Breaking Changes

- **channels.json** nicht mehr in Git getrackt (nur .example)
- **CHANNEL_DEFAULT** wechselt von Telegram zu Matrix (nach Freigabe)
- **Runtime-Konfiguration** über CHANNELS_CONFIG-Env-Var oder
  /var/lydia/config/channels.json (nicht mehr runtime/messenger/channels.json)
- **Adapter-Architektur:** Python statt Bash für Matrix-Integration

## Offene Fragen

- Wann erfolgt die explizite Operator-Abnahme für #240?
- TURN benötigt DNS-CNAME + Firewall-Freigabe (Operator-Aktion)
- CNAMEs für matrix.hl.maier.wtf und element.hl.maier.wtf fehlen noch
- PostgreSQL-Passwort-Rotation vor Produktivbetrieb?
- Monitoring-Alerts an Telegram bereits getestet?
