---
snapshot_version: gitea-epic-issue/v1
source: slarti/backlog#157
state: closed
updated_at: 2026-07-13T18:36:00+02:00
labels:
  - "Systemarchitektur"
  - "epic"
  - "project:homelab-agenten-ausbau"
  - "ready"
publication: sanitized
---

# Eddie – Homelab Orchestration & Scheduling Engine

# EPIC: Eddie – Homelab Orchestration & Scheduling Engine

**Status:** Specification / Backlog
**Priorität:** Hoch
**Ersetzt:** Eldir als Homelab-Scheduler (Eldir bleibt exklusiv in der Ægir Trading Platform)

## Hintergrund

Eddie ist der zentrale Scheduler, Event Router, Queue Manager und Dispatcher des Homelabs.

Eddie ersetzt den bisherigen Gitea-Task-Loop (`task_loop.sh`) als zentrale Orchestrierungskomponente.
Eldir bleibt exklusiv Bestandteil der Ægir Trading Platform und wird im Homelab **nicht** verwendet.

Eddie ist ein eigenständiger Docker-Container ohne LLM-Abhängigkeit, determiniert und erweiterbar.

## Architekturprinzipien

- **Eigenständiger Docker-Container** auf Pi5, neben Gitea, Paperless etc.
- **Keine LLM-Abhängigkeit** – alle Entscheidungen basieren auf konfigurierbaren Regeln und Policies
- **Deterministisches Verhalten** – gleiche Eingabe → gleiche Ausgabe
- **Keine Business- oder Fachlogik** – Eddie orchestriert, führt nicht selbst aus
- **HTTP REST API** – Kommunikation mit Lydia und anderen Komponenten via JSON
- **SQLite-Persistenz** – Jobs, History, Konfiguration überleben Container-Neustart
- **Erweiterbar** – neue Eventquellen und Executor ohne Kernarchitektur-Änderungen

## Rollenverteilung

| Rolle | Wer | Verantwortung |
|-------|-----|---------------|
| **Operator** | Michael | Definiert Ziele und Prioritäten |
| **Architekt** | Slarti | Entwickelt Architektur, Policies, Workflows; entscheidet WAS passiert |
| **Scheduler/Router** | Eddie | Entscheidet WANN und WER eine Aufgabe ausführt; managed Queues, Retries, Events |
| **Execution Engine** | Lydia | Führt Aufgaben aus, die Eddie dispatched |
| **Ephemere Worker** | Veklinge | Spezial-Worker, werden von Eddie bei Bedarf gestartet |

## Scope – Phase 1

### Scheduling
- Cron-Jobs (periodisch)
- Einmalige Jobs (deferred execution)
- Wiederkehrende Jobs
- Job-Prioritäten

### Event Routing (Phase 1: Gitea + Cron)
- Gitea-Events (Issues, PRs, Pushes) – ersetzt den aktuellen `task_loop.sh`
- Cron-getriggerte Events
- Später: Messenger-Nachrichten, Paperless-Ereignisse, Webhooks

### Queue Management
- Prioritäten-Warteschlangen
- Parallelisierung (konfigurierbar)
- Abhängigkeiten zwischen Jobs
- Retry mit Backoff (max. 3 Versuche, dann Escalation)
- Timeout pro Job
- Dead Letter Queue für endgültig fehlgeschlagene Jobs

### Dispatching
Eddie entscheidet:
- Welcher Executor zuständig ist (Lydia, Vekling, zukünftige Worker)
- Wann der Executor gestartet wird
- Welche Parameter übergeben werden

Eddie führt **nicht** aus – er delegiert.

### API (HTTP REST)
Interne Schnittstellen:
- `POST /jobs` – Job anlegen
- `GET /jobs/:id` – Job-Status abrufen
- `DELETE /jobs/:id` – Job abbrechen
- `GET /jobs` – Alle Jobs listen
- `POST /events` – Event einspeisen
- `GET /queue` – Queue-Status einsehen
- `GET /status` – Eddie-Health + Gesamtstatus (wird von `/status`-Command eingebunden)

### Autorisierung & Audit
- Nur explizit von Michael oder Slarti autorisierte Konfigurationsänderungen
- Jede Änderung wird auditiert (Log + History)
- Lydia darf keine eigenmächtigen Schedule-Änderungen vornehmen
- Lydia darf Status und Queue auslesen

### Monitoring
- Job-Status (pending, running, failed, completed, escalated)
- Laufzeiten
- Fehler mit Retry-Zähler
- Health-Endpoint

## Architekturentscheidungen (vorläufig)

| Entscheidung | Wert |
|-------------|------|
| **Container-Typ** | Docker (Pi5, aarch64) |
| **Sprache/Framework** | [noch offen – ADR] |
| **API** | HTTP REST (JSON) |
| **Persistenz** | SQLite |
| **Event-Quellen Phase 1** | Gitea + Cron |
| **Kommunikation Lydia** | HTTP REST (Eddie → Lydia + Lydia → Eddie) |
| **Synchron-Kommandos** | `/status`, `/register` etc. bleiben direkt im Processor |
| **Async/KI-Tasks** | ImageGen, Prompts etc. werden via Eddie geroutet |
| **Workflow Engine** | Phase 2 (noch nicht in Phase 1) |
| **Task-Loop-Ersatz** | `task_loop.sh` + Vekling-Dispatch wird durch Eddie ersetzt |

## Abgrenzung (Nicht in Phase 1)

- Workflow Engine (Multi-Step, Sequencing)
- Messenger-Event-Routing (bleibt direkt im Processor)
- Paperless-Fachlogik
- Business-Logik einzelner Workflows
- LLM-Integration in Eddie selbst

## Lieferweg

1. **ADR erstellen** – Architekturentscheidung dokumentieren
2. **Tests first** – Persistenz, Retry/Escalation, API, Autorisation
3. **Feature-Branch** – Implementierung
4. **Gitea Actions grün** – CI-Tests bestehen
5. **PR** – Mit Testnachweis, kein direkter Produktionspatch
6. **Deployment** – Docker-Container auf Pi5

## Migration

- Bestehende Cron-Jobs aus Lydia-Verantwortung nach Eddie überführen
- `task_loop.sh` bleibt bis Eddie produktiv ist, dann Deaktivierung
- Worker-Queues (Vekling) werden von Eddie übernommen
