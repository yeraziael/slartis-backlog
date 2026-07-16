---
snapshot_version: gitea-epic-issue/v1
source: slarti/backlog#212
state: open
updated_at: 2026-07-16T22:14:59+02:00
labels:
  - "Systemarchitektur"
  - "clarifying"
  - "epic"
  - "project:homelab-agenten-ausbau"
publication: sanitized
---

# Matrix als primärer Kommunikationskanal für Lydia und interne Homelab-Agenten

EPIC: Matrix als primärer Kommunikationskanal für Lydia und interne Homelab-Agenten

Typ:
Epic

Priorität:
Hoch, jedoch nach Fertigstellung und Stabilisierung der bestehenden CI/CD-Pipeline

Verantwortlich:
Slarti

Zielsystem:
Raspberry Pi 5, 8 GB RAM, Docker

Betroffene Komponenten:

* Lydia
* Messenger-Handler
* Veklinge
* Slarti-Integration
* Telegram-Gateway
* Signal-Gateway
* Reverse Proxy
* Monitoring
* Backup
* CI/CD

Ausgangslage

Lydia wird derzeit über einen eigenen Messenger-Handler mit Telegram und Signal verbunden.

Aktueller Kommunikationsweg:

Telegram / Signal
-> Messenger-Container
-> JSON-Dateien auf Shared Volume
-> Lydia Host Processor
-> ausgehende JSON-Dateien
-> Messenger-Container
-> Telegram / Signal

Die bestehende Lösung verursacht unter anderem folgende Probleme:

* Signal-cli ist vergleichsweise wartungsintensiv.
* Signal-JSON-RPC verhält sich bei Attachments und Voice Memos problematisch.
* Telegram und Signal besitzen unterschiedliche Nachrichtenlimits.
* Chunking, Fehlerbehandlung und Zustandsverwaltung müssen individuell implementiert werden.
* Interne Agentenkommunikation ist an externe Messenger gekoppelt.
* Nachrichten, Aufgabenstatus und Agentenantworten liegen nicht in einem einheitlichen Kommunikationssystem vor.
* Eine spätere Kommunikation zwischen Lydia, Slarti und Veklingen benötigt einen belastbaren internen Kanal.

Ziel

Auf dem Raspberry Pi 5 soll ein eigener Matrix-Server als primärer interner Kommunikationskanal für Lydia, Slarti und Veklinge betrieben werden.

Matrix soll zunächst nicht Telegram und Signal vollständig ersetzen.

Zielarchitektur:

Matrix
= primärer interner Kommunikationskanal

Telegram und Signal
= externe Benutzer-Gateways

Lydia soll intern ausschließlich über eine normalisierte Nachrichtenstruktur arbeiten. Matrix, Telegram und Signal werden durch Adapter an diese Struktur angebunden.

Die Umstellung muss schrittweise, rückfallfähig und ohne Unterbrechung des bestehenden Messenger-Betriebs erfolgen.

Grundsatzentscheidung

Der Matrix-Server darf nicht ungeprüft anhand einer früheren Produktempfehlung ausgewählt werden.

Slarti muss vor der Implementierung mindestens folgende Homeserver prüfen:

* Continuwuity
* Synapse
* gegebenenfalls weitere aktuell gepflegte und ARM64-kompatible Matrix-Homeserver

Die Auswahl ist anhand folgender Kriterien zu treffen:

* aktiver Wartungszustand
* ARM64-Unterstützung
* Docker-Support
* Matrix-Spezifikationsabdeckung
* Client-Kompatibilität
* Federation-Unterstützung
* Unterstützung von Application Services beziehungsweise Bots
* Datenbank- und Backup-Konzept
* Upgrade- und Migrationsfähigkeit
* RAM- und CPU-Bedarf auf dem Pi 5
* Sicherheitsmodell
* Administrierbarkeit
* Monitoring
* Wiederherstellbarkeit

Die Entscheidung ist als ADR zu dokumentieren.

Continuwuity ist bevorzugt zu prüfen, aber nicht ohne technische Verifikation fest vorgegeben.

Sollarchitektur

Internet / lokale Clients
|
v
nginx-proxy + acme-companion
|
+--> <internal-host>
|        |
|        v
|    Matrix Homeserver
|        |
|        +--> persistente Datenbank
|        +--> persistente Mediendaten
|        +--> Backup
|
+--> <internal-host>
|
v
Element Web oder geeigneter Matrix-Webclient

