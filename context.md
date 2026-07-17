# Gitea Backlog Context

## Quelle

Slartis operatives Backlog liegt in Gitea im Repository `slarti/backlog`.
Die stabilen, hostunabhaengigen Pfade sind:

- Repository: `slarti/backlog`
- Issues API: `/api/v1/repos/slarti/backlog/issues`
- Einzelnes Issue: `/api/v1/repos/slarti/backlog/issues/<number>`
- Kommentare: `/api/v1/repos/slarti/backlog/issues/<number>/comments`
- Labels: `/api/v1/repos/slarti/backlog/labels`
- Pull Requests werden in den jeweiligen Implementierungs-Repositories gefuehrt,
  nicht im Backlog-Repository.

`GITEA/issues.json` indexiert den oeffentlich bereinigten Snapshot
aller offenen und geschlossenen Backlog-Issues. Die einzelnen Inhalte liegen unter
`GITEA/issues/<number>-<slug>.md`. Interne URLs, Transport-Absender,
Attachments, lokale Pfade und Zugangsdaten sind nicht Teil dieses Snapshots.
Das Feld `is_epic` kennzeichnet die zusaetzlich als Epic erkannten Records.
`GITEA/summary.md` fasst den aktuellen Liefer- und Abhaengigkeitsstand zusammen.

## Issue-Typen

Slarti verwendet mindestens folgende fachliche Typen:

- `epic`: Architekturrahmen und Gesamtziel mit mehreren Subtasks
- `sub-task`: abgegrenztes Arbeitspaket eines Epics
- eigenstaendiges Issue: kleiner Auftrag ohne Epic-Hierarchie
- Operator-Task: Laufzeitaktion wie Deployment, DNS, Firewall, Rotation oder
  Abnahme; getrennt von Code- und Konfigurationsarbeit

Epic-Discovery darf nicht nur dem Label `epic` vertrauen. Ein expliziter
`Epic:`-Marker in Titel oder am Anfang des Bodys gilt ebenfalls als
Klassifikation. Dadurch bleiben weitergeleitete oder noch nicht gelabelte
Epics auffindbar.

## Konvention Fuer Epic-Issues

Ein Epic beschreibt:

1. Ziel und fachlichen Umfang
2. Architekturgrenzen und nicht verhandelbare Regeln
3. Abhaengigkeiten und bekannte Blocker
4. Milestones oder Subtasks
5. messbare Definition of Done
6. notwendige Operatoraktionen als getrennte Schritte

Subtasks werden im Epic ueber ihre Gitea-Issue-Nummern referenziert. Vor dem
Schliessen eines Epics werden alle referenzierten Subtasks und die reale
Operatorabnahme geprueft.

## Konvention Fuer Ausfuehrbare Issues

Ein agentenfaehiges Implementierungs-Issue folgt diesem Muster:

```text
Parent: #<epic>
Depends on: #<issue>, ...

Repo: <owner/repository>
Branch: <type/name>
Create/modify: <erlaubte Pfade>
Implement: <eindeutiger Vertrag>
Tests first: <exakte Testdatei und erwartete Faelle>
Do not: <Scope- und Sicherheitsgrenzen>
Done: <messbarer Abschluss>
```

Der Ausfuehrungsvertrag ergaenzt:

- absoluten Worktree und exakten Branch
- Abhaengigkeits-Gate vor dem Editieren
- erlaubte und verbotene Dateien
- fokussierten Testbefehl mit Arbeitsverzeichnis
- vollstaendige Repository-Suite und `git diff --check`
- CI-Registrierung fuer jeden neuen Fachtest
- Delivery-Grenze: Branch, Commit, Push und zugewiesener PR; kein Merge oder
  Deployment ohne eigene Freigabe
- Retry-Regel mit Logbefund, Ursache und begrenztem Loesungsscope

Fehlende Interfaces oder ungemergte Voraussetzungen werden nicht erraten.
Sie werden als eigener Vorgaenger geplant. Code-/Konfigurationsvorbereitung und
Operatorlaufzeit bleiben getrennte Issues.

## Herkunft Und Synchronisation

Bei einer spaeteren Synchronisation bleibt die Gitea-Issue-Nummer die stabile
operative Identitaet. GitHub-Artefakte muessen Repository, Pfad und Commit-SHA
als Herkunft tragen; Gitea-Issues verweisen entsprechend auf diese Herkunft.
Die konkrete Aktualisierungs- und Konfliktlogik wird ausserhalb dieses
Snapshots implementiert.

Dieser Stand enthaelt absichtlich keine Synchronisationsskripte und nimmt keine
Gitea-Aenderung vor. Der Snapshot wurde zuletzt am 2026-07-17 aktualisiert.
