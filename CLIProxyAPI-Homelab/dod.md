# Definition of Done

- Architektur- und Compliance-Spike ist dokumentiert; Zielhost und erlaubte Provider sind entschieden.
- Gepinntes Container-Image und Compose-Konfiguration sind versioniert.
- Der Gateway ist intern erreichbar und von extern nicht erreichbar.
- Management API, Control Panel, Plugins und Debug-Endpunkte sind deaktiviert oder explizit gehaertet.
- Secrets liegen nicht im Repository und besitzen minimale Dateirechte.
- OpenCode ist als Pilotclient erfolgreich integriert.
- Healthcheck, Monitoring, Log-Rotation, Backup, Restore, Update und Rollback sind getestet und dokumentiert.
- Sicherheits- und Funktionstests aus `tests.md` bestehen.
- Betriebsdokumentation beschreibt Credential-Onboarding, Rotation, Providerausfall und vollstaendige Abschaltung.
- Slarti und Lydia erhalten erst nach erfolgreichem Pilotbetrieb eigene, getrennte Client-Keys.