Lydia
|
+--> Matrix Adapter
+--> Telegram Adapter
+--> Signal Adapter
|
v
Normalisiertes internes Message Envelope
|
v
Decision Engine / Task Engine / Memory Engine

Architekturprinzipien

1. Matrix ist ein Kommunikationskanal, keine Workflow-Datenbank.

Matrix-Räume dürfen nicht zur alleinigen persistenten Speicherung des Task-Status verwendet werden.

Der autoritative Zustand von Aufgaben bleibt in den dafür vorgesehenen Systemen:

* Gitea Issues
* Lydia Task Engine
* Lydia Memory
* gegebenenfalls eine dedizierte Datenbank

Matrix transportiert:

* Befehle
* Benachrichtigungen
* Antworten
* Statusmeldungen
* Ereignisse
* Benutzerinteraktionen

2. Interne Logik darf nicht vom Messenger abhängen.

Lydia darf keine Matrix-spezifische Geschäftslogik im Decision Engine Core enthalten.

Alle Kanäle müssen auf ein gemeinsames internes Nachrichtenformat abgebildet werden.

Beispiel:

{
"message_id": "...",
"source": "matrix",
"source_instance": "homelab",
"room_id": "...",
"sender_id": "...",
"sender_display_name": "...",
"received_at": "...",
"message_type": "text",
"text": "/status",
"attachments": [],
"reply_to": null,
"metadata": {}
}

3. Kein Big-Bang-Wechsel.

Die bestehende Signal- und Telegram-Anbindung bleibt während der Migration funktionsfähig.

Matrix wird zunächst zusätzlich eingeführt.

Erst nach erfolgreicher Parallelphase darf Matrix zum primären internen Kanal erklärt werden.

4. Federation ist eine bewusste Entscheidung.

Federation darf nicht versehentlich aktiviert oder unvollständig exponiert werden.

Slarti muss eine der folgenden Varianten auswählen und dokumentieren:

* vollständig lokaler Matrix-Server ohne Federation
* private Instanz mit kontrollierter Federation
* öffentlich föderierbare Instanz

Für die erste Ausbaustufe ist ein privater beziehungsweise nicht föderierter Betrieb zu bevorzugen, sofern keine belastbare Anforderung für Federation besteht.

5. Keine offenen Registrierungen.

Öffentliche Selbstregistrierung muss standardmäßig deaktiviert sein.

Benutzerkonten werden administrativ oder über einen kontrollierten Provisionierungsprozess angelegt.

6. Secrets gehören nicht ins Repository.

Passwörter, Tokens, Signing Keys und administrative Zugangsdaten dürfen nicht in Git gespeichert werden.

Bestehende Secret-Management- und Backup-Regeln des Homelabs sind anzuwenden.

Scope

Im Scope:

* Auswahl eines geeigneten Matrix-Homeservers
* Docker-Deployment auf dem Pi 5
* Reverse-Proxy-Konfiguration
* TLS
* persistente Speicherung
* Backup und Restore
* Matrix-Webclient
* initiale Benutzer und Räume
* Lydia-Matrix-Adapter
* normalisiertes Nachrichtenformat
* Berechtigungskonzept
* Agentenräume
* Auditierbare Ereignisverarbeitung
* Rate Limiting
* Fehlerbehandlung
* Reconnect und Sync-Cursor
* Attachments
* Nachrichten-Chunking
* Monitoring
* CI/CD
* Dokumentation
* Parallelbetrieb mit Telegram und Signal
* spätere Gateway-Architektur

Nicht im ersten Scope:

* vollständige Abschaltung von Signal
* vollständige Abschaltung von Telegram
* WhatsApp-Bridge
* öffentliche Benutzerregistrierung
* unkontrollierte Federation
* Matrix als Ersatz für Gitea Issues
* Matrix als universelle Event-Queue
* E2EE für automatisierte Agentenräume, sofern dafür keine robuste Bot-Implementierung vorliegt
* produktiver Betrieb einer Vielzahl externer Bridges

Funktionale Anforderungen

FR-01: Matrix-Homeserver

Ein Matrix-Homeserver muss als Docker-Service auf dem Pi 5 betrieben werden.

Er muss:

* ARM64 unterstützen
* nach Neustart automatisch starten
* persistente Daten verwenden
* Healthchecks besitzen
* Logs über die Homelab-Standardmechanismen bereitstellen
* kontrolliert aktualisierbar sein

