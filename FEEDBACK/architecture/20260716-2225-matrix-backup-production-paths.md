---
feedback_version: architecture-feedback/v1
id: AF-20260716-2225-matrix-backup-production-paths
created_at: 2026-07-16T22:25:36+01:00
author: slarti
severity: blocking
status: open
source_repository: Homelab/Architecture
source_ref: 7c4eb8e
related_epic: matrix-server-212
related_work_item: matrix-backup-235
responds_to: none
supersedes: none
---

# Matrix-Backupvertrag bildet Produktionspfade nicht ab

## Beobachtung

Der gemergte Backup- und Restore-Vertrag aus Work Item #235 adressiert die
isolierte Synapse-PoC-Struktur. Die ebenfalls gemergte Produktions-Compose-Datei
verwendet andere Container- und Volume-Pfade.

## Evidenz

- `pi/backupMatrix.sh` sichert `/mnt/hardDrive/docker/synapse-poc/*` und den
  Container `synapse-poc-db`.
- `pi/restoreMatrix.md` stellt in dieselben PoC-Pfade wieder her.
- `pi/compose/synapse.yml` bindet Produktionsdaten unter
  `/mnt/hardDrive/docker/synapse/*` ein und verwendet keinen
  `synapse-poc-db`-Containernamen.
- Der lokale Architektur-CI-Lauf ist gruen, prueft aber nur den vorhandenen
  PoC-Vertrag und erkennt diese Profilabweichung nicht.

## Auswirkung

Ein Operator koennte vor einem Produktions-Upgrade ein formal erfolgreiches,
aber fuer die Produktionsdaten unvollstaendiges Backup erzeugen. Ein Restore
nach dem vorhandenen Dokument wuerde nicht den produktiven Datenbestand
wiederherstellen.

## Empfehlung

Vor Produktionsdeployment oder Upgrade einen getesteten Produktionsvertrag
fuer Datenbank-Dump, Medien, Signing-Key, Konfiguration und Adapter-State
erstellen. Das Matrix-Release-Profil aus Work Item #241 soll diese Artefakte
und ihre Checksummen mechanisch referenzieren. PoC- und Produktionspfade
bleiben explizit getrennt; keine automatische Pfaduebersetzung.

## Benoetigte Entscheidung

Soll die Produktionsvariante als expliziter Vorganger von #241 umgesetzt
werden, oder wird der Scope von #241 um Backup-/Restore-Artefakte und deren
Blackbox-Test erweitert?

## Stop-Bedingung

Kein produktives Matrix-Deployment, Upgrade oder Restore, bis ein
produktionskompatibler Backup-Nachweis und ein erfolgreich getesteter Restore
vorliegen.
