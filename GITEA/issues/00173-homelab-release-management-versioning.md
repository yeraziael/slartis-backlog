---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#173
state: open
updated_at: 2026-07-14T16:54:32+02:00
is_epic: true
labels:
  - "Systemarchitektur"
  - "epic"
  - "project:homelab-agenten-ausbau"
  - "ready"
publication: sanitized
---

# Homelab Release Management & Versioning

Ziel
Aufbau eines standardisierten Release-Managements für alle Homelab-Repositories.
Nach erfolgreicher CI/CD soll aus einer freigegebenen Version automatisch ein reproduzierbarer Gitea-Release entstehen. Releases bilden künftig die einzige unterstützte Installations- und Deployment-Basis für Lydia und andere Komponenten. Deployments aus beliebigen Commits oder direkt aus main sind langfristig nicht mehr vorgesehen.


⸻


Hintergrund
Die CI/CD-Pipeline stellt sicher, dass Änderungen gebaut und getestet werden.
Dieses Epic erweitert den Software-Lifecycle um eine offizielle Release-Phase.
Jeder Release muss:
eindeutig versioniert sein,
reproduzierbar gebaut werden können,
nachvollziehbar dokumentiert sein,
alle benötigten Artefakte enthalten,
für Rollbacks geeignet sein.


⸻


Scope
Versionierung
SemVer (MAJOR.MINOR.PATCH) als Standard einführen.
Versionierungsrichtlinien dokumentieren.
Einheitliche Tag-Konvention (vX.Y.Z) definieren.


⸻


Release Workflow
Automatischer Ablauf:
CI erfolgreich
Release-Kandidat bestimmen
Git-Tag erzeugen oder validieren
Gitea Release erstellen
Release Notes generieren
Artefakte anhängen
Release veröffentlichen


⸻


Release Assets
Repositoryabhängig unterstützen:
Docker Images
tar.gz
zip
Konfigurationsdateien
compose-Dateien
PDF-Dokumentation
SHA256-Checksummen


⸻


Release Notes
Automatische Erstellung aus:
Commits
Merge Requests
geschlossenen Issues
Optional:
Conventional Commits unterstützen.


⸻


Changelog
Automatisches CHANGELOG pflegen.
Mindestens:
Features
Fixes
Breaking Changes


⸻


Gitea Integration
Nutzung der Gitea Release API oder Tea CLI.
Vollständig automatisierte Release-Erstellung.
Unterstützung für Draft Releases und Pre-Releases.


⸻


Rollback
Jeder Release muss:
eindeutig referenzierbar sein,
reproduzierbar gebaut werden können,
jederzeit erneut deploybar sein.


⸻


Repository Standardisierung
Für alle Homelab-Repositories einheitlich:
identische Release-Struktur
identisches Versionierungsschema
identische Namenskonventionen
identische Pipeline-Schritte


⸻


Nicht Bestandteil dieses Epics
automatisches Deployment
Canary Releases
Blue/Green Deployments
Multi-Node Rollouts
Diese Themen gehören in das Deployment-Epic.


⸻


Deliverables
Release-Guideline
Versionierungsrichtlinie
Release-Pipeline
automatisierte Release Notes
automatisches Changelog
Gitea Release Integration
Release-Artefakte
Rollback-Konzept


⸻


Definition of Done
Alle Homelab-Repositories unterstützen ein einheitliches Release-Verfahren.
Nach erfolgreicher CI kann automatisch ein Gitea-Release erstellt werden.
Jeder Release besitzt eine SemVer-Version.
Jeder Release enthält Release Notes und die definierten Artefakte.
Releases sind reproduzierbar.
Rollbacks auf frühere Releases sind möglich.
Die Dokumentation beschreibt den vollständigen Release-Prozess.


⸻


Abhängigkeiten
Voraussetzung:
CI/CD Foundation Epic abgeschlossen.
Nachgelagerte Epics:
Deployment Automation
Release Consumption durch Lydia
Automatische Update-Strategien
Multi-Repository Release Coordination


⸻


Architekturhinweis
Releases werden künftig zum offiziellen Übergabepunkt zwischen Entwicklung und Betrieb.
Slarti entwickelt gegen Branches und Pull Requests.
Die CI validiert Änderungen.
Releases markieren freigegebene Versionen.
Lydia konsumiert ausschließlich veröffentlichte Releases und niemals ungeprüfte Commits oder den aktuellen Stand von main. Dadurch werden reproduzierbare Deployments, sichere Rollbacks und eine stabile Runtime gewährleistet.