FR-02: Domain und TLS

Vorgesehene Domain:

<internal-host>

Optionaler Webclient:

<internal-host>

Die Dienste müssen über den bestehenden nginx-proxy und acme-companion erreichbar sein.

HTTP muss auf HTTPS umgeleitet werden.

Interne Serviceports dürfen nicht unnötig am Docker-Host veröffentlicht werden.

FR-03: Matrix-Server-Discovery

Die erforderlichen Matrix-Discovery-Endpunkte müssen korrekt bereitgestellt werden.

Zu prüfen und zu testen sind insbesondere:

* /.well-known/matrix/client
* /.well-known/matrix/server

Die endgültige Konfiguration hängt davon ab, ob Federation aktiviert wird.

FR-04: Benutzerkonten

Mindestens folgende Konten beziehungsweise Service-Identitäten sind vorzusehen:

* Operator
* Lydia
* Slarti
* Vekling-Service oder kontrolliert erzeugte Vekling-Identitäten
* optional administrativer Break-Glass-Account

Servicekonten dürfen nicht mit normalen Benutzerkonten vermischt werden.

FR-05: Räume

Mindestens folgende Räume sind anzulegen:

#lydia-control
Zweck:
Direkte Steuerung von Lydia

#lydia-status
Zweck:
Status-, Health- und Betriebsinformationen

#slarti
Zweck:
Übergaben, Planungen und Rückmeldungen von Slarti

#worker
Zweck:
Kommunikation mit Veklingen und Worker-Ereignisse

#alerts
Zweck:
Fehler, CI/CD-Fehlschläge, Ausfälle und sicherheitsrelevante Warnungen

#inbox
Zweck:
Normalisierte eingehende Nachrichten aus externen Gateways, sofern dafür ein Raum-basiertes Modell gewählt wird

Die tatsächlichen kanonischen Aliasnamen sind in der technischen Planung festzulegen.

FR-06: Berechtigungen

Power Levels und Raumrechte müssen restriktiv konfiguriert werden.

Beispiel:

* Operator: Administration
* Lydia: Nachrichten senden, Status aktualisieren, Räume verwalten, soweit erforderlich
* Slarti: Nachrichten senden und lesen, aber keine Serveradministration
* Veklinge: nur definierte Worker-Räume
* Telegram-/Signal-Gateway: nur definierte Gateway-Räume

Veklinge dürfen keine globalen Administrationsrechte erhalten.

FR-07: Lydia-Matrix-Adapter

Ein eigener Adapter muss implementiert werden, der:

* neue Matrix-Ereignisse abruft
* einen persistenten Sync-Cursor speichert
* Ereignisse dedupliziert
* Nachrichten in das interne Message Envelope überführt
* Antworten in den ursprünglichen Raum sendet
* Reply-Beziehungen unterstützt
* Fehler und Rate Limits behandelt
* Reconnects übersteht
* keine Nachricht nach einem Neustart doppelt verarbeitet
* unbekannte Eventtypen sicher ignoriert oder quarantänisiert

FR-08: Idempotenz

Jede eingehende Matrix-Nachricht darf höchstens einmal als ausführbarer Lydia-Auftrag behandelt werden.

Matrix-Event-ID und gegebenenfalls Transaction-ID sind zur Deduplizierung zu verwenden.

Die Verarbeitung muss auch nach Container- oder Host-Neustarts idempotent bleiben.

FR-09: Befehle

Mindestens folgende Befehle müssen über Matrix unterstützt werden:

/help
/status
/tasks
/task <Beschreibung>
/cancel <Task-ID>
/approve <Approval-ID>
/reject <Approval-ID>

Weitere bestehende Lydia-Befehle sind über denselben Parser bereitzustellen.

Der Command Parser darf nicht Matrix-spezifisch sein.

FR-10: Antworten und Chunking

Lange Antworten müssen kanalabhängig zerlegt werden.

Für Matrix ist ein eigenes, konfigurierbares Limit festzulegen, obwohl der Client technisch längere Nachrichten akzeptieren kann.

Chunking muss:

* Wortgrenzen berücksichtigen
* Codeblöcke möglichst erhalten
* Teile nummerieren
* Reihenfolge garantieren
* bei Teilfehlern wiederholbar sein

Beispiel:

[1/3]
[2/3]
[3/3]

FR-11: Attachments

