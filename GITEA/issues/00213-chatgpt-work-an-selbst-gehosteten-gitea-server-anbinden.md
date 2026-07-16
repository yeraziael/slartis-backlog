---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#213
state: closed
updated_at: 2026-07-14T15:37:01+02:00
is_epic: true
labels:
  - "Systemarchitektur"
  - "epic"
  - "project:homelab-agenten-ausbau"
  - "ready"
publication: sanitized
---

# ChatGPT Work an selbst gehosteten Gitea-Server anbinden

EPIC: ChatGPT Work an selbst gehosteten Gitea-Server anbinden

Status: Planned
Priorität: High
Owner: Slarti
System: Homelab
Zielplattform: Raspberry Pi 5
Abhängigkeiten:

* Gitea unter <internal-gitea-reference> erreichbar
* Frontproxy und TLS funktionsfähig
* Docker auf dem Pi 5
* ChatGPT-Plan mit Unterstützung für Custom Connectoren beziehungsweise MCP

## Kontext

ChatGPT Work soll kontrolliert auf den selbst gehosteten Gitea-Server zugreifen können.

Der native GitHub-Connector ist hierfür nicht ausreichend, da der Server auf Gitea basiert. Deshalb soll ein eigener MCP-kompatibler Connector als Vermittlungsschicht zwischen ChatGPT Work und der Gitea-REST-API bereitgestellt werden.

Ziel ist, dass ChatGPT auf freigegebene Repositories zugreifen und zunächst insbesondere Backlog-, Issue-, Pull-Request- und CI/CD-Aufgaben unterstützen kann.

Die Verbindung darf nicht über einen persönlichen Administrator-Account erfolgen. Sie muss auf einem dedizierten Service-Account, minimalen Berechtigungen und nachvollziehbaren Aktionen basieren.

## Zielbild

Architektur:

ChatGPT Work
|
| HTTPS / MCP
v
Gitea-MCP-Connector
|
| Gitea REST API
v
Gitea
<internal-gitea-reference>

Der MCP-Connector läuft als eigener Docker-Container auf dem Pi 5 und wird über den bestehenden Frontproxy unter einer eigenen HTTPS-Subdomain veröffentlicht.

Vorgeschlagener Endpunkt:

<internal-gitea-reference>

Der Connector verwendet einen dedizierten Gitea-Service-Account und einen ausschließlich serverseitig gespeicherten API-Token.

## Kernanforderungen

### 1. Technische Voranalyse

Slarti soll vor der Implementierung prüfen:

* Welche MCP-Transportart ChatGPT Work aktuell unterstützt.
* Welche Authentifizierungsverfahren für Custom Connectoren beziehungsweise Remote-MCP-Server unterstützt werden.
* Ob OAuth erforderlich ist oder ein sicherer Bearer-Token- beziehungsweise API-Key-basierter Zugriff möglich ist.
* Welche Anforderungen an TLS, öffentliche Erreichbarkeit, Redirect-URLs und Connector-Metadaten bestehen.
* Ob ein geeigneter vorhandener Gitea-MCP-Server genutzt werden kann.
* Ob dieser aktiv gepflegt, sicher und mit der eingesetzten Gitea-Version kompatibel ist.
* Ob eine Eigenimplementierung sinnvoller ist.

Es darf kein beliebiges ungeprüftes Container-Image produktiv eingesetzt werden.

### 2. Dedizierter Gitea-Service-Account

Einen separaten Gitea-Benutzer für den Connector vorsehen.

Vorgeschlagener Benutzername:

chatgpt-work

Der Account darf keine globalen Administratorrechte erhalten.

Der Zugriff soll auf die benötigte Organisation und explizit freigegebene Repositories beschränkt werden.

Primäre Organisation:

Homelab

Slarti soll dokumentieren:

* welche Repository-Rolle der Service-Account erhält,
* welche API-Berechtigungen erforderlich sind,
* welche Rechte zunächst bewusst nicht vergeben werden,
* wie der Account und sein Token widerrufen werden können.

### 3. Berechtigungsmodell

Die Fähigkeiten sind stufenweise umzusetzen.

#### Phase 1: Read-only

Zulässige Aktionen:

* Organisationen und freigegebene Repositories auflisten
* Repository-Metadaten lesen
* Branches und Tags lesen
* Dateien und Verzeichnisstrukturen lesen
* Code durchsuchen
* Commits lesen
* Issues lesen
* Issue-Kommentare lesen
* Pull Requests lesen
* Reviews lesen
* CI/CD-Status und relevante Checks lesen
* Releases lesen

Nicht zulässig:

* Dateien ändern
* Branches erstellen
* Issues erstellen
* Kommentare schreiben
* Pull Requests erstellen oder mergen
* Releases erstellen
* Einstellungen ändern
* Secrets lesen oder ändern
* Repositories löschen

