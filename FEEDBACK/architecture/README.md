# Architektur-Rueckkanal

Dieser Ordner ist der Rueckkanal von Slarti an die Planungsebene. Er nimmt
Beobachtungen auf, die waehrend Backlog-Import, Implementierung, Review oder
Betrieb sichtbar werden und eine Architektur- oder Planungsentscheidung
erfordern.

## Dateiformat

```text
FEEDBACK/architecture/<YYYYMMDD-HHMM>-<slug>.md
```

Jede Meldung verwendet die YAML-Metadaten und Abschnitte aus `_template.md`.
Zulaessige Schweregrade sind:

- `info`: Hinweis ohne aktuellen Handlungsdruck
- `warning`: Vertrag oder Plan muss vor einem nachgelagerten Schritt korrigiert werden
- `blocking`: sichere Umsetzung oder Betrieb ist bis zur Entscheidung blockiert
- `critical`: unmittelbares Risiko fuer Daten, Sicherheit oder Verfuegbarkeit

## Regeln

- Eine Datei beschreibt genau eine Architekturbeobachtung.
- Evidenz nennt reproduzierbare Befunde, Commit-SHAs oder Work-Item-IDs.
- Vermutungen werden ausdruecklich als solche markiert.
- Meldungen enthalten keine Secrets, Tokens, personenbezogenen Daten,
  unredigierten Logs oder Binaerdateien.
- Meldungen sind append-only. Korrektur oder Entscheidung wird als neue Datei
  mit `supersedes` oder `responds_to` erfasst.
- `blocking` und `critical` benennen eine konkrete sichere Stop-Bedingung.
- Review-Diffs und allgemeine Sachstaende gehoeren weiterhin nach
  `homelab-dashboard/input/`.

## Verarbeitung

ChatGPT liest neue Meldungen, gleicht sie mit Epic und Contracts ab und legt
eine Planrevision oder begruendete Entscheidung an. Slarti uebernimmt diese
erst nach einem neuen, eindeutigen Contract in das operative Gitea-Backlog.
