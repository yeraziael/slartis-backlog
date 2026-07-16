---
snapshot_version: gitea-epic-issue/v1
source: slarti/backlog#195
state: open
updated_at: 2026-07-14T08:48:33+02:00
labels:
  - "epic"
publication: sanitized
---

# Medizinische Kosten-, Einreichungs- und Erstattungsverwaltung

## Status (2026-07-14)

**Scope-Update:** Dieses Epic folgt dem in Kommentar #2761 definierten erweiterten Scope (Medizinische Kosten-, Einreichungs- und Erstattungsverwaltung).

**Mehrpersonenfähigkeit:** Der MVP bildet mehrere Familienmitglieder direkt ab (Entscheidung 2026-07-14).

**Absorbiert:** Issue #12 (Erstattungsstatus-Analyse) wird von diesem Epic absorbiert.

**Blocker:** Produktionsreife PDF-Pipeline (neues Issue #196)

---



Typ: Epic

Status: Blocked

Blocker:
Die PDF-Pipeline muss zuerst funktionsfähig, stabil und produktionsreif sein. Dieses Epic darf erst umgesetzt werden, wenn die PDF-Pipeline strukturierte, reproduzierbare und validierte Dokumentpakete erzeugen kann.

Ziel

Lydia soll medizinische Rechnungen, Rezepte, Verordnungen und zugehörige Nachweise aus Paperless-NGX erkennen, zusammenführen und als einreichungsfertige Pakete für folgende Empfänger vorbereiten:

* Beihilfe Bund
* Barmenia Krankenversicherung

Die tatsächliche authentifizierte Einreichung bleibt zunächst ein manueller Human-in-the-loop-Schritt.

Es wird keine inoffizielle API, keine Reverse-Engineering-Lösung und keine automatisierte Umgehung von App-, Login-, TAN- oder TOTP-Verfahren implementiert.

Ausgangslage

Für Beihilfe Bund und Barmenia existieren keine öffentlich dokumentierten APIs für die Rechnungseinreichung.

Die offiziellen Einreichungswege sind:

* Beihilfe Bund App
* BarmeniaApp
* Meine Barmenia Webportal

Beide Systeme akzeptieren vorhandene PDF-Dateien. Daher soll Lydia die gesamte Vorbereitung automatisieren und dem Operator nur noch die Prüfung und das endgültige Absenden überlassen.

Abhängigkeiten

Hard Blocker:

* PDF-Pipeline abgeschlossen
* PDF-Pipeline erzeugt valide, lesbare und normalisierte PDF-Dateien
* PDF-Pipeline unterstützt das Zusammenführen mehrerer Dokumente
* PDF-Pipeline liefert verlässliche Metadaten und Fehlerzustände
* PDF-Pipeline besitzt Tests und CI/CD-Integration
* PDF-Pipeline behandelt beschädigte, verschlüsselte oder unlesbare Dateien kontrolliert

Weitere Abhängigkeiten:

* Paperless-NGX API-Zugriff
* Lydia Task- und Decision-Engine
* Messenger-Handler für Freigaben und Statusmeldungen
* persistente Statusverwaltung
* sicherer Dateitransfer zum iPhone oder zum manuellen Uploadgerät

Nicht Bestandteil dieses Epics

* Reverse Engineering der Beihilfe- oder Barmenia-Apps
* Verwendung nicht dokumentierter interner APIs
* automatisiertes Login in Versicherungsportale
* Speicherung von Barmenia-Passwort, SMS-TAN oder TOTP-Secret
* vollautomatisches endgültiges Absenden
* automatische rechtliche oder medizinische Entscheidung über die Erstattungsfähigkeit
* automatische Änderung oder inhaltliche Manipulation von Originalrechnungen

User Story

Als Operator möchte ich, dass Lydia neue medizinische Belege automatisch erkennt, zusammengehörige Unterlagen bündelt und getrennte Einreichungspakete für Beihilfe Bund und Barmenia vorbereitet, damit ich nur noch prüfen und über den offiziellen Übermittlungsweg absenden muss.

Soll-Prozess

1. Dokumenteingang

Neue Dokumente gelangen über Paperless-NGX in das System.

Mögliche Dokumenttypen:

* Arztrechnung
* Zahnarztrechnung
* Krankenhausrechnung
* Apothekenbeleg
* Rezept
* Privatrezept
* Verordnung
* Heil- und Kostenplan
* Therapienachweis
* Zahlungsnachweis
* Mahnung
* Beihilfebescheid
* Leistungsabrechnung der Barmenia

2. Dokumentklassifikation

Lydia beziehungsweise die PDF-Pipeline bestimmt soweit möglich:

* Dokumenttyp
* Patient
* Rechnungsaussteller
* Rechnungsdatum
* Rechnungsnummer
* Bruttobetrag
* Leistungszeitraum
* zugehörige Verordnung
* zugehöriges Rezept
* zugehöriger Heil- und Kostenplan
* mögliche Vorgänger- oder Folgedokumente

Unsichere Zuordnungen dürfen nicht automatisch freigegeben werden.

3. Bündelung

Zusammengehörige Dokumente werden zu einem Submission Bundle gruppiert.

Beispiele:

* Arztrechnung plus Rezept
* Therapiekosten plus Verordnung
* Zahnarztrechnung plus Heil- und Kostenplan
* Rechnung plus Zahlungsnachweis
* Krankenhausrechnung plus ergänzende Anlagen

Ein Originaldokument darf nicht verändert werden. Zusammengeführte PDFs sind abgeleitete Arbeitskopien.

4. Zielbestimmung

Für jedes Submission Bundle wird bestimmt, für welche Empfänger es vorbereitet werden soll:

* Beihilfe Bund
* Barmenia
* beide
* keiner, da manuelle Prüfung erforderlich

Die Zielbestimmung muss konfigurierbar sein und darf nicht ausschließlich aus einem LLM-Ergebnis abgeleitet werden.

5. Validierung

Vor der Freigabe müssen mindestens folgende Prüfungen erfolgen:

* PDF technisch valide
* PDF nicht leer
* Seiten vollständig gerendert
* Text oder Bildinhalt vorhanden
* Patient bestimmt oder als unsicher markiert
* Rechnungssteller erkannt oder als unsicher markiert
* Rechnungsdatum erkannt
* Rechnungsbetrag erkannt
* Rechnungsnummer erkannt, sofern vorhanden
* keine bekannte Dublette
* nicht bereits bei demselben Empfänger eingereicht
* Dateigröße innerhalb konfigurierbarer Grenzen
* Seitenzahl innerhalb konfigurierbarer Grenzen
* keine verschlüsselte oder passwortgeschützte Datei
* Prüfsumme erzeugt

6. Einreichungspakete

Lydia erzeugt getrennte Pakete pro Empfänger.

Beispiel:

submission-bundles/
SUB-2026-00042/
source/
original-rechnung.pdf
original-rezept.pdf
beihilfe-bund/
01-rechnung.pdf
02-rezept.pdf
manifest.json
sha256sums.txt
barmenia/
01-rechnung.pdf
02-rezept.pdf
manifest.json
sha256sums.txt

Originaldateien bleiben unverändert und werden ausschließlich referenziert oder kopiert.

7. Freigabe

Lydia sendet dem Operator eine kompakte Freigabeanfrage über den Messenger.

Beispiel:

Einreichung SUB-2026-00042 vorbereitet.

Patient: Michael Maier
Rechnungssteller: Beispielpraxis
Rechnungsdatum: 10.07.2026
Betrag: 184,72 EUR
Dokumente: 2
Ziele:

* Beihilfe Bund
* Barmenia

Status: Prüfung erforderlich

Aktionen:

* freigeben
* ablehnen
* Details
* Dokumente öffnen

Die konkrete Messenger-Syntax wird durch den Messenger-Handler festgelegt.

8. Bereitstellung

Nach Freigabe werden die Pakete über einen sicheren Übergabekanal bereitgestellt.

Mögliche Zielwege:

* iCloud Drive
* lokaler WebDAV-Ordner
* Nextcloud
* zeitlich begrenzter HTTPS-Download
* SMB-Freigabe im Heimnetz
* manuell erreichbarer Exportordner

Die Transportmethode muss austauschbar implementiert werden.

9. Manuelle Einreichung

Der Operator reicht die vorbereiteten PDFs manuell ein:

Beihilfe Bund:

* App öffnen
* Antrag beginnen
* vorbereitete PDFs auswählen
* Angaben prüfen
* absenden

Barmenia:

* BarmeniaApp oder Webportal öffnen
* vorbereitete PDFs auswählen
* Angaben prüfen
* absenden

10. Statuspflege

Nach der manuellen Einreichung bestätigt der Operator die Übermittlung.

Mögliche Zustände:

* detected
* classified
* needs_review
* bundling
* validation_failed
* ready_for_approval
* approved
* exported
* submitted_manually
* acknowledged
* partially_reimbursed
* reimbursed
* rejected
* closed

Eine Übermittlung gilt nicht allein deshalb als erfolgt, weil ein Paket exportiert wurde.

11. Bescheidzuordnung

Später eingehende Dokumente sollen dem ursprünglichen Submission Bundle zugeordnet werden:

* Beihilfebescheid
* Barmenia-Leistungsabrechnung
* Rückfrage
* Ablehnung
* Nachforderung
* Erstattungsmitteilung

Die Zuordnung erfolgt anhand von:

* Patient
* Rechnungssteller
* Rechnungsnummer
* Rechnungsdatum
* Betrag
* Aktenzeichen
* Submission-ID
* zeitlicher Nähe

Unsichere Zuordnungen müssen zur manuellen Prüfung vorgelegt werden.

Datenmodell

Submission Bundle:

* submission_id
* created_at
* updated_at
* patient_id
* status
* gross_amount
* currency
* invoice_date
* provider
* invoice_number
* source_document_ids
* target_systems
* validation_result
* approval_state
* export_state
* submission_state
* reimbursement_state

Target Submission:

* target_id
* submission_id
* target_name
* status
* prepared_at
* approved_at
* exported_at
* manually_submitted_at
* acknowledgement_received_at
* expected_reimbursement
* actual_reimbursement
* notes

Document Reference:

* paperless_document_id
* document_type
* source_filename
* derived_filename
* sha256
* page_count
* mime_type
* validation_status
* relation_type

Manifest

Jedes Zielpaket erhält ein maschinenlesbares Manifest.

Beispiel:

{
“schema_version”: “1.0”,
“submission_id”: “SUB-2026-00042”,
“created_at”: “2026-07-14T00:00:00+02:00”,
“patient”: {
“id”: “patient-001”,
“display_name”: “Michael Maier”
},
“invoice”: {
“provider”: “Beispielpraxis”,
“invoice_number”: “RE-4711”,
“invoice_date”: “2026-07-10”,
“gross_amount”: 184.72,
“currency”: “EUR”
},
“target”: {
“name”: “beihilfe_bund”,
“submission_mode”: “manual”
},
“documents”: [
{
“paperless_document_id”: 1234,
“type”: “invoice”,
“filename”: “01-rechnung.pdf”,
“sha256”: “…”
},
{
“paperless_document_id”: 1235,
“type”: “prescription”,
“filename”: “02-rezept.pdf”,
“sha256”: “…”
}
],
“validation”: {
“status”: “passed”,
“warnings”: []
},
“approval”: {
“status”: “pending”
}
}

Dublettenvermeidung

Ein Dokument oder eine Rechnung darf nicht versehentlich mehrfach für denselben Empfänger eingereicht werden.

Dublettenprüfung mindestens anhand von:

* Paperless-Dokument-ID
* SHA-256-Prüfsumme
* Patient
* Rechnungssteller
* Rechnungsnummer
* Rechnungsdatum
* Rechnungsbetrag
* Zielsystem

Ein identischer Beleg darf jedoch getrennt an Beihilfe Bund und Barmenia vorbereitet werden.

Sicherheit

Gesundheitsdaten sind besonders schützenswert.

Vorgaben:

* Verarbeitung bevorzugt lokal
* keine Übertragung an externe LLM-Anbieter ohne ausdrückliche Freigabe
* keine Zugangsdaten in Git
* keine Secrets im Manifest
* keine Passwörter oder TOTP-Secrets im Lydia-Repository
* restriktive Dateiberechtigungen
* vollständiges Audit-Log
* temporäre Exportdateien nach konfigurierbarer Frist löschen
* Prüfsummen für alle exportierten Dateien
* Logs dürfen keine vollständigen medizinischen Inhalte enthalten
* Messenger-Nachrichten enthalten nur notwendige Metadaten
* Dokumentdownloads benötigen Authentifizierung oder zeitlich begrenzte Tokens

Audit-Log

Folgende Ereignisse müssen protokolliert werden:

* Dokument erkannt
* Dokument klassifiziert
* Zuordnung zu einem Bundle
* Bundle geändert
* Validierung durchgeführt
* Freigabe angefordert
* Freigabe erteilt oder verweigert
* Paket exportiert
* manuelle Einreichung bestätigt
* Bescheid zugeordnet
* Status geändert
* Erstattungsbetrag eingetragen

Jeder Eintrag enthält:

* Zeitstempel
* Submission-ID
* Aktion
* ausführende Komponente oder Benutzer
* vorheriger Status
* neuer Status
* Ergebnis
* Fehlercode, falls vorhanden

Fehlerbehandlung

Fehlerfälle müssen explizit behandelt werden:

* beschädigtes PDF
* verschlüsseltes PDF
* leeres PDF
* fehlende Seiten
* nicht erkannter Patient
* mehrere mögliche Patienten
* fehlender Rechnungsbetrag
* fehlendes Rechnungsdatum
* widersprüchliche Rechnungsnummern
* Dublettenverdacht
* Dokument bereits eingereicht
* Exportziel nicht erreichbar
* unzureichender Speicherplatz
* Messenger nicht erreichbar
* Paperless API nicht erreichbar
* Paket überschreitet konfigurierte Limits

Ein Fehler darf nicht zu einer stillen Verwerfung führen.

Technische Komponenten

Vorgesehene Module:

* Paperless Intake Adapter
* Medical Document Classifier
* Document Relationship Resolver
* Submission Bundle Service
* Validation Engine
* Duplicate Detection Service
* Manifest Generator
* PDF Package Builder
* Approval Workflow Adapter
* Export Adapter
* Submission Registry
* Reimbursement Matching Service
* Audit Logger

Die Module sollen klar voneinander getrennt und einzeln testbar sein.

Konfiguration

Konfigurierbar sein müssen mindestens:

* zulässige Dokumenttypen
* Patienten
* Zielsysteme
* Zielregeln
* maximale Seitenzahl
* maximale Dateigröße
* maximale Anzahl von Dokumenten pro Paket
* Exportpfad
* Aufbewahrungsdauer
* Messenger-Ziel
* Freigabepflicht
* Dublettenschwellen
* OCR- und Klassifikationsschwellen
* lokale oder externe Modellnutzung

MVP

Der MVP umfasst:

1. Erkennung neuer relevanter Dokumente in Paperless
2. manuelle oder regelbasierte Patientenzuordnung
3. Erkennung von Rechnungsdatum, Rechnungsnummer und Betrag
4. manuelle Auswahl zusammengehöriger Dokumente
5. Erstellung eines Bundles
6. getrennte Pakete für Beihilfe Bund und Barmenia
7. Manifest und SHA-256-Prüfsummen
8. Dublettenprüfung
9. Messenger-Freigabe
10. Export in einen festgelegten Ordner
11. manuelle Bestätigung der erfolgten Einreichung
12. persistente Statusverwaltung

Nicht erforderlich für den MVP:

* vollautomatische Dokumentbeziehungserkennung
* automatische Erstattungsberechnung
* automatische Bescheidzuordnung
* Browserautomatisierung
* App-Steuerung
* direkter Portal-Upload

Spätere Ausbaustufen

Phase 2:

* automatische Verknüpfung von Rechnung, Rezept und Verordnung
* regelbasierte Zielbestimmung
* automatische Bescheidzuordnung
* Erstattungsabgleich
* offene Differenzen und Restbeträge
* Fristen und Wiedervorlagen
* Familienmitglieder und unterschiedliche Beihilfesätze

Phase 3:

* optionaler Playwright-Assistent für das Barmenia-Webportal
* ausschließlich lokaler Browser
* Login und Zwei-Faktor-Authentifizierung durch den Operator
* automatisierte Dateiauswahl
* Stopp vor dem endgültigen Absenden

Phase 3 darf nur nach einer gesonderten Sicherheits- und Nutzungsbedingungen-Prüfung umgesetzt werden.

Akzeptanzkriterien

Das Epic ist abgeschlossen, wenn:

* die PDF-Pipeline als Blocker abgeschlossen ist
* neue relevante Paperless-Dokumente erkannt werden
* ein Submission Bundle erstellt werden kann
* mehrere zusammengehörige Dokumente gebündelt werden können
* Originaldateien unverändert bleiben
* für Beihilfe Bund und Barmenia getrennte Pakete erzeugt werden
* jedes Paket ein valides Manifest enthält
* jedes Dokument eine SHA-256-Prüfsumme besitzt
* bereits eingereichte Belege zuverlässig erkannt oder gewarnt werden
* unsichere Klassifikationen eine manuelle Prüfung erzwingen
* eine Freigabe über den Messenger angefordert werden kann
* ohne Freigabe kein Export erfolgt
* freigegebene Pakete sicher bereitgestellt werden
* die manuelle Einreichung als eigener Status bestätigt werden kann
* alle Statusänderungen persistent gespeichert werden
* alle relevanten Aktionen im Audit-Log erscheinen
* Fehler nicht stillschweigend ignoriert werden
* keine Versicherungszugangsdaten gespeichert werden
* keine inoffiziellen API-Endpunkte verwendet werden
* automatisierte Tests für Kernlogik und Fehlerfälle vorhanden sind
* CI/CD erfolgreich durchläuft
* Betriebs- und Wiederherstellungsdokumentation vorhanden ist

Definition of Done

* Architektur dokumentiert
* Datenmodell dokumentiert
* Threat Model erstellt
* Datenschutz- und Secret-Konzept dokumentiert
* MVP implementiert
* Unit-Tests vorhanden
* Integrationstests mit Paperless vorhanden
* Tests für beschädigte und unvollständige PDFs vorhanden
* Tests für Dubletten vorhanden
* Tests für fehlende Freigaben vorhanden
* CI/CD grün
* Beispielkonfiguration vorhanden
* Beispielmanifest vorhanden
* Runbook vorhanden
* Backup- und Restore-Verfahren dokumentiert
* Logging und Monitoring vorhanden
* keine Secrets im Repository
* keine produktiven Gesundheitsdaten in Test-Fixtures
* Operator-Abnahme erfolgreich

Vorgeschlagene Child Issues

1. Architektur und Threat Model für medizinische Einreichungspipeline erstellen
2. Submission-Bundle-Datenmodell definieren
3. Paperless Intake Adapter implementieren
4. medizinische Dokumenttypen und Metadaten definieren
5. Bundle- und Relationship-Service implementieren
6. PDF-Pipeline an Submission Bundle anbinden
7. Validation Engine implementieren
8. Dublettenprüfung implementieren
9. Manifest- und Checksum-Generator implementieren
10. Beihilfe-Bund-Package-Builder implementieren
11. Barmenia-Package-Builder implementieren
12. Approval Workflow über Messenger implementieren
13. sicheren Export Adapter implementieren
14. Submission Registry implementieren
15. Audit Logging implementieren
16. Fehler- und Retry-Konzept implementieren
17. Integrationstests mit Paperless erstellen
18. Runbook und Operator-Dokumentation erstellen
19. spätere Bescheid- und Erstattungszuordnung spezifizieren

Priorisierung

Dieses Epic wird nach Abschluss der PDF-Pipeline eingeplant.

Reihenfolge:

1. CI/CD- und Coding-Fähigkeit stabilisieren
2. PDF-Pipeline abschließen
3. dieses Epic entblocken
4. MVP der Einreichungsvorbereitung implementieren
5. Bescheid- und Erstattungsabgleich als Folgeausbau

Hinweis an Slarti

Dieses Epic ist ausdrücklich keine Aufgabe zur Entwicklung eines Bots, der Versicherungsportale unbeaufsichtigt bedient.

Das Ziel ist eine belastbare lokale Dokumenten-, Freigabe- und Nachverfolgungspipeline mit manueller finaler Einreichung.

Architekturentscheidungen sind so zu treffen, dass später weitere Kostenträger oder Versicherungen als zusätzliche Target Adapter ergänzt werden können.