Der Adapter muss mindestens folgende Attachment-Typen erkennen:

* PDF
* Bild
* Audio
* Textdatei

Für jedes Attachment sind zu erfassen:

* Matrix Content URI
* MIME-Type
* Dateiname
* Größe
* Prüfsumme nach Download
* Absender
* Raum
* Event-ID

Downloads müssen Größenlimits, Timeouts und MIME-Validierung besitzen.

Dateien dürfen nicht unmittelbar ungeprüft ausgeführt oder an Parser übergeben werden.

FR-12: Voice Memos

Audio-Anhänge sollen über Matrix zuverlässig empfangen und anschließend an Lydias spätere Transkriptionspipeline übergeben werden können.

Die eigentliche Speech-to-Text-Implementierung ist nicht zwingend Bestandteil dieses Epics.

Der Übergabevertrag muss jedoch definiert werden.

FR-13: Externe Gateways

Telegram und Signal bleiben vorerst eigenständige Adapter.

Die Zielstruktur lautet:

Telegram Adapter
Signal Adapter
Matrix Adapter
|
v
gemeinsames internes Message Envelope
|
v
Lydia Core

Eine Nachricht aus Telegram oder Signal darf optional als Matrix-Ereignis in einem Gateway-Raum gespiegelt werden.

Loops müssen verhindert werden.

Dafür sind Origin- und Trace-Felder vorzusehen.

Beispiel:

{
"origin_channel": "telegram",
"trace_id": "...",
"bridged_by": "lydia-gateway",
"bridge_hops": 1
}

FR-14: Agentenkommunikation

Slarti und Veklinge sollen Matrix später als standardisierten Kommunikationskanal nutzen können.

Agentenmeldungen müssen maschinenlesbar strukturiert werden können.

Beispiel:

{
"type": "worker.status",
"worker_id": "vekling-07",
"task_id": "123",
"status": "claimed",
"timestamp": "..."
}

Maschinenlesbare Payloads dürfen nicht ausschließlich als unvalidierter Freitext verarbeitet werden.

FR-15: Human-in-the-loop

Riskante Aktionen müssen weiterhin Lydias Execution Gate durchlaufen.

Matrix darf die bestehenden Freigaberegeln nicht umgehen.

Beispiel:

Lydia:
Aktion benötigt Freigabe:

* Aktion: Neustart von Dienst X
* Risiko: Dienstunterbrechung
* Approval-ID: abc123

Operator:
/approve abc123

Die Freigabe muss:

* an den ursprünglichen Benutzer gebunden sein
* ablaufen
* nur einmal nutzbar sein
* revisionssicher protokolliert werden

Nichtfunktionale Anforderungen

NFR-01: Ressourcen

Slarti muss vor Produktivsetzung Last- und Ressourcenmessungen durchführen.

Zu dokumentieren sind mindestens:

* RAM im Idle
* RAM bei aktiver Nutzung
* CPU im Idle
* CPU unter Testlast
* Datenbankwachstum
* Medienwachstum
* Startzeit
* Verhalten bei Neustart
* Verhalten bei vollem Datenträger

Der Betrieb darf die bestehenden Pi-Dienste nicht destabilisieren.

NFR-02: Sicherheit

Mindestens umzusetzen:

* keine offene Registrierung
* starke Admin-Passwörter
* separate Servicekonten
* minimale Raumrechte
* TLS
* Rate Limiting
* Login-Schutz
* restriktive Docker-Netze
* keine unnötigen Host-Port-Bindings
* Read-only-Dateisysteme, soweit praktikabel
* Drop unnötiger Linux-Capabilities
* Secret-Injection außerhalb von Git
* regelmäßige Updates
* dokumentierter Incident-Prozess

NFR-03: Datenschutz

Zu definieren sind:

* Aufbewahrungsdauer von Nachrichten
* Aufbewahrungsdauer von Medien
* Löschkonzept
* Umgang mit personenbezogenen Dokumenten
* Log-Redaktion
* Backup-Aufbewahrung
* Zugriff auf Räume

Lydia darf sensible Nachrichteninhalte nicht unkontrolliert in Debug-Logs schreiben.

NFR-04: Backup

Gesichert werden müssen:

* Homeserver-Konfiguration
* Signing Keys
* Datenbank
* Mediendaten
* Benutzer- und Raumzustand, soweit erforderlich
* Reverse-Proxy-Konfiguration
* Lydia-Adapterzustand
* Sync-Cursor
* Deduplizierungszustand

