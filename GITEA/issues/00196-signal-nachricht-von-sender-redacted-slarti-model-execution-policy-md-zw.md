---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#196
state: closed
updated_at: 2026-07-14T12:28:13+02:00
is_epic: false
labels:
  - "Systemarchitektur"
  - "project:homelab-agenten-ausbau"
  - "ready"
publication: sanitized
---

# Signal: Nachricht von sender-redacted: @slarti MODEL_EXECUTION_POLICY.md Zweck Diese

---

Nachricht von <sender-redacted>: @slarti MODEL_EXECUTION_POLICY.md

Zweck

Diese Policy steuert, welches Modell Slarti für welche Aufgaben verwenden darf.

Slarti MUSS vor Beginn jeder substanziellen Aufgabe prüfen, welches Modell aktuell aktiv ist.

Wenn das aktive Modell nicht dem laut dieser Policy vorgesehenen Modell entspricht, darf Slarti die Aufgabe nicht ohne ausdrückliche Bestätigung des Operators beginnen oder fortsetzen.

Ziele:

* Sol-Kontingent schützen
* Terra als reguläres Cloud-Arbeitsmodell verwenden
* Routinearbeiten möglichst lokal ausführen
* unbeabsichtigte Modellwechsel verhindern
* Modellnutzung transparent und nachvollziehbar machen

⸻

1. Verbindliche Modellklassen

Die konkreten Provider- und Modellnamen können je nach OpenCode-Konfiguration abweichen.

Slarti muss die verfügbaren Modelle semantisch folgenden Klassen zuordnen:

Modellklasse	Bevorzugte Verwendung
LOCAL_FAST	einfache Analyse, Dokumentation, Tickets, kleine Änderungen
LOCAL_CODER	Coding, Tests, CI/CD, Bash, Python, Docker, Refactoring
LUNA	einfache Cloud-Aufgaben, Textarbeit, Zusammenfassungen
TERRA	anspruchsvolle Planung, Architektur, Reviews, komplexere Implementierung
SOL	Eskalationsmodell für besonders schwierige oder festgefahrene Aufgaben

Aktuelle Zielzuordnung:

LOCAL_FAST:
- qwen3.5:4b
- qwen2.5:3b
- vergleichbare lokale General-Purpose-Modelle
LOCAL_CODER:
- qwen2.5-coder:7b
- vergleichbare lokale Coding-Modelle
LUNA:
- jedes von OpenAI als Luna bezeichnete Modell
TERRA:
- jedes von OpenAI als Terra bezeichnete Modell
SOL:
- jedes von OpenAI als Sol bezeichnete Modell

Aliase, Versionssuffixe und Provider-Präfixe ändern die Modellklasse nicht.

Beispiele:

openai/terra
openai/terra-latest
gpt-5.6-terra

werden der Klasse TERRA zugeordnet.

⸻

2. Pflichtprüfung vor Arbeitsbeginn

Vor jeder substanziellen Aufgabe MUSS Slarti:

1. das aktuell aktive Modell ermitteln,
2. dessen Modellklasse bestimmen,
3. die Aufgabe klassifizieren,
4. die laut Policy vorgesehene Modellklasse bestimmen,
5. aktives und vorgesehenes Modell vergleichen.

Eine substanzielle Aufgabe ist insbesondere:

* Änderung von Quellcode
* Änderung von Konfiguration
* Erstellung oder Änderung einer Architektur
* Ausführung eines längeren Analyse- oder Debugging-Prozesses
* Eröffnung oder Bearbeitung eines Pull Requests
* Änderung mehrerer Dateien
* Generierung größerer Artefakte
* irreversible oder potenziell riskante Aktion

Reine Statusabfragen und sehr kurze Antworten dürfen ohne erneute Bestätigung erfolgen, sofern keine Modellabweichung für eine daran anschließende Aufgabe entsteht.

⸻

3. Aufgabenzuordnung

3.1 LOCAL_FAST

Standard für:

* Ticketpflege
* Backlog-Bereinigung
* Zusammenfassungen
* README-Änderungen
* einfache Dokumentation
* Formatierung
* einfache Klassifikation
* kleine Recherche innerhalb des Repositories
* triviale Konfigurationsänderungen
* kleine Textänderungen
* Erstellung einfacher Checklisten

3.2 LOCAL_CODER

Standard für:

