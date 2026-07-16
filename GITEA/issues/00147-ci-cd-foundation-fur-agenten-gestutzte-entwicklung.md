---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#147
state: closed
updated_at: 2026-07-14T00:32:27+02:00
is_epic: true
labels:
  []
publication: sanitized
---

# CI/CD Foundation für Agenten-gestützte Entwicklung

Epic: CI/CD Foundation für Agenten-gestützte Entwicklung

Ziel

Aufbau einer wiederverwendbaren CI/CD-Infrastruktur für das Homelab-Agenten-Ökosystem.

Die Pipeline soll als Qualitäts- und Sicherheits-Gate zwischen Agentenänderungen und produktiven Systemen dienen.

Besonderer Fokus:
Lydia ist ein eingeschränkter Execution-Agent. Die Infrastruktur muss daher möglichst viel Validierung, Kontrolle und Feedback übernehmen, damit Lydia auch bei zeitweiser Abwesenheit von Slarti sicher arbeiten kann.

⸻

Hintergrund

Aktueller Zustand:

* Mehrere gekoppelte Projekte:
    * Lydia Agent
    * Messenger-Container (Telegram/Signal)
    * Paperless-Integration
    * weitere Homelab-Services
* Gitea als zentrale Versionsverwaltung
* Shell-basierte Komponenten mit umfangreicher Testsuite (~170 Tests)
* Docker-basierte Services
* Lokale LLM-Infrastruktur mit begrenzten Ressourcen

Problem:

Ohne CI/CD müssen Agenten und Menschen manuell prüfen, ob Änderungen Nebenwirkungen verursachen.

Risiken:

* Regressionen
* beschädigte Services
* unnötige Agenteniterationen
* hoher Kontextverbrauch
* schwierige Wiederherstellung

⸻

Architekturziel

Etablieren eines Entwicklungsflusses:

Issue
  ↓
Agent bearbeitet Aufgabe
  ↓
Git Commit
  ↓
CI Pipeline
  ↓
Tests / Validierung
  ↓
Review / Freigabe
  ↓
Deployment

Die Pipeline ist der technische Qualitätsprüfer.

⸻

Anforderungen

1. Repository-Standard

Definiere eine einheitliche Struktur für Agenten-Projekte.

Jedes Projekt soll unterstützen:

project/
├── src/
├── tests/
├── docs/
├── agents/
│   ├── ARCHITECTURE.md
│   ├── OPERATIONS.md
│   ├── DECISIONS.md
│   └── KNOWN_ISSUES.md
├── .ci/
└── README.md

Ziel:

Ein Agent soll den Projektkontext verstehen können, ohne komplette Historien durchsuchen zu müssen.

⸻

2. CI Pipeline

Implementiere eine Pipeline-Basis mit:

Pflichtschritten

* Repository Checkout
* Syntaxprüfung
* Qualitätsprüfung
* Testausführung
* Ergebnisreporting

Für Shell-Projekte:

* ShellCheck
* Unit Tests
* Integrationstests (wenn vorhanden)

⸻

3. Maschinenlesbare Ergebnisse

Die Pipeline muss Ergebnisse liefern, die von Lydia verarbeitet werden können.

Erforderlich:

* eindeutiger Exit-Code
* klare Fehlerbeschreibung
* betroffene Datei
* betroffene Testfälle
* Logs

Beispiel:

STATUS: FAILED
Component:
signal_handler.sh
Failure:
test_voice_message_timeout
Location:
line 143
Suggested action:
Review timeout handling

⸻

4. Deployment-Schutz

Kein ungeprüftes Deployment.

Minimaler Ablauf:

Commit
 ↓
CI erfolgreich
 ↓
Freigabe
 ↓
Deployment

Die Pipeline muss verhindern, dass fehlerhafte Änderungen produktive Systeme erreichen.

⸻

5. Lydia-Kompatibilität

Berücksichtigen:

Lydia darf:

* definierte Aufgaben bearbeiten
* Code ändern
* Tests ausführen
* Dokumentation aktualisieren

Lydia darf nicht:

* Architektur eigenständig ändern
* Sicherheitsgrenzen umgehen
* Produktionssysteme ungeprüft verändern

Die Pipeline muss Lydia unterstützen durch:

* klare Fehlerberichte
* reproduzierbare Tests
* definierte Erfolgskriterien

⸻

6. Wiederverwendbarkeit

Die Pipeline muss als Vorlage für weitere Projekte nutzbar sein.

Ziel:

Neues Projekt anbinden mit:

* minimaler Konfiguration
* vorhandenen Templates
* dokumentiertem Vorgehen

⸻

7. Dokumentation

Erstellen:

Entwicklerdokumentation

* Pipeline-Aufbau
* Komponenten
* Erweiterung

Betriebsdokumentation

* Start
* Fehleranalyse
* Wiederherstellung

Agent-Dokumentation

* Wie Lydia die Pipeline nutzt
* Welche Fehlerinformationen erwartet werden

⸻

Nicht-Ziele

Nicht Bestandteil dieser Aufgabe:

* Lydia autonomer machen
* Architekturentscheidungen automatisieren
* vollständige autonome Deployments
* Sicherheitsrechte erweitern

⸻

Priorisierung

Phase 1: Fundament

* Pipeline Framework auswählen
* Erstes Projekt integrieren
* Tests automatisch ausführen

Phase 2: Agent-Unterstützung

* strukturierte Reports
* Agent Context Dateien
* Runbooks

Phase 3: Skalierung

* Templates
* weitere Projekte anbinden
* Deployment-Automatisierung

⸻

Definition of Done

Die Aufgabe gilt als abgeschlossen wenn:

[ ] Ein bestehendes Projekt läuft erfolgreich durch die Pipeline

[ ] Die Testsuite wird automatisch ausgeführt

[ ] Fehler werden verständlich gemeldet

[ ] Lydia kann aus einem Pipeline-Fehler eine konkrete Aufgabe ableiten

[ ] Ein zweites Projekt kann mit geringem Aufwand integriert werden

[ ] Dokumentation ist vorhanden

[ ] Keine Änderung kann ungeprüft produktiv gehen

⸻

Leitprinzip

Die Pipeline soll Slarti nicht ersetzen.

Sie soll dafür sorgen, dass Lydia innerhalb sicherer Grenzen zuverlässig arbeiten kann.
