# Slarti's Backlog

> Repository zur strukturierten Ausplanung von Entwicklungsarbeit vor der Implementierung.

## Ziel

Dieses Repository dient **nicht** als klassisches Issue-Tracking. Stattdessen werden Epics als Verzeichnisstruktur modelliert und so detailliert vorbereitet, dass Slarti daraus eigenständig Gitea-Issues und Branches erzeugen kann.

```
EPIC/
├── context.md
├── contract.md
├── prerequisites.md
├── tests.md
├── dod.md
├── ci-cd.md
└── milestones/
    └── M01/
        ├── context.md
        ├── prerequisites.md
        ├── contract.md
        ├── tests.md
        ├── dod.md
        └── tasks/
            └── T001/
                ├── context.md
                ├── contract.md
                ├── prerequisites.md
                ├── tests.md
                ├── dod.md
                └── implementation.md
```

## Engineering-Regeln

- Ein Epic definiert Architektur und Gesamtziel.
- Jeder Milestone besitzt explizite Voraussetzungen (`prerequisites.md`).
- Jede Task startet mit einem Branch und endet mit einem Pull Request.
- CI/CD-Anforderungen werden auf Epic-Ebene definiert, in Milestones konkretisiert und in Tasks vollständig ausformuliert.
- Jeder Contract muss so präzise sein, dass ein leistungsfähiger Coding-Agent ihn ohne zusätzliche Interpretation umsetzen kann.
- Kontext wird so klein wie möglich gehalten und nur dort wiederholt, wo er für die jeweilige Ebene erforderlich ist.

## Rolle dieses Repositories

Dieses Repository ist die gemeinsame Planungsgrundlage zwischen Operator, ChatGPT und Slarti. ChatGPT plant und strukturiert die Umsetzung, Slarti übernimmt daraus die technische Implementierung und überführt die Ergebnisse in das operative Gitea-Backlog.

## Gitea-Kontext

`context.md` dokumentiert die Gitea-Pfade, Issue-Typen und Slartis Konvention
fuer Epics und ausfuehrbare Arbeitspakete. Der oeffentlich bereinigte Snapshot
aller Backlog-Issues und sein aktuelles Summary liegen unter `GITEA/`;
Synchronisationsskripte sind bewusst nicht Bestandteil dieses Stands.
