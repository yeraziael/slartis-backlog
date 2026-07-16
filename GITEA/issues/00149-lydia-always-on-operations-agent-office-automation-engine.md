---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#149
state: open
updated_at: 2026-07-14T00:34:20+02:00
is_epic: true
labels:
  - "Systemarchitektur"
  - "epic"
  - "in-progress"
  - "project:homelab-agenten-ausbau"
publication: sanitized
---

# Lydia Always-On Operations Agent & Office Automation Engine

## Ziel

Lydia soll zu einem Always-on Execution Agent auf dem Raspberry Pi 5 werden.

Sie übernimmt zwei klar getrennte Aufgabenbereiche:

1. **Agent Operations**

   * technische Aufgaben aus Gitea bearbeiten
   * wiederkehrende Agenten-Workflows ausführen
   * mit Slarti zusammenarbeiten

2. **Digital Office Assistant**

   * Paperless-Dokumente verarbeiten
   * Fristen und Aktionen erkennen
   * Benutzer über Signal/Telegram einbinden

Lydia muss unabhängig vom Rechenknecht funktionieren.

Der Rechenknecht mit Ollama ist eine optionale Ressource für anspruchsvollere KI-Aufgaben, aber keine notwendige Abhängigkeit.

---

# Architekturprinzipien

## Always-On Basis

Primäre Laufzeit:

* Raspberry Pi 5 (8GB RAM)
* Lydia Runtime
* Gitea
* Paperless-ngx
* Messenger-Schnittstelle

Optional:

* Rechenknecht Gaming-PC
* Ollama
* GPU-Modelle

Regel:

> Lydia muss alle Kernfunktionen ohne Ollama ausführen können.

---

# Systemrollen

## Slarti

Verantwortung:

* Architektur
* komplexe Planung
* technische Reviews
* Erstellung von Entwicklungsaufgaben

Arbeitskanal:

* Gitea Issues

---

## Lydia

Verantwortung:

* Ausführung
* Überwachung
* Kommunikation
* Automatisierung
* Statusmeldungen

Lydia ist kein Architekt.

Lydia führt definierte Prozesse aus.

---

# Bereich 1: Gitea Agent Operations

## Ziel

Gitea wird das technische Operations Center.

Lydia überwacht definierte Repositories und Issues.

Fähigkeiten:

* neue Issues erkennen
* Labels auswerten
* Prioritäten berücksichtigen
* Aufgaben übernehmen
* Fortschritt melden
* Ergebnisse dokumentieren
* Fehler eskalieren

Workflow:

```
Slarti erstellt Issue
        |
        v
Lydia erkennt Task
        |
        v
Validierung
        |
        v
Ausführung
        |
        v
Tests / Checks
        |
        v
Ergebnis zurück an Gitea
```

---

# Bereich 2: Lydia Scheduler

## Ziel

Lydia benötigt eine eigene Scheduling-Komponente.

Fähigkeiten:

* wiederkehrende Aufgaben verwalten
* Zeitpläne persistent speichern
* Ausführung protokollieren
* Fehler behandeln

Beispiele:

## Architektur-Review

Intervall:
wöchentlich

Ablauf:

* Lydia startet Gespräch
* stellt definierte Fragen
* sammelt Antworten
* erzeugt Zusammenfassung
* erstellt bei Bedarf Gitea Issue für Slarti

---

## System Checks

Beispiele:

* Backup-Status
* Container-Status
* Speicherplatz
* offene Aufgaben
* Sicherheitsprüfungen

---

# Bereich 3: Messenger Interface

Lydia kommuniziert über:

* Signal
* Telegram

Fähigkeiten:

* Nachrichten senden
* Antworten empfangen
* Kontext verwalten
* Aufgaben aus Gesprächen erzeugen

Beispiel:

```
Lydia:
"Ich habe einen offenen Punkt gefunden.
Soll ich daraus eine Aufgabe machen?"

User:
"Ja"

Lydia:
erstellt Gitea Issue
```

---

# Bereich 4: Paperless Office Automation

## Ziel

Paperless ist Lydias digitaler Posteingang.

Paperless enthält:

* Briefe
* Rechnungen
* Verträge
* Bescheide
* Verwaltungsdokumente

