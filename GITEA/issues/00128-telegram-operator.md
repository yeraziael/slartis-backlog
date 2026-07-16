---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#128
state: closed
updated_at: 2026-07-14T00:35:49+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Ja – ich würde den Adminbereich sogar als eigenen Meilenstein (M1A) zwischen M1 und M2 einplanen. Für ein Mehrbenutzersystem ist das deutlich sauberer, als die Administration später “anzuflicken”.
M1A – Administration & Mandantenverwaltung
Ziel
Ein Administrator kann das gesamte System verwalten, ohne Datenbankzugriffe oder Shell-Zugriff zu benötigen.

⸻

Module
Benutzerverwaltung
Benutzer anlegen
Benutzer sperren/entsperren
Benutzer löschen (soft delete)
Passwort zurücksetzen
Rollen ändern
API-Keys verwalten
2FA aktivieren/deaktivieren
Login-Historie

⸻

Portfolioverwaltung
Admin sieht
alle Portfolios
Kontostände
offene Positionen
Performance
Drawdown
letzte Trades
Optional:
Portfolio einfrieren

⸻

Strategieverwaltung
Admin kann
Strategien aktivieren/deaktivieren
Strategien klonen
Standardstrategien bereitstellen
Versionen verwalten
Strategie sperren

⸻

Brokerverwaltung
API-Keys verschlüsselt speichern
Brokerstatus
Verbindung testen
Paper/Live umschalten
Berechtigungen verwalten

⸻

Modellverwaltung
Der Admin sieht:
Modellname

Version

Trainiert am

Datensatz

Genauigkeit

Sharpe

Status

Aktiv/Inaktiv
Außerdem:
Modell aktivieren
Rollback
Modell löschen
Training starten
Training stoppen

⸻

Scheduler
Admin kann Jobs
starten
stoppen
pausieren
neu planen
z. B.
News Import

Historische Daten

Retraining

Backtests

Backup

⸻

Monitoring
Dashboard
CPU
RAM
GPU
Festplatte
Queue
API
Broker
LLM
ML Services
Redis
PostgreSQL
Container

⸻

Audit
Alle Aktionen werden gespeichert
Admin X

↓

Benutzer Y

↓

Strategie geändert

↓

Zeitpunkt

↓

IP

↓

alte Werte

↓

neue Werte

⸻

Logs
Filterbar nach
Benutzer
Service
Fehler
Zeitraum

⸻

Benachrichtigungen
Admin erhält Meldungen bei
Broker offline
Retraining fehlgeschlagen
GPU voll
Datenimport fehlgeschlagen
Daily Loss überschritten
Kill Switch ausgelöst

⸻

Rollenmodell
Ich würde ein feingranulares RBAC (Role-Based Access Control) statt nur “Admin” und “User” verwenden.
Rolle
Rechte
Super Admin
Vollzugriff inkl. Systemeinstellungen
Administrator
Benutzer, Strategien, Modelle, Broker
Analyst
Backtests, Reports, Daten, keine Live-Trades
Trader
Eigene Strategien und Portfolios
Read Only
Nur Ansicht
API User
Nur API-Zugriff
Später kannst du zusätzlich Berechtigungen pro Aktion vergeben, z. B. strategy.edit, model.deploy oder user.disable.

⸻

Admin Dashboard
Ich würde eine Startseite mit Kennzahlen bauen:
────────────────────────────────────

Benutzer

Online: 4
Registriert: 8

────────────────────────────────────

Broker

IB ✓
Kraken ✓
Paper ✓

────────────────────────────────────

KI

Prediction Service ✓
LLM ✓
News Service ✓

────────────────────────────────────

Hardware

CPU 18 %

RAM 32 %

GPU0 67 %

GPU1 54 %

GPU2 Idle

GPU3 Training

────────────────────────────────────

Trading

Open Orders 12

Open Positions 31

Today's P/L +1,84 %

────────────────────────────────────

Alerts

1 Broker Warnung

0 API Fehler

2 Retraining Jobs

────────────────────────────────────
Definition of Done
Der Admin kann ohne Terminal oder Datenbankzugriff:
Benutzer und Rollen verwalten
Portfolios einsehen und bei Bedarf sperren
Strategien verwalten und versionieren
Modelle aktivieren oder auf eine frühere Version zurücksetzen
Brokerverbindungen testen
Hintergrundjobs steuern
Systemzustand (CPU, RAM, GPU, Services) überwachen
Audit-Logs und Fehlerprotokolle durchsuchen

⸻

Für dein Projekt würde ich außerdem eine Mandantenfähigkeit von Anfang an berücksichtigen. Auch wenn du zunächst nur 3–10 Nutzer planst, sollte jede Tabelle (Strategien, Portfolios, API-Keys, Backtests usw.) sauber einem Benutzer oder Tenant zugeordnet sein. Das vermeidet spätere Migrationen und macht die Plattform deutlich einfacher erweiterbar.
