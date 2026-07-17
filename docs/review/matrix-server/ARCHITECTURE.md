# Architekturentscheidungen

## Homeserver: Synapse + PostgreSQL

| Kriterium | Synapse | Continuwuity | Dendrite |
|---|---|---|---|
| ARM64 | ✅ | ✅ | ⚠️ experimentell |
| Docker | ✅ Official | ✅ Community | ⚠️ |
| OIDC | ✅ Native | ⚠️ | ✅ |
| Reife | ✅ Sehr stabil | ⚠️ Neu | ⚠️ Unstable |
| RAM Idle | ~150MB | ~50MB | ~100MB |
| Docs | ✅ Exzellent | ⚠️ Begrenzt | ⚠️ Begrenzt |

**Entscheidung:** Synapse, weil:
- Stabilster und am besten dokumentierter Homeserver
- Native OIDC-Integration mit Keycloak
- Größte Community und aktivste Weiterentwicklung
- ARM64-Docker-Image verfügbar

**Datenbank:** PostgreSQL 16 (einheitliche DB-Strategie mit Keycloak, Paperless)

## Authentifizierung: Keycloak OIDC

- Operator-Logins via bestehendem Keycloak (auth.hl.maier.wtf)
- Lydia, Slarti, Veklinge als dedizierte Matrix-Servicekonten
- Keine offene Registrierung
- Break-Glass-Admin-Account mit lokalem Password

## Betriebsmodus: Privat (keine Federation)

- Kein Port 8448
- Client-only Listener
- Federation nur bei explizitem Bedarf aktivierbar

## Adapter-Sprache: Python

Bewertet wurden Python, Go und Rust:

| Kriterium | Python | Go | Rust |
|---|---|---|---|
| Matrix-SDK | Custom stdlib (urllib) | mautrix (reif) | Kein reifes SDK |
| Async-I/O | asyncio | Goroutines | tokio |
| ARM64 | ✅ | ✅ | ✅ |
| RAM (idle) | ~30MB | ~10MB | ~5MB |
| Team-Erfahrung | Hoch | Mittel | Gering |

**Entscheidung:** Python mit **eigenem stdlib-basierten Matrix-Client**
(`urllib` + `json`), kein externes SDK (matrix-nio). Gründe:

- **Angriffsfläche minimieren:** `client.py` umfasst ~230 Zeilen ohne externe
  Abhängigkeiten. matrix-nio hat tausende Zeilen mit asyncio-Transports,
  Olm-Verschlüsselung, E2EE-Keys und einem komplexen Event-Loop. Unser Adapter
  benötigt nur Sync-Endpunkt + Media-Download.
- **Vollständige Kontrolle:** Retry-, Redirect-, Auth-, Timeout- und
  Fehlerbehandlung sind explizit und auditierbar. Keine versteckten
  Defaults in Bibliotheken.
- **Deterministisches Polling:** Synchroner urllib-Request ist einfacher
  zu debuggen und zu testen als asyncio-Loop mit Callbacks.
- **Keine Patch-Pflicht:** Bei matrix-nio-Updates müsste die Adapter-Schnittstelle
  stabil bleiben; bei eigenem Client ist die Wartungsfläche vorhersagbar.
- **Nachteli:** Erhöhte Eigenentwicklung bei Retry-, Redirect- und
  Fehlerbehandlung — durch explizite Tests und Redaktion abgesichert.

# Verworfenen Alternativen

1. **matrix-nio** — Das ausgereifteste Python-Matrix-SDK wurde nach
   Prototyping verworfen: 3000+ Zeilen asyncio-Overhead für Sync + Media,
   unerwünschte Abhängigkeiten (Olm, E2EE), erschwerte Testbarkeit und
   größere Angriffsfläche. Ersetzt durch 230 Zeilen stdlib.
2. **Continuwuity** — Vielversprechend (Rust, ressourcenschonend), aber zu neu
   und unzureichend dokumentiert für den Produktivbetrieb
2. **Dendrite** — Offizieller Synapse-Nachfolger von Matrix.org, aber noch nicht
   stabil genug (experimentelles ARM64-Image)
3. **Go als Adapter-Sprache** — Wäre ressourcenschonender, aber der
   Custom-Client (Python/stdlib) ist wartbarer als mautrix
4. **Signal als einzigen Messenger** — Zu wartungsintensiv (signal-cli,
   JSON-RPC-Probleme mit Attachments)
5. **Big-Bang-Migration** — Verworfen zugunsten schrittweisem Parallelbetrieb

# Auswirkungen auf bestehende Komponenten

## Messenger-Architektur
- Container pollt weiterhin Telegram + Signal
- Zusätzlich: Matrix-Inbound-Adapter (Python) als dritter Polling-Kanal
- Host-Processor dispatches weiterhin normalisiert
- Keine Änderung am bestehenden Telegram/Signal-Pfad

## CI/CD
- Neue CI-Gates: compose-validate, scan-secrets
- CI-Generator-Tests erweitert mit Matrix-Fixture-Assertions
- Release-Manifest-Validierung für Matrix-Profil

## Security
- channels.json nicht mehr im Git
- Secret-Scan-Guard in Pre-Commit + CI
- Externer Config-Pfad für Runtime-Konfiguration

## Backup
- Matrix-spezifische backupMatrix.sh
- Fünf Artefaktklassen: DB-Dump, Medien, Signing-Key, Config, Adapter-State

## Monitoring
- Health-Endpunkt mit Sync-Lag, Delivery-Failures, Quarantän
- Fallback-Alerting über Telegram bei Matrix-Ausfall
