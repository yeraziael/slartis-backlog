---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#127
state: closed
updated_at: 2026-07-14T00:32:52+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Definition of Done
Alle Fehler führen zu einem sicheren Zustand.
Keine Order geht verloren.

⸻

M11 – Selbstoptimierung
Ziel
Modelle verbessern.
Arbeitspakete
Retraining
Model Registry
Versionierung
Shadow Testing
A/B Tests
Performance Reports
Tests
Neues Modell schlägt altes Modell.
Rollback funktioniert.
Definition of Done
Ein Modell wird nur aktiviert, wenn es die definierte Mindestverbesserung (z. B. hinsichtlich Sharpe Ratio und maximalem Drawdown) gegenüber dem aktuellen Modell erreicht.
Zusätzlich empfehle ich zwei Meilensteine, die in deiner bisherigen Planung fehlen
M1.5 – Architektur & Qualitätsfundament
Dieser Meilenstein zahlt sich bei einem langfristigen Projekt enorm aus.
Arbeitspakete:
API-Spezifikation (OpenAPI)
Architekturentscheidung dokumentieren (ADR)
Einheitliches Logging
Fehlercodes
Konfigurationsmanagement
Secrets-Verwaltung
Health-Checks für alle Services
Definition of Done:
Jeder Service besitzt /health und /ready Endpunkte.
Die API ist vollständig dokumentiert.
Alle Konfigurationen kommen aus Umgebungsvariablen oder Konfigurationsdateien, nicht aus dem Quellcode.

⸻

M6.5 – Experiment- und Modellmanagement
Gerade bei ML-Projekten ist Nachvollziehbarkeit entscheidend.
Arbeitspakete:
Experiment-Tracking (z. B. MLflow)
Datensatz-Versionierung
Modellversionen
Reproduzierbare Trainingsläufe
Vergleichsberichte
Definition of Done:
Jedes Modell kann eindeutig einem Datensatz, einem Trainingslauf und einer Konfiguration zugeordnet werden.
Ein Training lässt sich jederzeit mit identischen Parametern reproduzieren.
Gesamtprojekt
Am Ende sollte die Plattform folgende Eigenschaften erfüllen:
Modular: Broker, Modelle und Datenquellen sind austauschbar.
Deterministisch: Die Orderausführung ist vollständig reproduzierbar und unabhängig vom LLM.
Mandantenfähig: 3–10 Nutzer mit eigenen Portfolios, Strategien und Risikoregeln arbeiten parallel.
Reproduzierbar: Jeder Backtest, jedes Training und jede Handelsentscheidung kann später nachvollzogen werden.
Sicher: Kein Modell oder LLM kann direkt Orders platzieren; jede Order durchläuft die Risk- und Execution-Engine mit den benutzerdefinierten Constraints.
Diese Struktur entspricht dem Aufbau, den man auch bei professionellen algorithmischen Handelssystemen und ML-Plattformen verwendet, und bietet eine solide Basis für spätere Erweiterungen wie zusätzliche Broker, neue Modelltypen oder weitere Assetklassen.