Ein Backup gilt erst als funktionsfähig, wenn ein Restore-Test erfolgreich durchgeführt wurde.

NFR-05: Monitoring

Mindestens zu überwachen:

* Containerstatus
* Health-Endpunkt
* CPU
* RAM
* Datenträgerbelegung
* Datenbankstatus
* Fehlerquote
* Matrix-Sync-Lag
* letzte erfolgreich verarbeitete Nachricht
* Anzahl fehlgeschlagener Nachrichten
* Anzahl quarantänisierter Attachments
* TLS-Zertifikatsstatus
* Backup-Alter

Kritische Fehler sollen in #alerts sowie über mindestens einen externen Fallback-Kanal gemeldet werden.

NFR-06: Wartbarkeit

Der Adapter ist nicht als monolithisches Bash-Skript zu implementieren, sofern eine robustere Sprache sinnvoll ist.

Slarti soll die Sprache anhand folgender Anforderungen auswählen:

* Matrix-SDK-Verfügbarkeit
* Async-I/O
* strukturierte Typen
* Testbarkeit
* robuste HTTP-Verarbeitung
* JSON-Schema-Validierung
* Logging
* ARM64-Support
* geringer Ressourcenbedarf

Python, Go und Rust sind zu bewerten.

Die Entscheidung ist kurz zu dokumentieren.

Phasen

Phase 0: Bestandsaufnahme

Aufgaben:

* aktuellen Messenger-Datenfluss dokumentieren
* bestehende Telegram- und Signal-Komponenten erfassen
* aktuelle Reverse-Proxy-Struktur prüfen
* verfügbare Pi-Ressourcen messen
* Backup-Ziel bestimmen
* Domain- und DNS-Konfiguration prüfen
* bestehende Lydia-Message-Schemas inventarisieren
* Abhängigkeiten zur CI/CD-Pipeline identifizieren

Ergebnis:

* Ist-Architektur
* Risikoanalyse
* Migrationsplan
* ADR-Entwurf

Phase 1: Homeserver-Auswahl und Proof of Concept

Aufgaben:

* Continuwuity prüfen
* Synapse prüfen
* ARM64-Images verifizieren
* Wartungsstatus prüfen
* Client-Kompatibilität testen
* Ressourcenverbrauch messen
* Backupfähigkeit prüfen
* Federation-Konfiguration prüfen
* Entscheidung als ADR dokumentieren

Ergebnis:

* ausgewählter Homeserver
* reproduzierbarer PoC
* gemessene Ressourcenwerte
* begründete Entscheidung

Phase 2: Infrastruktur

Aufgaben:

* Docker-Compose-Struktur erstellen
* persistente Volumes anlegen
* Datenbank konfigurieren
* Healthchecks hinzufügen
* nginx-proxy anbinden
* TLS einrichten
* Discovery-Endpunkte konfigurieren
* Registrierung deaktivieren
* Admin- und Servicekonten anlegen
* Webclient bereitstellen
* initiale Räume und Berechtigungen konfigurieren

Ergebnis:

* Matrix-Server ist intern und über die vorgesehene Domain erreichbar
* Operator kann sich mit einem Standardclient anmelden
* Räume und Rollen sind vorhanden

Phase 3: Lydia-Matrix-Adapter

Aufgaben:

* Adapterarchitektur definieren
* gemeinsames Message Envelope spezifizieren
* Inbound Sync implementieren
* Sync-Cursor persistieren
* Deduplizierung implementieren
* Outbound Messaging implementieren
* Replies implementieren
* Chunking implementieren
* Rate-Limit-Behandlung implementieren
* Reconnect implementieren
* Attachments sicher herunterladen
* Audit Logging implementieren
* Unit- und Integrationstests erstellen

Ergebnis:

* Lydia kann Matrix-Nachrichten zuverlässig empfangen und beantworten
* Neustarts verursachen keine Doppelverarbeitung

Phase 4: Parallelbetrieb

Aufgaben:

* Matrix zusätzlich zu Telegram und Signal aktivieren
* identische Testbefehle über alle Kanäle ausführen
* Antwortverhalten vergleichen
* Loop-Schutz testen
* Nachrichtenverlust simulieren
* Netzwerkunterbrechungen simulieren
* Containerneustarts testen
* Agentenräume testen
* mindestens sieben Tage kontrollierten Parallelbetrieb durchführen