* Bash-Skripte
* Python-Hilfsskripte
* Dockerfiles
* Docker-Compose-Dateien
* CI/CD-Konfiguration
* Testfälle
* Linting
* kleine und mittlere Bugfixes
* Refactoring mit klar definiertem Ziel
* Änderungen mit überschaubarem Kontext
* Implementierungen unter ungefähr 300 geänderten Codezeilen
* Ausführung und Reparatur bestehender Tests

3.3 LUNA

Standard für:

* leichte Cloud-Aufgaben
* sprachliche Überarbeitung
* strukturierte Zusammenfassungen
* Ticketentwürfe
* einfache Planung
* Aufgaben, die lokal nicht sinnvoll laufen, aber keine tiefe Architekturarbeit benötigen

Luna ist kein Standardmodell für komplexe Implementierung oder Architektur.

3.4 TERRA

Standard für:

* neue Features mit mehreren Komponenten
* Architekturentscheidungen
* technische Konzepte
* API-Design
* komplexe Debugging-Aufgaben
* größere Refactorings
* Review sicherheitsrelevanter oder systemkritischer Änderungen
* migrationsrelevante Planung
* Analyse schwer verständlicher Legacy-Strukturen
* Erstellung präziser Implementierungspläne für Lydia oder Veklinge

Terra ist das reguläre Cloud-Arbeitsmodell für Slarti.

3.5 SOL

Sol darf nur verwendet werden für:

* Probleme, bei denen Terra nach mindestens zwei ernsthaften Lösungsversuchen nicht weiterkommt
* komplexe systemübergreifende Architekturentscheidungen
* besonders schwierige Race Conditions
* schwer reproduzierbare Fehler
* sicherheitskritische Reviews mit hoher Tragweite
* Datenverlust-, Recovery- oder Migrationsszenarien mit hohem Risiko
* fundamentale Designentscheidungen, die mehrere Projekte langfristig beeinflussen
* ausdrücklich vom Operator für Sol freigegebene Aufgaben

Sol darf nicht allein deshalb verwendet werden, weil es verfügbar oder qualitativ stärker ist.

Sol darf insbesondere nicht standardmäßig verwendet werden für:

* Dokumentation
* Ticketpflege
* README-Dateien
* normale CI/CD-Arbeiten
* einfache Bash- oder Python-Aufgaben
* Tests
* kleine Bugfixes
* Routine-Refactoring
* Zusammenfassungen
* normale Code-Reviews

⸻

4. Verhalten bei korrektem Modell

Wenn das aktive Modell der vorgesehenen Modellklasse entspricht, darf Slarti die Aufgabe normal bearbeiten.

Vor Beginn soll Slarti intern protokollieren:

MODEL_CHECK
active_model: <erkannter Modellname>
active_class: <Modellklasse>
required_class: <Modellklasse>
task_classification: <kurze Beschreibung>
status: approved_by_policy

Eine zusätzliche Rückfrage an den Operator ist in diesem Fall nicht erforderlich.

⸻

5. Verhalten bei Modellabweichung

Wenn das aktive Modell nicht der laut Policy vorgesehenen Modellklasse entspricht, MUSS Slarti die Arbeit anhalten.

Slarti darf vor der Bestätigung:

* die Aufgabe lesen,
* den Umfang grob einschätzen,
* die Abweichung erklären,
* einen empfohlenen Modellwechsel nennen.

Slarti darf vor der Bestätigung NICHT:

* Dateien ändern,
* Commits erstellen,
* Tests mit potenziellen Nebenwirkungen starten,
* Container oder Dienste verändern,
* Pull Requests erstellen,
* Schreiboperationen durchführen,
* eine umfangreiche Analyse durchführen, die bereits einen wesentlichen Teil des Modellkontingents verbraucht.

Slarti muss folgende Warnung ausgeben:

MODELLABWEICHUNG
Aktives Modell:
<Modellname> (<Modellklasse>)
Laut Policy vorgesehen:
<Modellklasse>
Aufgabenklassifikation:
<Klassifikation>
Begründung:
<kurze Begründung der Modellzuordnung>
Empfehlung:
<Modell wechseln oder aktuelle Nutzung ausdrücklich freigeben>
Ich beginne oder fahre erst fort, wenn du die Abweichung ausdrücklich bestätigst.

Eine gültige Bestätigung muss eindeutig sein.

Beispiele gültiger Bestätigungen:

Bestätigt.
Mit diesem Modell fortfahren.
Sol für diese Aufgabe freigegeben.
Terra-Abweichung akzeptiert.
Ja, trotz Policy fortfahren.

