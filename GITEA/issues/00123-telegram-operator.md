---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#123
state: closed
updated_at: 2026-07-14T00:32:51+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

confidence

position size

stop

take profit

⸻

User Constraints
Jeder Benutzer bekommt seine eigene Konfiguration.
Beispielsweise
risk:
  max_loss_day: 2%

  max_loss_trade:1%

portfolio:
  max_positions:10

  leverage:2

strategy:
  ai_weight:70%

  technical_weight:30%

stoploss:
  trailing:true

  atr_multiplier:2.3

trading:

  avoid_earnings:true

  avoid_fridays:false

⸻

Lernsystem
Ich würde keine “ständig lernende KI” im Livebetrieb verwenden.
Stattdessen:
Marktdaten

↓

Feature Store

↓

Training

↓

Evaluation

↓

Backtesting

↓

Paper Trading

↓

Live Trading
Nur wenn ein neues Modell nachweislich besser ist (z. B. anhand definierter Kennzahlen wie Sharpe Ratio oder Drawdown), wird es freigegeben. So vermeidest du unkontrollierte Modelländerungen während des Live-Handels.

⸻

Scheduler
Ein Scheduler steuert
08:00

News sammeln

↓

09:00

Vorhersagen

↓

09:10

Signale

↓

09:15

Trades

↓

jede Minute

Überwachung

⸻

GPU Nutzung
Mit vier RTX3070 könntest du beispielsweise
GPU0
LLM
GPU1
Preisvorhersage
GPU2
News
GPU3
Training / Backtesting
laufen lassen.

⸻

Modelle
Für ein lokales Setup wären beispielsweise sinnvoll:
Aufgabe
Modellklasse
Beratung
7–14B Instruction-LLM
News-Sentiment
FinBERT oder moderner Finanz-Encoder
Zeitreihen
Temporal Fusion Transformer (TFT), TiDE oder PatchTST
Ensemble
XGBoost, LightGBM oder CatBoost für tabellarische Features
Volatilität
GARCH als Baseline, später neuronale Modelle
Ich würde nicht auf ein einzelnes großes Modell setzen. Ein Ensemble aus spezialisierten Modellen liefert in der Praxis oft robustere Ergebnisse.
Erweiterungen
Später kannst du ergänzen:
Multi-Agent-System (News-Agent, Macro-Agent, Portfolio-Agent)
Reinforcement Learning zunächst nur im Simulator
Optionsanalyse
Korrelationen zwischen Märkten
Regime-Erkennung (Trend-, Seitwärts- oder Krisenmarkt)
Ereigniskalender (Quartalszahlen, Zinsentscheide)
Monte-Carlo-Simulationen für das Risikomanagement
Meine Gesamt-Empfehlung
Ich würde das Projekt in drei klar getrennte Ebenen aufteilen:
Steuerungsebene (PHP + TypeScript + PostgreSQL): Benutzer, Authentifizierung, Portfolios, Strategien, Konfiguration und Monitoring.
Analyseebene (Python): Datenbeschaffung, Feature Engineering, News-Auswertung, ML-Modelle, Backtests und Paper Trading. Diese Ebene erzeugt Wahrscheinlichkeiten und Signale, aber führt keine Trades aus.
Ausführungsebene (Python): Ein deterministischer Risk- und Execution-Engine, die ausschließlich auf Basis der Modellausgaben und der benutzerdefinierten Constraints Orders platziert. Das LLM hat dabei keinen direkten Zugriff auf die Broker-API.
Diese Trennung sorgt dafür, dass generative KI beratend und interpretierend eingesetzt wird, während die eigentliche Handelsausführung reproduzierbar, testbar und sicher bleibt. Gerade wenn mehrere Nutzer mit unterschiedlichen Strategien und Portfolios auf derselben Plattform arbeiten, ist diese Architektur deutlich wartbarer und robuster.