#### Phase 2: Backlog- und Kollaborationszugriff

Zusätzlich zulässige Aktionen:

* Issues erstellen
* Issues aktualisieren
* Labels setzen
* Assignees setzen
* Milestones zuordnen
* Kommentare zu Issues schreiben
* Kommentare zu Pull Requests schreiben

Direkte Änderungen am Repository-Inhalt bleiben verboten.

#### Phase 3: Kontrollierte Codeänderungen

Erst nach separater Freigabe umsetzen.

Mögliche Aktionen:

* Feature-Branch erstellen
* Dateien ausschließlich auf Feature-Branches ändern
* Commits erstellen
* Pull Requests erstellen
* CI-Ergebnisse prüfen
* Pull Requests aktualisieren

Weiterhin verboten:

* direkter Push auf main
* Umgehung von Branch Protection
* selbstständiges Mergen ohne definierte Freigaberegel
* Repository-Löschung
* Änderung von Secrets
* Änderung von Benutzer- oder Organisationsrechten
* Deaktivierung von CI/CD- oder Sicherheitsprüfungen

### 4. MCP-Werkzeuge

Mindestens folgende Tools sollen für Phase 1 spezifiziert und implementiert werden:

* list_organizations
* list_repositories
* get_repository
* list_branches
* list_tags
* get_file
* list_directory
* search_code
* list_commits
* get_commit
* list_issues
* get_issue
* list_issue_comments
* list_pull_requests
* get_pull_request
* list_pull_request_reviews
* get_ci_status
* list_releases
* get_release

Für Phase 2:

* create_issue
* update_issue
* comment_issue
* set_issue_labels
* set_issue_assignees
* set_issue_milestone
* comment_pull_request

Für Phase 3 optional:

* create_branch
* create_or_update_file
* create_commit
* create_pull_request
* update_pull_request

Die Tools müssen eine konsistente, maschinenlesbare Ausgabe liefern.

Fehler der Gitea-API dürfen nicht verschluckt werden. HTTP-Status, Fehlerklasse und eine bereinigte Fehlermeldung müssen zurückgegeben werden, ohne Secrets preiszugeben.

### 5. Sicherheitsanforderungen

Der Gitea-Token darf:

* nicht im Repository liegen,
* nicht in Docker-Images eingebaut sein,
* nicht in Logs erscheinen,
* nicht in ChatGPT-Konversationen ausgegeben werden,
* nicht über MCP-Toolantworten offengelegt werden.

Bevorzugte Secret-Verwaltung:

1. Docker Secret, sofern im vorhandenen Deployment praktikabel
2. alternativ geschützte Environment-Datei außerhalb des Git-Repositories

Dateiberechtigungen müssen restriktiv gesetzt werden.

Zusätzlich erforderlich:

* TLS ausschließlich über HTTPS
* keine unverschlüsselte öffentliche MCP-Verbindung
* Authentifizierung am MCP-Endpunkt
* Rate Limiting
* Request-Timeouts
* Größenlimits für Eingaben und Antworten
* Input-Validierung
* Schutz vor Path Traversal
* Schutz vor beliebigen API-Passthrough-Aufrufen
* explizite Allowlist unterstützter Gitea-Endpunkte
* Repository-Allowlist
* Secret-Redaction im Logging
* kein Shell-Command-Execution-Tool
* keine Möglichkeit, beliebige interne URLs abzurufen

### 6. Netzwerk und Deployment

Der Connector soll als eigener Docker-Compose-Stack oder sauber abgegrenzter Bestandteil des Homelab-Stacks betrieben werden.

Anforderungen:

* eigener Container
* Restart-Policy
* Healthcheck
* strukturierte Logs
* persistente Konfiguration, soweit erforderlich
* keine privilegierte Ausführung
* read-only Root-Filesystem, soweit technisch möglich
* non-root Container-User
* Ressourcenlimits
* Anschluss an das bestehende Reverse-Proxy-Netzwerk
* keine unnötigen Host-Port-Freigaben

Vorgeschlagenes Netzwerk:

frontproxy_default

Vorgeschlagene öffentliche Adresse:

<internal-host>

Die Kommunikation vom Connector zu Gitea soll nach Möglichkeit intern über das Docker- beziehungsweise Homelab-Netz erfolgen. Die öffentliche Gitea-Adresse kann als Fallback verwendet werden.

### 7. Audit Logging

Alle schreibenden Aktionen müssen nachvollziehbar protokolliert werden.

Mindestens zu erfassen:

* Zeitstempel
* Tool-Name
* Zielorganisation
* Zielrepository
* betroffene Issue-, Pull-Request- oder Branch-Referenz
* Aktionstyp
* Ergebnis
* Gitea-Request-ID, sofern vorhanden
* aufrufende Connector-Identität, soweit verfügbar

