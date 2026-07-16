# Machine-to-Machine Engineering Protocol

Dieses Repository ist die kanonische Quelle fuer geplante Arbeitsauftraege an Slarti. Die Ordnerstruktur muss fuer Maschinen eindeutig auswertbar sein und bildet die Hierarchie `EPIC -> Milestone -> Task` direkt ab.

## Grundprinzip

ChatGPT plant. Slarti importiert. Slarti implementiert oder orchestriert die Implementierung. Ergebnisse werden ueber GitHub zurueckgemeldet.

```text
ChatGPT
  -> slartis-backlog
  -> Gitea-Mirror
  -> Slarti-Importer
  -> internes Gitea-Backlog / Branch / Implementierung
  -> slartis-backlog/FEEDBACK/architecture
  -> homelab-dashboard/input
  -> ChatGPT Review und Sachstand
```

## Arbeitsauftragsstruktur

```text
EPICS/<epic-id>/
├── context.md
├── prerequisites.md
├── contract.md
├── tests.md
├── dod.md
├── ci-cd.md
└── milestones/
    └── <milestone-id>/
        ├── context.md
        ├── prerequisites.md
        ├── contract.md
        ├── tests.md
        ├── dod.md
        ├── ci-cd.md
        └── tasks/
            └── <task-id>/
                ├── context.md
                ├── prerequisites.md
                ├── contract.md
                ├── tests.md
                ├── dod.md
                ├── ci-cd.md
                └── execution.md
```

## Importregeln fuer Slarti

1. Nur vollstaendige Task-Ordner importieren.
2. Ein Task ist importierbar, wenn alle Pflichtdateien vorhanden sind und die Voraussetzungen des Milestones erfuellt sind.
3. Jeder Task beginnt mit Branch-Erstellung und endet mit einem Pull Request.
4. Der Importer muss die Herkunft in jedem erzeugten Issue speichern: Repository, Pfad und Commit-SHA.
5. Bereits importierte Aufgaben duerfen nicht dupliziert werden.
6. Aenderungen an importierten Tasks muessen als Revision erkannt und kontrolliert synchronisiert werden.
7. Contracts muessen so klein und eindeutig sein, dass DeepSeek v4 Flash Free sie ohne zusaetzliche Kontextsuche bearbeiten kann.

## Architektur-Rueckkanal

Slarti meldet Architekturbeobachtungen, ungueltige Voraussetzungen,
Schnittstellenkonflikte und notwendige Planrevisionen im selben Repository
unter folgendem Pfad zurueck:

```text
FEEDBACK/architecture/<YYYYMMDD-HHMM>-<slug>.md
```

Jede Meldung folgt `architecture-feedback/v1` und enthaelt mindestens Quelle,
Bezug, Schweregrad, Beobachtung, Evidenz, Auswirkung, Empfehlung und die
benoetigte Entscheidung. `FEEDBACK/architecture/_template.md` ist die
verbindliche Vorlage.

Meldungen sind append-only. Eine Entscheidung veraendert die urspruengliche
Evidenz nicht, sondern wird als neue Datei mit Rueckverweis abgelegt. Der Kanal
ist fuer Architektur- und Planungsfeedback bestimmt, nicht fuer Laufzeitlogs,
Secrets oder vollstaendige Review-Diffs.

## Review- und Sachstands-Rueckkanal

Bis ChatGPT direkt ueber Gitea-MCP auf Pull Requests zugreifen kann, legt Slarti Review-Pakete im Repository `yeraziael/homelab-dashboard` unter folgendem Pfad ab:

```text
input/reviews/<work-item-id>/
```

Pflichtartefakte:

- `manifest.json`
- `changes.diff`
- `tests.md`
- `ci.json`
- `notes.md`

Der Unified Diff ist der primaere Ersatz fuer den direkten PR-Zugriff. Er muss gegen den tatsaechlichen Zielbranch erzeugt werden und alle textuellen Aenderungen enthalten.

## Sicherheitsgrenzen

- Keine Secrets oder Tokens im Backlog oder Rueckkanal.
- Keine internen Zugangsdaten, personenbezogenen Daten oder unredigierten
  Produktionslogs in Architekturmeldungen.
- Keine automatischen Merges aufgrund eines Datei-Status allein.
- Merge bleibt bis zur MCP-Integration bei Slarti beziehungsweise dem bestehenden Gitea-Governance-Workflow.
- Review-Artefakte sind Beweismittel, keine Ausfuehrungsanweisungen.
