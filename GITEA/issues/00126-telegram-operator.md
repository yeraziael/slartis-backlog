---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#126
state: closed
updated_at: 2026-07-14T00:32:51+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Ich würde das Projekt wie ein professionelles Softwareprojekt aufziehen. Jeder Meilenstein hat:
Ziel
Arbeitspakete
Deliverables
Tests
Definition of Done (DoD)
So bleibt das Projekt jederzeit in einem lauffähigen Zustand.

⸻

M0 – Infrastruktur & Projektgrundlage
Ziel: Ein reproduzierbares Entwicklungssystem.
Arbeitspakete
Repository
Git Repository
Branching-Strategie
.gitignore
Commit-Konventionen
Docker
Container für:
nginx
php-fpm
postgresql
redis
python-services
ollama/vLLM
prometheus
grafana
GPU
NVIDIA Driver
CUDA
Docker GPU Runtime
GPU-Test
Entwicklungsumgebung
VS Code Dev Container
Makefile
.env
Konfiguration
CI
Linter
PHPStan
PHPUnit
Ruff
Pytest
TypeScript Build
Deliverables
docker compose up

läuft ohne Fehler
Definition of Done
Alle Container starten
GPU wird erkannt
Datenbank erreichbar
CI erfolgreich
README beschreibt Setup in <30 Minuten

⸻

M1 – Benutzerverwaltung
Ziel
Mehrbenutzerfähiges Grundsystem.
Arbeitspakete
Backend
Registrierung
Login
JWT
Refresh Token
Passwort vergessen
Rollen
Frontend
Login
Registrierung
Dashboard
Profil
Datenbank
users

roles

sessions

audit_log
Tests
Login
Logout
Token Refresh
Passwort ändern
Rechteprüfung
Definition of Done
Ein neuer Benutzer kann:
Konto erstellen
sich anmelden
Passwort ändern
Dashboard öffnen
ohne manuelle Datenbankeingriffe.

⸻

M2 – Datenplattform
Ziel
Marktdaten automatisch sammeln.
Arbeitspakete
Historische Kurse
Daily
Hourly
Minute
News
RSS
Pressemitteilungen
Scheduler
Cron
Retry
Queue
Importer
OHLCV
Splits
Dividenden
Datenbank
symbols

prices

news

events
Tests
Import startet automatisch
Duplikate werden erkannt
Fehlende Daten werden ergänzt
Definition of Done
Ein neuer Ticker wird automatisch vollständig importiert.

⸻

M3 – Broker Layer
Ziel
Broker austauschbar machen.
Arbeitspakete
Interface
Broker
Implementierungen
Paper
Interactive Brokers
Kraken
Methoden
buy()

sell()

cancel()

positions()

balance()

orders()
Tests
Mock Broker
Integration Tests
Paper Broker
Definition of Done
Ein Strategiemodul kennt den Broker-Typ nicht.

⸻

M4 – Paper Trading
Ziel
Realistische Simulation.
Arbeitspakete
Portfolio
Cash
Positionen
Limit Orders
Market Orders
Stops
Trailing Stops
Gebühren
Slippage
Tests
100 simulierte Orders.
Saldo muss reproduzierbar sein.
Definition of Done
Paper Trading erzeugt identische Ergebnisse bei gleichem Datensatz.

⸻

M5 – Backtesting
Ziel
Strategien bewerten.
Arbeitspakete
Engine
Parameter
Walk Forward
KPIs
Export
Charts
Tests
Bekannte Strategie liefert reproduzierbare Kennzahlen.
Definition of Done
Jede Strategie kann
Backtest starten

↓

Bericht erzeugen

↓

KPIs speichern

⸻

M6 – Feature Store
Ziel
Alle ML Features zentral berechnen.
Arbeitspakete
Indikatoren
RSI
EMA
ATR
MACD
ADX
Volumen
Volatilität
News Score
Makrodaten
Feature Cache
Tests
Feature-Werte stimmen mit Referenzbibliotheken überein.
Definition of Done
Neue Features können ohne Änderungen an der KI hinzugefügt werden.

⸻

M7 – Machine Learning
Ziel
Vorhersagemodelle.
Arbeitspakete
Datensätze
Training
Evaluation
Hyperparameter
Model Registry
GPU Training
Inference
Tests
Train/Test Trennung
Walk Forward
Keine Data Leakage
Definition of Done
Modell erzeugt:
Probability Up

Probability Down

Confidence

Expected Return
innerhalb weniger hundert Millisekunden pro Vorhersage.

⸻

M8 – Decision Engine
Ziel
Signal erzeugen.
Arbeitspakete
Gewichtung
KI
Technik
News
Risiko
Portfolio
Constraints
Positionsgröße
Stop
Take Profit
Tests
100 definierte Szenarien.
Immer gleiche Entscheidung.
Definition of Done
Decision Engine ist vollständig deterministisch.

⸻

M9 – LLM
Ziel
Assistent.
Arbeitspakete
Prompt Engine
RAG
Strategie Parser
JSON Output
Chat
Historie
Tests
Ungültige Antworten werden erkannt.
JSON Validator
Definition of Done
LLM erzeugt ausschließlich gültige JSON-Konfigurationen.
Keine Freitext-Entscheidungen gelangen in die Handelslogik.

⸻

M10 – Live Trading
Ziel
Produktiver Betrieb.
Arbeitspakete
Broker
Order Queue
Retry
Monitoring
Kill Switch
Limits
Audit Log
Benachrichtigungen
Tests
Broker offline
Netzwerkfehler
Teilweise Ausführung
API Timeout