Nicht ausreichend sind unklare Antworten wie:

Okay.
Mal sehen.
Mach weiter wie sinnvoll.

Bei unklarer Antwort muss Slarti erneut eine eindeutige Bestätigung verlangen.

⸻

6. Strengere Regeln bei Sol

Wenn das aktive Modell SOL ist, obwohl die Policy ein anderes Modell vorsieht, muss die Warnung zusätzlich enthalten:

WARNUNG: Sol-Kontingent wird verwendet.
Diese Aufgabe ist laut Policy nicht als Sol-Aufgabe klassifiziert.
Die Fortsetzung kann das wöchentliche Sol-Kontingent reduzieren.

Die Bestätigung muss Sol ausdrücklich erwähnen.

Gültige Beispiele:

Sol-Nutzung für diese Aufgabe bestätigt.
Mit Sol fortfahren.
Ich bestätige den Verbrauch des Sol-Kontingents.

Ein allgemeines „Ja“ reicht für eine nicht policy-konforme Sol-Nutzung nicht aus.

⸻

7. Downgrade und Upgrade

Downgrade

Wenn ein schwächeres Modell aktiv ist als vorgesehen, muss Slarti warnen, weil Ergebnisqualität oder Zuverlässigkeit unzureichend sein können.

Beispiel:

Aktiv: LOCAL_CODER
Vorgesehen: TERRA

Slarti empfiehlt den Wechsel auf Terra.

Upgrade

Wenn ein stärkeres oder teureres Modell aktiv ist als vorgesehen, muss Slarti ebenfalls warnen, weil unnötig Kontingent verbraucht wird.

Beispiel:

Aktiv: SOL
Vorgesehen: LOCAL_CODER

Slarti empfiehlt den Wechsel auf das lokale Coding-Modell.

Abweichungen sind in beide Richtungen bestätigungspflichtig.

⸻

8. Eskalation von Terra zu Sol

Eine Eskalation von Terra zu Sol ist nur zulässig, wenn Slarti dokumentiert:

1. welche Lösungsansätze mit Terra versucht wurden,
2. warum diese nicht ausreichten,
3. welches konkrete Problem Sol lösen soll,
4. welche Dateien oder Komponenten betroffen sind,
5. welches Ergebnis von Sol erwartet wird.

Vor dem Modellwechsel muss Slarti folgende Meldung ausgeben:

SOL-ESKALATION ERFORDERLICH
Bisheriges Modell:
Terra
Fehlgeschlagene oder unzureichende Ansätze:
1. <Ansatz>
2. <Ansatz>
Verbleibendes Kernproblem:
<Problem>
Warum Sol erforderlich erscheint:
<Begründung>
Erwarteter Umfang der Sol-Nutzung:
<kurze Einschätzung>
Bitte bestätige ausdrücklich:
„Sol für diese Eskalation freigegeben.“

Ohne diese ausdrückliche Bestätigung darf nicht auf Sol eskaliert werden.

⸻

9. Modellwechsel während einer Aufgabe

Slarti muss die Modellprüfung erneut ausführen, wenn:

* das Modell manuell gewechselt wurde,
* OpenCode automatisch ein anderes Modell auswählt,
* ein Provider-Fallback erfolgt,
* eine Session neu gestartet wurde,
* die Aufgabe an einen anderen Agenten übergeben wurde,
* ein Subagent oder Worker mit einem anderen Modell gestartet wird,
* der aktuelle Modellname nicht mehr sicher feststellbar ist.

Eine einmalige Bestätigung gilt nur für:

* die konkrete Aufgabe,
* die konkrete Modellabweichung,
* die aktuelle Session oder den klar definierten Arbeitsabschnitt.

Sie ist keine dauerhafte Ausnahme von der Policy.

⸻

10. Unbekanntes oder nicht ermittelbares Modell

Wenn Slarti das aktive Modell nicht zuverlässig erkennen kann, gilt:

active_class: UNKNOWN

UNKNOWN ist niemals automatisch zulässig.

Slarti muss anhalten und melden:

MODELLSTATUS UNKLAR
Ich kann das aktuell aktive Modell nicht zuverlässig bestimmen.
Laut Policy darf ich deshalb keine substanzielle Arbeit beginnen.
Bitte:
1. prüfe das aktive Modell in OpenCode,
2. nenne oder wechsle das Modell,
3. bestätige anschließend die Fortsetzung.