Paperless enthält NICHT:

* Programmierwissen
* Agent Memory
* technische Dokumentation

---

## Workflow

```
Neues Dokument in Paperless
          |
          v
Lydia erkennt Eingang
          |
          v
Dokument analysieren
          |
          v
Aktion ableiten
          |
          v
Benutzer informieren
```

Beispiele:

### Rechnung

Erkennen:

* Anbieter
* Betrag
* Zahlungsfrist

Aktion:

* Erinnerung erzeugen
* Status melden

---

### Vertrag

Erkennen:

* Vertragspartner
* Laufzeit
* Kündigungsfrist

Aktion:

* Erinnerung planen

---

### Brief

Erkennen:

* Absender
* Thema
* erforderliche Handlung

Aktion:

* Benutzer fragen

---

# Bereich 5: KI Provider Layer

## Prinzip

KI ist austauschbar.

Priorität:

```
1. Lokale Logik
       |
       v
2. Ollama verfügbar?
       |
       v
3. Lokales Modell verwenden
       |
       v
4. Keine KI verfügbar:
       Queue / Eskalation
```

Ollama ist ein Accelerator.

Keine Kernabhängigkeit.

---

# Bereich 6: Memory und State

## Technisches Agent Memory

Speicher:

* Lydia Home Repo
* Gitea
* SQLite State DB

Enthält:

* Aufgabenstatus
* Policies
* Workflow-Zustand
* technische Entscheidungen

---

## Dokumentwissen

Speicher:

* Paperless

Enthält:

* private Dokumente
* Büroinformationen
* Verwaltungsunterlagen

Strikte Trennung.

---

# Bereich 7: CI/CD Integration

Alle Änderungen an Lydia müssen kontrolliert erfolgen.

Pipeline:

```
Git Commit
      |
      v
CI Pipeline
      |
      +-- Unit Tests
      +-- Integration Tests
      +-- Policy Checks
      |
      v
Deployment
      |
      v
Lydia Runtime
```

Definition:

Kein manueller Produktionspatch ohne Pipeline.

---

# Sicherheitsgrenzen

Lydia darf:

* eigene Dateien verwalten
* Tasks ausführen
* Container User-Workloads starten
* Reports erzeugen
* Issues erstellen

Lydia darf nicht:

* Rechte erweitern
* Policies ändern
* Systemkonfiguration eigenständig verändern

Systemänderungen:

```
Lydia erstellt Issue
        |
        v
Review
        |
        v
Freigabe
```

---

# Definition of Done

## Core

* [ ] Lydia läuft stabil 24/7 auf Pi5
* [ ] Scheduler funktioniert
* [ ] Task State ist persistent

## Gitea Integration

* [ ] Issue Monitoring funktioniert
* [ ] Task Lifecycle implementiert
* [ ] Ergebnisse werden zurückgeschrieben

## Messenger

* [ ] Signal Kommunikation
* [ ] Telegram Kommunikation
* [ ] Dialoge können Tasks erzeugen

## Paperless

* [ ] Dokumenteingänge werden erkannt
* [ ] Verarbeitungspipeline existiert
* [ ] Aktionen können erzeugt werden

## CI/CD

* [ ] Tests laufen automatisch
* [ ] Deployment reproduzierbar
* [ ] Rollback möglich

## Ollama

* [ ] Optionaler Provider
* [ ] Kein Hard Dependency

---

# Priorisierung

## P0

1. CI/CD Pipeline fertigstellen
2. Lydia Task Engine
3. Scheduler
4. Messenger Workflow

## P1

5. Paperless Office Automation
6. Ollama Provider
7. Erweiterte Workflows

## P2

8. Selbstoptimierung
9. Erweiterte Agentenfähigkeiten

---

# Ergebnis

Nach Abschluss ist Lydia:

* ein Always-On Agent auf dem Pi5
* über Signal/Telegram erreichbar
* durch Gitea steuerbar
* durch CI/CD abgesichert
* unabhängig von Ollama
* fähig, Büroprozesse über Paperless zu automatisieren
* erweiterbar durch Slarti geplante Workflows

---
[internal attachment omitted]