Ergebnis:

* Matrix läuft stabil neben den bestehenden Kanälen
* keine Nachrichtenverluste
* keine Bridge-Loops
* keine unkontrollierte Doppelverarbeitung

Phase 5: Primärer interner Kanal

Aufgaben:

* Matrix als primären Kanal für Lydia-interne Kommunikation definieren
* Slarti-Übergaben auf Matrix vorbereiten
* Worker-Protokoll für Veklinge definieren
* externe Messenger auf Gateway-Rolle reduzieren
* Betriebsdokumentation aktualisieren
* Fallback-Verfahren dokumentieren

Ergebnis:

* interne Kommunikation erfolgt vorrangig über Matrix
* Telegram und Signal bleiben als externe Zugänge verfügbar

Phase 6: Optionale Folgearbeiten

Nicht automatisch umsetzen, sondern als separate Issues anlegen:

* kontrollierte Federation
* Application-Service-Bridge für Telegram
* Application-Service-Bridge für Signal
* E2EE-fähiger Lydia-Bot
* Push Notifications
* Single Sign-on
* automatische Raumprovisionierung
* Matrix-basierte Tutor-Räume
* Dateiübergabe an Paperless
* Voice-Note-Transkription
* mobile Client-Härtung
* Retention Policies pro Raum

Vorgeschlagene Child Issues

1. ADR: Auswahl des Matrix-Homeservers
2. Matrix PoC auf ARM64
3. Docker-Deployment für den ausgewählten Homeserver
4. Reverse Proxy und TLS für <internal-host>
5. Matrix Discovery und Federation-Modus
6. Matrix-Webclient bereitstellen
7. Benutzer-, Servicekonto- und Rollenmodell
8. Raumstruktur und Power Levels
9. Internes Lydia Message Envelope
10. Lydia Matrix Inbound Adapter
11. Lydia Matrix Outbound Adapter
12. Sync-Cursor und Event-Deduplizierung
13. Matrix Attachment Pipeline
14. Matrix Chunking und Reply Handling
15. Human-in-the-loop Approvals über Matrix
16. Telegram-, Signal- und Matrix-Adapter vereinheitlichen
17. Bridge-Loop-Prevention
18. Matrix Monitoring und Alerting
19. Matrix Backup und Restore-Test
20. Security Hardening
21. CI/CD für Matrix-Konfiguration und Lydia-Adapter
22. Parallelbetriebstest
23. Betriebs- und Notfallhandbuch
24. Migration zum primären internen Kanal
25. Follow-up: Vekling Worker Protocol über Matrix

Testanforderungen

Unit Tests:

* Event Parsing
* Command Parsing
* Message Envelope Mapping
* Deduplizierung
* Chunking
* Reply Mapping
* Attachment-Metadaten
* Approval-Prüfung
* Loop-Erkennung
* Berechtigungsprüfung

Integrationstests:

* Nachricht vom Matrix-Client an Lydia
* Antwort von Lydia an denselben Raum
* mehrere Nachrichten in kurzer Folge
* Neustart nach Empfang, aber vor Verarbeitung
* Neustart nach Verarbeitung, aber vor Bestätigung
* ungültiges Event
* nicht unterstützter Eventtyp
* zu großes Attachment
* falscher MIME-Type
* Server nicht erreichbar
* Rate Limit
* Token ungültig
* Raumzugriff entzogen
* Datenbank nicht erreichbar
* Datenträger voll

End-to-End-Tests:

1. Operator sendet /status.
2. Lydia empfängt die Nachricht einmal.
3. Lydia verarbeitet den Befehl.
4. Lydia antwortet im richtigen Raum.
5. Antwort referenziert optional die Ausgangsnachricht.
6. Audit Log enthält Trace-ID und Event-ID.
7. Neustart erzeugt keine Wiederholung.

Weitere E2E-Szenarien:

* /task erzeugt einen nachvollziehbaren Auftrag
* Approval Flow funktioniert
* PDF wird sicher entgegengenommen
* Audio wird an die Attachment-Schnittstelle übergeben
* Telegram-Nachricht wird optional nach Matrix gespiegelt
* Matrix-Antwort wird nicht versehentlich erneut zu Matrix gebrückt
* Alert wird bei Matrix-Ausfall über einen Fallback-Kanal zugestellt

CI/CD-Anforderungen

