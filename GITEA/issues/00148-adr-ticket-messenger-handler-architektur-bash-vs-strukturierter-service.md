---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#148
state: open
updated_at: 2026-07-14T00:35:49+02:00
is_epic: false
labels:
  - "Systemarchitektur"
  - "ready"
publication: sanitized
---

# ADR Ticket: Messenger Handler Architektur – Bash vs. strukturierter Service

Status

Backlog

Priorität

Nach Abschluss der CI/CD Foundation

Verantwortlich

Slarti – Systemarchitektur

⸻

Ziel

Bewertung der aktuellen Messenger-Handler-Architektur und Entscheidung über die zukünftige technische Basis.

Aktuell besteht der Messenger-Stack hauptsächlich aus Bash-Skripten, die Telegram, Signal-cli, JSON-Verarbeitung und Message-Handling verbinden.

Ziel ist zu entscheiden, ob:

1. Bash als Basis langfristig ausreichend ist

oder

2. eine schrittweise Migration kritischer Logik in eine besser geeignete Sprache (z. B. Python) sinnvoll ist.

⸻

Aktueller Kontext

System:

Telegram Bot API
        |
        |
Signal-cli TCP/JSON-RPC
        |
        v
Messenger Handler Container
        |
        v
JSON Message Queue
        |
        v
Lydia Agent
        |
        v
Outgoing Handler

Aktuelle Eigenschaften:

* Alpine Container
* Bash-basierter Handler
* JSON-Dateiaustausch
* Polling-basierte Verarbeitung
* Signal-cli Integration
* Telegram Integration
* umfangreiche Testsuite (~170 Tests)
* lokale Agentenarchitektur

⸻

Problemstellung

Der aktuelle Bash-Ansatz funktioniert, aber die Komplexität steigt.

Zu bewerten:

* Wartbarkeit
* Fehlerbehandlung
* Erweiterbarkeit
* Testbarkeit
* Agentenfreundlichkeit
* Performance
* Betriebssicherheit

Besondere Aufmerksamkeit:

Der Messenger ist eine zentrale Schnittstelle zwischen externen Diensten und Lydia.

Fehler dort wirken sich auf das gesamte Agentensystem aus.

⸻

Analyseauftrag

Vor einer Entscheidung analysieren:

1. Aktueller Zustand

Dokumentieren:

* vorhandene Skripte
* Datenflüsse
* Abhängigkeiten
* Fehlerbehandlung
* Testabdeckung
* bekannte Probleme

⸻

2. Bash-Bewertung

Bewerten:

Vorteile:

* geringe Abhängigkeiten
* einfache Containerisierung
* gute Integration mit Linux-Werkzeugen

Nachteile:

* komplexe JSON-Verarbeitung
* State Management
* Retry-Logik
* strukturierte Fehlerbehandlung
* Erweiterbarkeit

⸻

3. Alternative Architektur

Bewerten einer Service-orientierten Struktur:

Beispiel:

messenger/
├── adapters/
│   ├── signal.py
│   └── telegram.py
│
├── core/
│   ├── router.py
│   ├── queue.py
│   └── state.py
│
├── storage/
│   └── sqlite
│
├── tests/
│
└── main.py

Mögliche Vorteile:

* bessere Strukturierung
* bessere Tests
* saubere Zustandsverwaltung
* bessere Agenten-Wartbarkeit

⸻

Anforderungen an die Entscheidung

Die Entscheidung muss berücksichtigen:

Lydia

Die Architektur muss wartbar bleiben durch einen eingeschränkten Execution-Agenten.

Priorität:

Verständlichkeit > maximale Eleganz

⸻

Betriebssicherheit

Kein Big-Bang-Rewrite.

Falls Migration sinnvoll:

* schrittweise
* rückrollbar
* parallel betreibbar

⸻

Ressourcen

Berücksichtigen:

* Raspberry Pi 5
* Alpine Container
* geringe Ressourcen
* lokale Infrastruktur

⸻

Erwartetes Ergebnis

Erstelle ein ADR:

ADR-XXX Messenger Handler Architektur

mit:

* aktuellem Zustand
* Problemdefinition
* betrachteten Optionen
* Vor- und Nachteilen
* Entscheidung
* Begründung
* Migrationsplan (falls erforderlich)

⸻

Nicht-Ziel

Nicht Bestandteil:

* sofortiger Rewrite
* Wechsel der Messaging-Plattform
* Änderung der Lydia-Rollen
* neue Features

⸻

Definition of Done

[ ] Architektur analysiert

[ ] Entscheidung dokumentiert

[ ] Auswirkungen auf bestehende Komponenten bewertet

[ ] Migrationsstrategie definiert oder Bash-Ansatz bestätigt

[ ] Lydia-Betriebsmodell berücksichtigt

⸻

Leitprinzip

Die aktuelle Lösung muss nicht ersetzt werden, weil sie alt ist.

Sie soll nur dann verändert werden, wenn eine neue Architektur messbare Vorteile für Stabilität, Wartbarkeit oder Erweiterbarkeit bringt.
