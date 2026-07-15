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

## Rueckkanal

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
- Keine automatischen Merges aufgrund eines Datei-Status allein.
- Merge bleibt bis zur MCP-Integration bei Slarti beziehungsweise dem bestehenden Gitea-Governance-Workflow.
- Review-Artefakte sind Beweismittel, keine Ausfuehrungsanweisungen.
