---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#124
state: closed
updated_at: 2026-07-14T00:32:51+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Für ein Projekt dieser Größenordnung würde ich mit 12–16 Wochen Entwicklungszeit für einen ersten stabilen MVP rechnen. Der Fokus sollte darauf liegen, früh eine komplette Pipeline (Daten → Signal → Paper Trade → Analyse) zu haben und erst danach komplexere KI-Funktionen hinzuzufügen.
Phase 0 – Infrastruktur (1 Woche)
Ziel: Entwicklungsumgebung und Grundarchitektur.
Meilenstein M0
Ubuntu Server einrichten
NVIDIA-Treiber + CUDA + cuDNN installieren (aktuell erkennt dein System die GPUs noch nicht)
Docker + Docker Compose
Git
CI/CD
Python 3.12
PHP 8.4
PostgreSQL
Redis
Nginx
SSL
Monitoring (Prometheus + Grafana)
Ergebnis
Server läuft
Container laufen
Datenbank läuft
GPU nutzbar

⸻

Phase 1 – Grundsystem (2 Wochen)
M1 Backend
PHP
Login
JWT
Userverwaltung
Rollen
API
Frontend
React + TypeScript
Dashboard
Login
Benutzerverwaltung
Datenbank
users
accounts
roles
strategies
constraints
portfolios

⸻

Ergebnis
Mehrere Benutzer können sich anmelden.

⸻

Phase 2 – Datenplattform (2 Wochen)
M2
Historische Daten
Aktien
ETFs
Krypto
Forex
News
RSS
Pressemitteilungen
Wirtschaftskalender
Scheduler
1 min
5 min
15 min
1 h
daily
Speicherung
market_data

news

events

fundamentals

⸻

Ergebnis
Automatische Datensammlung.

⸻

Phase 3 – Broker Layer (1 Woche)
M3
Abstraktionsschicht
Broker

↓

Interactive Brokers

Kraken

Binance

Paper Broker
Jeder Broker implementiert
buy()

sell()

cancel()

positions()

balance()

orders()

⸻

Ergebnis
Jeder Broker ist austauschbar.

⸻

Phase 4 – Paper Trading (2 Wochen)
M4
Paper Broker
Portfolio
Performance
Positionen
Stop Loss
Trailing Stop
Take Profit
Orderhistorie

⸻

Ergebnis
Komplette Simulation.

⸻

Phase 5 – Backtesting (2 Wochen)
M5
Engine
Features
Parameter
Walk Forward
Performance
KPIs
CAGR
Sharpe
Sortino
Max Drawdown
Trefferquote
Profit Factor

⸻

Ergebnis
Jede Strategie ist testbar.

⸻

Phase 6 – Feature Engineering (2 Wochen)
M6
Technische Indikatoren
EMA
SMA
RSI
MACD
ATR
ADX
OBV
VWAP
Bollinger
Market Features
Volatilität
Momentum
Trend
Liquidität
News Features
Sentiment
Entity Recognition
Earnings

⸻

Ergebnis
Feature Store.

⸻

Phase 7 – Erste KI (3 Wochen)
M7
Modelle
News
FinBERT
↓
Sentiment

⸻

Zeitreihe
TFT
oder
PatchTST
↓
Wahrscheinlichkeit

⸻

Ensemble
LightGBM
↓
Final Prediction

⸻

Output
{
  "buy_probability":0.73,
  "sell_probability":0.18,
  "confidence":0.91,
  "expected_return":1.8
}

⸻

Ergebnis
Erste Vorhersagen.

⸻

Phase 8 – Decision Engine (2 Wochen)
M8
Gewichtet
KI
News
Technische Analyse
Risiko
Benutzerregeln
liefert
BUY

SELL

WAIT
inkl.
Positionsgröße.

⸻

Ergebnis
Automatische Signale.

⸻

Phase 9 – LLM Integration (2 Wochen)
M9
Lokales Modell
Aufgaben
Strategie erklären
Markt zusammenfassen
Benutzer beraten
Parameter erzeugen
NICHT
Orders senden
Beispiel
User:
“Ich möchte defensiv handeln.”
↓
LLM
↓
{
 "risk":0.01,
 "max_positions":5,
 "allow_short":false
}

⸻

Ergebnis
LLM arbeitet als Assistent.

⸻

Phase 10 – Live Trading (2 Wochen)
M10
Paper
↓
Shadow Mode
↓
kleine Beträge
↓
vollständig
Safety
Kill Switch
Daily Loss
Max Drawdown
Emergency Stop

⸻

Ergebnis
Produktiv.

⸻

Phase 11 – Optimierung (laufend)
M11
Automatisches Retraining
Hyperparameter
GPU-Auslastung
Model Registry
A/B Tests
Monitoring
Logging

⸻

Projektstruktur
trading-ai/

backend/
    php-api/

frontend/
    react/

services/

    broker/

    market-data/

    news/

    ml/

    llm/

    strategy/

    risk/

    backtest/

    scheduler/

database/

docker/

docs/

models/

logs/

tests/

⸻

Datenfluss
Marktdaten
          │
          ▼
 Feature Engineering
          │
          ▼
 KI Modelle
          │
          ▼
 Wahrscheinlichkeit
          │
          ▼
 Decision Engine
          │
          ▼
 Risk Engine
          │
          ▼
 Broker
          │
          ▼
 Portfolio
          │
          ▼
 Feedback
          │
          ▼
 Retraining

⸻

Prioritäten
Priorität
Funktion
Status für MVP
⭐⭐⭐⭐⭐
Benutzerverwaltung
Pflicht
⭐⭐⭐⭐⭐
Historische Daten
Pflicht
⭐⭐⭐⭐⭐
Paper Trading
Pflicht
⭐⭐⭐⭐⭐
Backtesting
Pflicht
⭐⭐⭐⭐⭐
Broker-Abstraktion
Pflicht