Slarti darf niemals aus Stil, Antwortqualität oder vermuteter Leistungsfähigkeit ableiten, welches Modell aktiv ist.

Die Modellidentität muss aus einer technischen Quelle stammen, beispielsweise:

* OpenCode-Session-Metadaten
* Provider-Metadaten
* Modellanzeige
* Runtime-Umgebungsvariable
* Konfigurationsdatei
* API-Antwortmetadaten
* Session- oder Request-Log

⸻

11. Technische Ermittlung in OpenCode

Slarti soll die Modellidentität in folgender Priorität ermitteln:

1. explizite Modellinformation der aktuellen OpenCode-Session
2. aktuelle Provider- und Modellanzeige von OpenCode
3. Session-Metadaten oder Request-Metadaten
4. OpenCode-Konfiguration
5. Umgebungsvariablen
6. letzter eindeutig protokollierter Modellwechsel innerhalb derselben Session

Nicht zulässig:

* Raten
* Ableitung aus dem Schreibstil
* Annahme aufgrund des zuletzt vom Operator genannten Modells
* Annahme aufgrund eines früheren Chats
* Annahme, dass ein Provider-Fallback das gleiche Modell verwendet

Wenn OpenCode die Modellinformation nicht direkt für den Agenten bereitstellt, muss Slarti den Operator vor jeder substanziellen Aufgabe auf die fehlende technische Durchsetzbarkeit hinweisen.

⸻

12. Empfohlene maschinenlesbare Konfiguration

Zusätzlich zu dieser Policy soll folgende Datei gepflegt werden:

# model-policy.yaml
version: 1
default_cloud_model: TERRA
default_local_coding_model: LOCAL_CODER
default_local_general_model: LOCAL_FAST
classes:
  LOCAL_FAST:
    patterns:
      - "qwen3.5:4b"
      - "qwen2.5:3b"
  LOCAL_CODER:
    patterns:
      - "qwen2.5-coder:7b"
  LUNA:
    patterns:
      - "luna"
  TERRA:
    patterns:
      - "terra"
  SOL:
    patterns:
      - "sol"
rules:
  documentation: LOCAL_FAST
  ticket_management: LOCAL_FAST
  summarization: LOCAL_FAST
  bash: LOCAL_CODER
  python_utility: LOCAL_CODER
  docker: LOCAL_CODER
  ci_cd: LOCAL_CODER
  tests: LOCAL_CODER
  small_bugfix: LOCAL_CODER
  medium_implementation: LOCAL_CODER
  large_feature: TERRA
  architecture: TERRA
  complex_debugging: TERRA
  security_review: TERRA
  migration_planning: TERRA
  blocked_after_two_terra_attempts: SOL
  critical_recovery: SOL
confirmation:
  required_on_any_mismatch: true
  explicit_sol_confirmation: true
  unknown_model_is_blocking: true
  confirmation_scope: task

⸻

13. Protokollierung

Jede Modellabweichung und jede Bestätigung soll protokolliert werden.

Format:

MODEL_POLICY_EVENT
timestamp: <ISO-8601>
task: <Aufgabe oder Issue>
active_model: <Modellname>
active_class: <Klasse>
required_class: <Klasse>
mismatch: true|false
operator_confirmation: <Wortlaut oder none>
decision: proceed|blocked|model_changed

Das Protokoll darf keine API-Keys, Tokens oder sonstigen Secrets enthalten.

⸻

14. Sicherheitsregel

Diese Policy ist eine Ausführungs- und Kostenkontrollregel.

Sie ersetzt nicht:

* Berechtigungsprüfungen
* Secret-Handling
* Backup-Vorgaben
* Branch- und Pull-Request-Regeln
* Tests
* Definition of Done
* Operatorfreigaben für riskante Aktionen

Auch bei korrektem Modell bleiben alle anderen Policies vollständig gültig.

⸻

15. Verbindliche Kurzregel

Vor jeder substanziellen Aufgabe gilt:

DETECT MODEL
→ CLASSIFY MODEL
→ CLASSIFY TASK
→ DETERMINE REQUIRED MODEL
→ COMPARE
→ MATCH: PROCEED
→ MISMATCH: WARN AND BLOCK
→ SOL MISMATCH: REQUIRE EXPLICIT SOL CONFIRMATION
→ UNKNOWN MODEL: BLOCK

Slarti darf diese Prüfung nicht überspringen, um Zeit zu sparen oder die Aufgabe schneller zu beginnen.

---
[internal attachment omitted]
