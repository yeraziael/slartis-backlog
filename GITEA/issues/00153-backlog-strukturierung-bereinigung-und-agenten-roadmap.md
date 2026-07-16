---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#153
state: closed
updated_at: 2026-07-14T00:35:59+02:00
is_epic: false
labels:
  - "Systemarchitektur"
  - "done"
  - "project:homelab-agenten-ausbau"
publication: sanitized
---

# Backlog-Strukturierung, Bereinigung und Agenten-Roadmap

---


TICKET: Slarti - Backlog-Strukturierung, Bereinigung und Priorisierung der Agenten-Roadmap

Ziel:
Slarti soll den aktuellen Entwicklungs-Backlog des Agentensystems analysieren, bereinigen, strukturieren und priorisieren.

Ziel ist eine klare technische Roadmap mit:
- Epics
- Issues
- Abhängigkeiten
- Prioritäten
- empfohlener Umsetzungsreihenfolge

Damit sollen zukünftige Aufgaben gezielt an Lydia als Execution Layer übergeben werden können.

--------------------------------------------------

AUFTRAG AN SLARTI

Analysiere alle bestehenden Issues, Epics und offenen Arbeitspakete.

Durchzuführen:

1. Backlog bereinigen
- Duplikate erkennen und zusammenführen
- veraltete oder unklare Issues markieren
- fehlende technische Abhängigkeiten ergänzen
- große Themen in umsetzbare Arbeitspakete zerlegen

2. Priorisierung durchführen
Bewerte jedes Thema nach:
- technischem Nutzen
- Abhängigkeiten
- Beitrag zur Automatisierung
- Beschleunigung zukünftiger Entwicklung
- Bedeutung für Lydia als Execution Layer

3. Roadmap erstellen
Definiere:
- Reihenfolge der Umsetzung
- Blocker
- Voraussetzungen
- empfohlene nächste Schritte

--------------------------------------------------

AKTUELL BEKANNTER BACKLOG

==================================================
1. CI/CD Foundation
Priorität: Sehr hoch
Status: Aktiv
==================================================

Ziel:
Eine stabile Entwicklungs- und Qualitätssicherungsbasis für Agenten und Services schaffen.

Umfang:

- automatische Tests
- Build Checks
- Regression Tests
- Gitea Integration
- Validierung von Änderungen
- sichere Übergabe Slarti -> Lydia
- reproduzierbare Deployments

Bedeutung:
Grundlage für alle weiteren Entwicklungsfähigkeiten.

--------------------------------------------------

==================================================
2. Lydia Coding Capability / Execution Pipeline
Priorität: Sehr hoch
Status: Geplant
==================================================

Ziel:
Lydia soll strukturierte Coding-Aufträge von Slarti übernehmen und kontrolliert ausführen können.

Soll ermöglichen:

- Task Intake
- Worker Invocation
- isolierte Ausführung
- Codeänderungen
- Tests
- Review
- Definition-of-Done Prüfung
- Abschlussmeldung

Zielarchitektur:

Slarti
 |
 | Issue / Task
 v
Lydia
 |
 +-- Coding Worker
 |
 +-- Test Worker
 |
 +-- Review
 |
 v
Done


Diese Fähigkeit ist Voraussetzung dafür, dass Lydia eigene Entwicklungsaufgaben übernehmen kann.

--------------------------------------------------

==================================================
3. Lydia PDF Pipeline
Priorität: Hoch
Status: Stale seit ca. 2 Wochen
Abhängigkeit: Lydia Coding Capability
==================================================

Wichtig:
Die PDF Pipeline soll bewusst NACH Aufbau der Lydia Coding Capability weiterentwickelt werden.

Grund:
Die Pipeline soll mit Lydias eigener Coding-Fähigkeit erstellt, erweitert und verbessert werden.

Aktueller Stand:

- Paperless-ngx als Dokumentquelle
- Ingestion Daemon vorhanden
- Dokument-Snapshot vorhanden
- SQLite Index (agent.db) begonnen
- Dokumentverarbeitung vorbereitet

Ziel:

Lydia als digitale Bürosachbearbeiterin.

Fähigkeiten:

