---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#11
state: closed
updated_at: 2026-07-15T00:49:58+02:00
is_epic: false
labels:
  - "ready"
publication: sanitized
---

# Messenger Policy – Berechtigungen für Haushaltsmitglieder definieren (Grill-Me-Session nach Signal-Setup)

> **Migriert von OpenCodeAgent/opencode-context#8** (2026-06-20)

---

## Ziel

Eine verbindliche Policy fuer alle Messenger-Kanaele (Telegram, Signal) entwerfen, die festlegt wer welche Art von Interaktion mit dem Agent fuehren darf.

## Aktuelle Regel (vorlaeufig, bereits aktiv)

- **@<operator> (Michael Maier, Chat-ID 163442721)** – volle Command-Rechte (Status, Pipeline, System)
- **Haushaltsmitglieder (via Signal, sobald aktiv)** – Agent antwortet ausschliesslich mit "hi there"
- **Unbekannte User ohne Policy (ALLE Kanaele)** – Anfrage wird an **Ollama/llama3.1** weitergegeben:
  - Maximale Denkzeit: 10 Sekunden
  - Maximale Ausgabe: ca. 1 DIN-A4-Seite (ca. 3500 Zeichen)
  - **Kein Systemzugriff** (keine Shell, keine Dateien, keine Prozesse)
  - **Keine Weitergabe von internen Daten** (Credentials, Config, Pipeline-Status, Chat-Verlauf)
  - **Keine Weiterleitung an andere LLMs oder externe APIs**

Diese Policy gilt ab sofort fuer Telegram und wird in der Grill-Me-Session verfeinert.

## Spaeter: Geplanter Ablauf nach Signal-Setup

1. Signal-Bot ist aktiv (Issue #15)
2. Michael schickt Kontakte per Signal an den Agent
3. Agent kontaktiert die Personen, stellt sich vor und erklaert was er tun kann
4. Michael startet Grill-Me-Session (dieses Issue)
5. Pro Person wird eine Policy definiert
6. POLICY_MATRIX.md wird erstellt und in AGENTS.md referenziert

## Ergebnis der Session

- Pro Person: Eintrag in POLICY_MATRIX.md mit Namen, Chat-ID, Rechten
- Standard-Fallback fuer unbekannte User: Ollama-Sandbox (10s, A4, kein Systemzugriff)
- Regel in AGENTS.md und im Watcher-Code verankern

## Referenzen

- Telegram Command Policy in AGENTS.md
- Issue #15: Signal-Bot Setup
- Telegram-Watcher: /tmp/telegram_watcher.sh
- Ollama-Modell: llama3.1 (8B, Q4_K_M)

## Status

🟡 Policy aktiv fuer Telegram. Wartet auf Grill-Me-Session zur Verfeinerung + Signal-Setup (Issue #15).