Die Matrix-Infrastruktur und der Lydia-Adapter müssen in die bestehende CI/CD-Strategie aufgenommen werden.

Pipeline-Schritte:

* Linting
* Schema-Validierung
* Unit Tests
* Integrationstests
* Container-Build
* ARM64-Build oder Multi-Arch-Verifikation
* Container-Scan
* Secret Scan
* Compose-Validierung
* Konfigurationsprüfung
* Deployment in Testumgebung
* Smoke Test
* kontrolliertes Deployment
* Post-Deployment-Verifikation
* automatischer oder dokumentierter Rollback

Direkte Pushes auf main bleiben verboten.

Änderungen erfolgen über Pull Requests.

Erforderliche Statuschecks müssen vor dem Merge erfolgreich sein.

Branches werden nach erfolgreichem Merge gelöscht.

Bestehende Repository-Einstellungen werden mit den neuen Anforderungen konsolidiert und nicht blind überschrieben.

Definition of Done

Das Epic gilt als abgeschlossen, wenn:

* eine dokumentierte Homeserver-Auswahl vorliegt
* der Matrix-Homeserver stabil auf dem Pi 5 läuft
* TLS und Domain korrekt funktionieren
* offene Registrierung deaktiviert ist
* Benutzer, Servicekonten und Räume eingerichtet sind
* Lydia Matrix-Nachrichten empfangen kann
* Lydia zuverlässig antworten kann
* Event-Deduplizierung funktioniert
* der Sync-Cursor Neustarts übersteht
* Attachments sicher behandelt werden
* Berechtigungen getestet wurden
* Telegram und Signal weiterhin funktionieren
* keine Bridge-Loops auftreten
* ein mindestens siebentägiger Parallelbetrieb erfolgreich war
* Monitoring eingerichtet ist
* Backup automatisiert ist
* ein Restore erfolgreich getestet wurde
* CI/CD alle erforderlichen Prüfungen ausführt
* Rollback getestet oder nachvollziehbar dokumentiert ist
* Betriebsdokumentation vorhanden ist
* Notfallzugriff dokumentiert ist
* keine Secrets im Repository liegen
* Matrix als primärer interner Kommunikationskanal freigegeben wurde

Abnahmekriterien

AC-01:
Der Operator kann sich über einen Standard-Matrix-Client am eigenen Server anmelden.

AC-02:
Der Operator kann Lydia in #lydia-control mit /status ansprechen und erhält innerhalb eines definierten Zeitlimits eine Antwort.

AC-03:
Eine Nachricht wird auch nach Neustart von Lydia oder des Matrix-Adapters nicht doppelt verarbeitet.

AC-04:
Ein nicht autorisierter Benutzer kann keine administrativen Lydia-Befehle ausführen.

AC-05:
Ein PDF-Anhang wird heruntergeladen, geprüft und mit vollständigen Metadaten an die interne Attachment-Schnittstelle übergeben.

AC-06:
Ein zu großes oder unzulässiges Attachment wird abgewiesen und protokolliert.

AC-07:
Bei Ausfall des Matrix-Servers bleiben Telegram und Signal grundsätzlich verfügbar.

AC-08:
Bei Ausfall des Matrix-Servers wird eine Warnung über einen externen Fallback-Kanal erzeugt.

AC-09:
Ein vollständiger Backup-Restore stellt einen funktionsfähigen Homeserver einschließlich relevanter Schlüssel und Daten wieder her.

AC-10:
Der Ressourcenverbrauch bleibt innerhalb der vorab definierten Betriebsgrenzen des Pi 5.

AC-11:
Der bestehende Betrieb von Gitea, Paperless und den übrigen Pi-Diensten wird nicht messbar destabilisiert.

AC-12:
Matrix-Ereignisse dienen nicht als alleinige autoritative Speicherung des Task-Status.

Risiken

Risiko:
Der Pi wird durch Matrix, Datenbank und Medienablage überlastet.

Gegenmaßnahme:
PoC, Ressourcenmessung, Limits, Medien-Retention und Monitoring.

Risiko:
Federation wird versehentlich öffentlich aktiviert.

Gegenmaßnahme:
Explizite ADR-Entscheidung, Konfigurationstest und externe Prüfung.

Risiko:
Bots können E2EE-Nachrichten nicht verarbeiten.

Gegenmaßnahme:
E2EE in Agentenräumen zunächst nicht voraussetzen; spätere Erweiterung als separates Issue.