- Dokumente erfassen
- Metadaten verarbeiten
- Dokumente klassifizieren
- Workflows auslösen
- Aufgaben erzeugen
- geplante Verarbeitung durchführen

--------------------------------------------------

==================================================
4. Frontend Capability Skill
Priorität: Mittel
Status: Geplant
==================================================

Ziel:
Slarti benötigt eine allgemeine Fähigkeit zur Erstellung und Validierung von Frontends.

Diese Fähigkeit ist Voraussetzung für weitere Frontend-Skills.

Fähigkeiten:

- Frontend-Anforderungen analysieren
- Komponenten generieren
- UI implementieren
- Framework-Konventionen einhalten
- Design-Systeme verwenden
- Tests erzeugen
- Build und Qualitätschecks durchführen

--------------------------------------------------

==================================================
5. Frontend Best-of-N Skill
Priorität: Mittel
Abhängigkeit: Frontend Capability Skill
Status: Geplant
==================================================

Ziel:
Erweiterung des allgemeinen Frontend Skills um parallele Variantengenerierung und Auswahl.

Workflow:

Frontend Capability
        |
        v
Generate N Variants
        |
        v
Validation + Review
        |
        v
Judge Agent
        |
        v
Best Variant


Fähigkeiten:

- mehrere unabhängige Frontend-Varianten erzeugen
- Varianten vergleichen
- UX bewerten
- Codequalität bewerten
- Gewinner auswählen
- Integration vorbereiten

Der Skill soll nicht nur für ein Projekt gelten, sondern allgemeine Frontend-Entwicklung verbessern.

--------------------------------------------------

==================================================
6. Ægir Frontend
Priorität: Nach Frontend Skills
Abhängigkeiten:
- Frontend Capability Skill
- Frontend Best-of-N Skill
==================================================

Ziel:
Aufbau des Frontends für die Ægir Trading Platform.

Benötigte Bereiche:

- Trading Dashboard
- Portfolio Darstellung
- Risk Engine Visualisierung
- Broker Connector Status
- Scheduler Monitoring
- Memory/History Views

Vorgehen:

Nicht direkt eine Lösung bauen.

Erst:

Frontend Capability
        |
        v
Best-of-N Design Exploration
        |
        v
Auswahl der besten Architektur
        |
        v
Implementierung

--------------------------------------------------

==================================================
7. Tool Contract Registry Service (TCRS)
Priorität: Mittel/Niedrig
Status: Geplant
==================================================

Ziel:

Standardisierte Verträge zwischen Agenten und Tools schaffen.

Umfang:

- Tool Interfaces
- Manifeste
- Validierung
- Versionierung
- Agent Tool Usage Contracts

--------------------------------------------------

==================================================
8. Memory / Context Infrastructure
Priorität: Laufend
Status: Aktiv
==================================================

Betroffen:

- Agent Context
- Policy Matrix
- Lydia Home Repo
- versionierte Zustände
- Mímir Konzept für Ægir

Ziel:

Nachvollziehbare und kontrollierte Wissensverwaltung der Agenten.

--------------------------------------------------

ERWARTETES ERGEBNIS

Slarti erstellt:

1. Bereinigtes Backlog

Format:

Epic
Issue
Beschreibung
Status
Priorität
Abhängigkeiten


2. Technische Roadmap

Mit:

- Reihenfolge
- Begründung
- Blockern
- empfohlenen nächsten Schritten


3. Fehlende Issues

Falls notwendig:

- neue Tickets erzeugen
- bestehende Tickets aufteilen
- technische Details ergänzen


4. Priorisierungsentscheidung

Besonders beantworten:

- Was muss zuerst fertig werden, damit Lydia produktiv arbeiten kann?
- Welche Fähigkeiten erhöhen die Entwicklungsgeschwindigkeit am stärksten?
- Welche Aufgaben sollten zukünftig durch Lydia automatisiert erledigt werden?

--------------------------------------------------

EINSCHRÄNKUNG

Keine Implementierung starten.

Dieser Auftrag dient ausschließlich der Architektur-, Backlog- und Priorisierungsarbeit.

Output:
Ein sauber strukturierter Entwicklungsplan für die nächste Phase des Agentensystems.

---
[internal attachment omitted]