Nicht protokollieren:

* API-Tokens
* Authorization-Header
* vollständige Secret-Werte
* unnötige Repository-Inhalte
* personenbezogene Inhalte, sofern für das Audit nicht erforderlich

Für rein lesende Aktionen genügt ein reduziertes Access-Log.

### 8. Bestätigungs- und Freigaberegeln

Read-only-Aktionen können ohne zusätzliche Bestätigung ausgeführt werden.

Schreibende Aktionen sollen nach Risiko klassifiziert werden.

Niedriges Risiko:

* Issue erstellen
* Issue kommentieren
* Label setzen
* Assignee setzen

Mittleres Risiko:

* Issue schließen
* Pull Request erstellen
* Datei auf Feature-Branch ändern
* Release-Entwurf erstellen

Hohes Risiko:

* Pull Request mergen
* Branch löschen
* Release veröffentlichen
* Branch Protection ändern
* Repository-Einstellungen ändern

Hochrisikoaktionen dürfen in der ersten Version nicht implementiert werden.

Falls sie später implementiert werden, müssen sie eine explizite Bestätigung verlangen und dürfen nicht durch eine allgemeine vorherige Zustimmung autorisiert werden.

### 9. Repository-Allowlist

Der Connector darf nicht automatisch auf alle Gitea-Repositories zugreifen.

Eine Konfiguration soll festlegen:

* erlaubte Organisationen
* erlaubte Repositories
* pro Repository zulässige Tool-Gruppen
* Read-only- oder Write-Modus
* erlaubte Zielbranches
* geschützte Branches

Beispiel:

organizations:
Homelab:
repositories:
homelab-agent-core:
mode: read-write-issues
pdf-schema-pipeline:
mode: read-only
Sekretariat:
mode: read-only

Die tatsächliche Konfiguration soll anhand des vorhandenen Repository-Bestands erstellt werden.

### 10. Tests

Mindestens folgende Testebenen sind erforderlich:

#### Unit Tests

* Gitea-API-Client
* Authentifizierung
* Fehlerbehandlung
* Pagination
* Input-Validierung
* Repository-Allowlist
* Secret-Redaction
* Rechteprüfung pro Tool

#### Integrationstests

* Verbindung zu einer Gitea-Testinstanz
* Repository auflisten
* Datei lesen
* Issue lesen
* Pull Request lesen
* CI-Status lesen
* Issue in Phase 2 erstellen
* Kommentar in Phase 2 schreiben
* unzulässigen Repository-Zugriff blockieren
* unzulässige Schreibaktion blockieren
* ungültigen Token korrekt behandeln
* Rate Limit korrekt behandeln

#### Security Tests

* Path-Traversal-Versuch
* SSRF-Versuch
* manipulierte Repository-Namen
* übergroße Payload
* Token-Leak in Fehlermeldungen
* Zugriff auf nicht erlaubte Organisationen
* Zugriff auf geschützte Endpunkte
* Injection-Versuche über Issue-Titel und Dateipfade

### 11. Monitoring

Bereitzustellen sind mindestens:

* Container-Healthcheck
* Erreichbarkeitsprüfung
* Fehlerzähler
* API-Latenz
* Anzahl erfolgreicher und fehlgeschlagener Tool-Aufrufe
* Gitea-Authentifizierungsfehler
* Rate-Limit-Ereignisse

Optional:

* Prometheus-Metriken
* Integration in das bestehende Homelab-Monitoring
* Alarmierung bei wiederholten Authentifizierungsfehlern

### 12. Dokumentation

Folgende Dokumentation muss erstellt werden:

* Architekturübersicht
* Datenfluss
* Threat Model
* Berechtigungsmatrix
* Service-Account-Einrichtung
* Token-Erstellung
* Secret-Rotation
* Deployment-Anleitung
* Reverse-Proxy-Konfiguration
* ChatGPT-Work-Connector-Einrichtung
* Repository-Allowlist
* Backup- und Restore-Hinweise
* Fehlerdiagnose
* Deinstallation
* vollständiger Widerruf aller Zugriffe

Es muss eine Runbook-Sektion enthalten sein:

* Connector deaktivieren
* Token widerrufen
* neuen Token einspielen
* Service-Account sperren
* kompromittierten Connector isolieren
* Logs prüfen
* Zugriff auf einzelne Repositories entziehen

## Nicht-Ziele

Nicht Bestandteil der ersten Version:

* vollständiger Gitea-Administrationszugriff
* Verwaltung von Benutzern
* Verwaltung von Organisationen
* Verwaltung von Secrets
* Repository-Löschung
* direkter Push auf main
* autonomes Mergen
* Änderung von Branch Protection
* Änderung globaler Gitea-Einstellungen
* beliebiger Zugriff auf interne Homelab-Dienste
* allgemeine Shell- oder SSH-Ausführung
* Ersatz für Slartis bestehenden OpenCode-Zugriff

