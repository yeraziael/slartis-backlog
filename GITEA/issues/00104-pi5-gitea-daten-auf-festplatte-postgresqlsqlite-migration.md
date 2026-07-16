---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#104
state: closed
updated_at: 2026-07-03T15:10:36+02:00
is_epic: false
labels:
  - "Aufgaben"
publication: sanitized
---

# Pi5 Gitea: Daten auf Festplatte + PostgreSQL→SQLite Migration

**Priority:** High

**Goal:** Gitea auf dem Pi5 (<internal-host>) muss persistente Daten auf die angeschlossene Festplatte schreiben (aktuell vermutlich SD-Karte) und von PostgreSQL auf SQLite migriert werden.

## Tasks
- [ ] Gitea-Data-Verzeichnis auf Festplatte umlegen (Daten- und Repo-Pfade)
- [ ] PostgreSQL→SQLite Migration durchführen (pg_dump → sqlite3 import)
- [ ] docker-compose/gitea.service anpassen
- [ ] Backup-Strategie für Festplatte prüfen
- [ ] Smoke-Test: Repos lesbar, Push/Pull funktioniert, Web-UI erreichbar

## Motivation
- SD-Karte ist Verschleißteil – häufige Schreibzugriffe verkürzen Lebensdauer drastisch
- PostgreSQL ist für Single-User-Gitea overengineered – SQLite reduziert Komplexität, RAM-Verbrauch und Backup-Aufwand