Risiko:
Bridges erzeugen Nachrichtenschleifen.

Gegenmaßnahme:
Trace-ID, Origin-Markierung, maximale Bridge-Hops und Deduplizierung.

Risiko:
Matrix wird irrtümlich als zuverlässige Task Queue verwendet.

Gegenmaßnahme:
Task-Status bleibt in Gitea beziehungsweise Lydia Task Engine.

Risiko:
Signing Keys oder Datenbank gehen verloren.

Gegenmaßnahme:
verschlüsseltes Backup und verpflichtender Restore-Test.

Risiko:
Der Homeserver wird nicht mehr aktiv gepflegt.

Gegenmaßnahme:
Wartungszustand vor Auswahl prüfen, Upgrade-Plan dokumentieren und Datenportabilität berücksichtigen.

Rollback

Der Rollback muss jederzeit bis zur endgültigen Migration möglich sein.

Rollback-Verfahren:

1. Matrix-Adapter deaktivieren.
2. Telegram und Signal als primäre Kanäle weiterbetreiben.
3. Matrix-Container stoppen, Daten jedoch nicht löschen.
4. fehlerhafte Version auf vorheriges Image zurücksetzen.
5. Datenbank beziehungsweise Konfiguration aus Backup wiederherstellen.
6. Smoke Test durchführen.
7. Ursache als Incident dokumentieren.

Der Rollback darf keine Änderung an Lydias Kernlogik erfordern.

Explizite Anweisung an Slarti

Implementiere dieses Epic nicht als unzerlegten Einzelschritt.

Erstelle zunächst:

1. eine Ist-Analyse,
2. eine ADR zur Homeserver-Auswahl,
3. die Child Issues,
4. eine Abhängigkeitsreihenfolge,
5. eine Risiko- und Rollback-Planung,
6. eine Aufwandsschätzung.

Beginne anschließend mit einem isolierten Proof of Concept.

Verändere den bestehenden Signal- und Telegram-Produktivpfad nicht, bevor:

* der Matrix-PoC erfolgreich ist,
* die neue Adaptergrenze definiert ist,
* Tests vorhanden sind,
* ein Backup- und Rollback-Verfahren existiert.

Nach jeder Implementierungsphase:

* Konfiguration prüfen,
* automatisierte Tests ausführen,
* Deployment verifizieren,
* Ressourcen messen,
* Ergebnisse dokumentieren,
* bestehende Funktionalität erneut testen.

Matrix wird erst nach erfolgreichem Parallelbetrieb und expliziter Abnahme zum primären internen Kommunikationskanal erklärt.

Planungs-Addendum 2026-07-14

Die konkrete, FLASH_FREE-ausfuehrbare Zerlegung umfasst zusaetzlich:

* #244 Matrix-Webclient (Element) bereitstellen — nach #220 und #221.
* #245 TURN fuer Matrix bereitstellen und absichern — nach #219, #220 und #236.

Ausfuehrungsreihenfolge:

1. CI- und Merge-Basis (#242, #243) abschliessen.
2. ADR und isolierten Synapse-PoC (#215, #217) abschliessen; keine Produktivdomain, Daten oder OIDC verwenden.
3. Daten-/Volume- und Synapse-Compose-Grundlage (#218, #219) erstellen.
4. Proxy, Discovery, OIDC, Element und TURN (#220 bis #222, #244, #245) als getrennte Konfigurations-PRs vorbereiten.
5. Identitaeten, Raeume, Envelope und Adapterkette (#223 bis #233) implementieren.
6. Hardening, Monitoring, Backup, Release-Profil und CI (#234 bis #237, #241) nachweisen.
7. Parallelbetrieb, Betriebsdokumentation und Freigabe (#238 bis #240) erst nach erfolgreichem Testbetrieb.

Operator-Prerequisites fuer die spaetere Produktivsetzung:

* CNAMEs fuer `<internal-host>`, `<internal-host>` und `<internal-host>`.
* TURN benoetigt ausserhalb von nginx-proxy eine explizite Firewall-Freigabe fuer die dokumentierten minimalen TCP/UDP-Listener- und Relay-Ports sowie einen TLS-Zertifikatsweg.
* DNS, Firewall, Zertifikate, Deployment und Merge bleiben Operator-Aktionen; FLASH_FREE erstellt nur getestete Konfigurations-PRs.