## Umsetzungsphasen

### Phase 0: Discovery und Architekturentscheidung

* aktuelle Anforderungen von ChatGPT Work an Custom Connectoren prüfen
* MCP-Transport und Authentifizierung klären
* existierende Gitea-MCP-Projekte evaluieren
* Build-versus-Buy-Entscheidung dokumentieren
* Threat Model erstellen
* Rechte- und Tool-Matrix festlegen

Ergebnis:

Ein Architecture Decision Record mit klarer Implementierungsentscheidung.

### Phase 1: Read-only MVP

* Service-Account vorbereiten
* Read-only-Token konfigurieren
* MCP-Connector implementieren oder integrieren
* Repository-Allowlist umsetzen
* Read-only-Tools bereitstellen
* Docker-Deployment erstellen
* HTTPS-Endpunkt über Frontproxy bereitstellen
* ChatGPT Work anbinden
* Integrationstests durchführen

Ergebnis:

ChatGPT Work kann freigegebene Gitea-Repositories, Dateien, Issues, Pull Requests und CI-Zustände lesen.

### Phase 2: Issues und Kommentare

* minimale Schreibrechte vergeben
* create_issue implementieren
* update_issue implementieren
* comment_issue implementieren
* Label-, Assignee- und Milestone-Funktionen implementieren
* Audit Logging aktivieren
* Sicherheits- und Berechtigungstests erweitern

Ergebnis:

ChatGPT Work kann Slartis Backlog kontrolliert lesen, Issues erstellen und bestehende Issues kommentieren.

### Phase 3: Kontrollierte Pull-Request-Erstellung

Nur nach gesonderter Freigabe.

* Feature-Branches erstellen
* Änderungen ausschließlich auf erlaubten Branches
* Pull Requests erstellen
* CI-Zustände auswerten
* keine automatische Merge-Funktion

Ergebnis:

ChatGPT Work kann Änderungen als überprüfbare Pull Requests vorbereiten, aber nicht autonom in main integrieren.

## Definition of Done

Das Epic gilt für Phase 1 und Phase 2 als abgeschlossen, wenn:

* ein dedizierter Gitea-Service-Account existiert,
* keine persönlichen oder administrativen Tokens verwendet werden,
* der MCP-Connector auf dem Pi 5 läuft,
* der Connector per HTTPS erreichbar ist,
* die Verbindung in ChatGPT Work eingerichtet ist,
* nur freigegebene Organisationen und Repositories sichtbar sind,
* Read-only-Tools vollständig funktionieren,
* Issues erstellt und kommentiert werden können,
* direkte Repository-Änderungen weiterhin blockiert sind,
* direkte Pushes auf main technisch ausgeschlossen sind,
* Secrets weder im Repository noch in Logs vorkommen,
* Audit Logging für schreibende Aktionen aktiv ist,
* Unit-, Integrations- und Security-Tests erfolgreich sind,
* Healthcheck und Monitoring vorhanden sind,
* die Dokumentation vollständig ist,
* Token-Rotation und vollständiger Zugriffswiderruf getestet wurden,
* ein End-to-End-Test erfolgreich durchgeführt wurde.

## End-to-End-Abnahmetest

1. ChatGPT Work listet die erlaubten Homelab-Repositories auf.
2. ChatGPT Work liest ein bestehendes Slarti-Issue.
3. ChatGPT Work liest zugehörige Repository-Dateien.
4. ChatGPT Work liest den CI/CD-Status.
5. ChatGPT Work erstellt ein neues Test-Issue.
6. ChatGPT Work kommentiert das Test-Issue.
7. Ein Zugriff auf ein nicht freigegebenes Repository wird blockiert.
8. Ein Versuch, direkt auf main zu schreiben, wird blockiert.
9. Ein Versuch, Repository-Einstellungen zu verändern, wird blockiert.
10. Alle erlaubten Schreibaktionen erscheinen im Audit Log.
11. In keinem Log oder Tool-Ergebnis erscheint der Gitea-Token.
12. Nach Widerruf des Tokens schlägt jeder weitere Gitea-Zugriff kontrolliert fehl.

## Erwartetes Ergebnis

Nach Abschluss kann ChatGPT Work als kontrollierter Gitea-Client für das Homelab eingesetzt werden.

Der erste produktive Einsatzzweck ist:

* Slartis Backlog durchsuchen
* Issues strukturieren
* neue Epic- und Task-Issues anlegen
* bestehende Issues kommentieren
* Repository- und CI/CD-Status zur Bewertung von Aufgaben heranziehen

Codeänderungen, Pull-Request-Erstellung und Merge-Funktionen bleiben bis zu einer separaten Sicherheitsfreigabe deaktiviert.
