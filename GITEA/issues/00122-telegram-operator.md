---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#122
state: closed
updated_at: 2026-07-14T00:35:49+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Mit deiner Hardware lässt sich ein leistungsfähiges System für Forschung und automatisiertes Trading aufbauen. Vier RTX 3070 (je nach VRAM-Ausbau vermutlich 8 GB) eignen sich gut für Inferenz und das Training kleiner bis mittelgroßer Modelle. Der Ryzen 5 3600 ist für Orchestrierung, Datenverarbeitung und API-Aufgaben ausreichend. Der eigentliche Engpass ist eher der Arbeitsspeicher (16 GB), insbesondere wenn viele historische Daten und mehrere Modelle parallel geladen werden. Für ein produktives System würde ich mittelfristig auf 32–64 GB RAM aufrüsten.
Ich würde die Plattform nicht als “einen Trading-Bot” bauen, sondern als modularen Entscheidungs- und Ausführungskern. Das reduziert die Kopplung der Komponenten und macht Tests, Backtests und spätere Erweiterungen deutlich einfacher.
Zielarchitektur
                           Browser
                               │
                               ▼
                   TypeScript Frontend
                               │
                          PHP REST API
                               │
 ┌─────────────────────────────┼─────────────────────────────┐
 │                             │                             │
 ▼                             ▼                             ▼
Userverwaltung            Strategien                 Portfolioverwaltung
                               │
                               ▼
                    Strategy Orchestrator
                               │
      ┌───────────────┬───────────────┬────────────────┐
      ▼               ▼               ▼                ▼
 Market Data     News Engine     KI Prediction     Risk Engine
      │               │               │                │
      └───────────────┴───────────────┴────────────────┘
                               │
                               ▼
                     Decision Engine
                               │
                               ▼
                      Broker Adapter
                               │
                               ▼
                  Interactive Brokers / Kraken / ...
Services
Ich würde die Software in einzelne Dienste aufteilen.
1. Frontend
TypeScript
Dashboard
Portfolio
Strategien
Risikoeinstellungen
Backtests
KI-Empfehlungen
Trades
Logs
Performance
Framework:
React
oder Vue

⸻

2. Backend
PHP eignet sich gut für
Auth
Benutzer
REST API
Strategieverwaltung
Konfiguration
Nicht jedoch für KI oder Backtesting.
Daher:
PHP bleibt API.
Python übernimmt:
KI
Data Science
Backtests
Broker
Scheduler

⸻

3. Datenbank
PostgreSQL.
SQLite wird schnell an Grenzen stoßen.
Beispielsweise:
users
accounts
strategies
constraints
positions
orders
signals
market_data
news
backtests
predictions
logs
Historische Kurse können sehr groß werden. Dafür würde ich entweder eine separate Datenbank oder partitionierte Tabellen verwenden.

⸻

KI-Teil
Hier würde ich die KI in mehrere spezialisierte Modelle zerlegen.
Modell 1
News Analyse
Input
Reuters
Unternehmensmeldungen
Finanznachrichten
Social Media (optional)
Output
Bullish
Bearish
Neutral

Confidence

0-100%

⸻

Modell 2
Preisvorhersage
Input
OHLCV
RSI
EMA
MACD
ATR
Volumen
Optionsdaten (optional)
Output
P(up)

P(down)

Expected return

Expected volatility
Kein “Der Kurs steigt auf 102 €”, sondern Wahrscheinlichkeitsverteilungen.

⸻

Modell 3
Portfolio Optimizer
entscheidet
welche Position

welche Größe

welches Risiko

welcher Stop Loss

Take Profit

Hebel

⸻

Modell 4
LLM
Das LLM sollte nicht selbst handeln.
Es sollte
Strategien erklären
Constraints interpretieren
Benutzer beraten
Markt zusammenfassen
Regeln in maschinenlesbare Konfigurationen übersetzen
Beispiel:
User schreibt
“Ich möchte konservativ handeln und maximal 2 % Risiko pro Trade.”
LLM erzeugt:
{
  "risk_per_trade":0.02,
  "max_open_positions":4,
  "max_drawdown":0.10,
  "allow_short":false
}
Die Handelslogik nutzt dann ausschließlich diese strukturierte Konfiguration.
Decision Engine
Das ist das Herzstück.
Sie bekommt:
Prediction

News Score

Technische Analyse

Portfolio

Constraints

Risiko

Liquidität
und entscheidet
BUY

SELL

HOLD
inklusive
