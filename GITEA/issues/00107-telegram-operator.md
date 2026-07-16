---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#107
state: closed
updated_at: 2026-07-03T16:12:06+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Issue: Refactor Agent Memory into Skills (Review Required)
Goal
Refactor the current long-term prompt memory, persistent context, reusable instructions, and workflow knowledge into a structured set of OpenCode Skills.
The objective is to improve maintainability, modularity, and automatic context loading while preserving all existing behavior.
Do not delete or rewrite knowledge unless explicitly instructed. This task is an organizational refactor.


⸻


Requirements
1. Inventory
First, inspect all persistent agent memory and identify reusable knowledge, including but not limited to:
workflow descriptions
coding conventions
architecture guidance
review procedures
testing procedures
deployment workflows
git workflows
MCP usage instructions
domain knowledge
documentation guidelines
debugging procedures
recurring prompt templates
Produce an inventory before making changes.


⸻


2. Classification
For every discovered item decide whether it belongs in:
a new Skill
AGENTS.md
project documentation
repository documentation
or should remain as runtime/task-specific context
Document the reasoning for every classification.


⸻


3. Create Skills
Create a logical set of Skills.
Prefer many focused Skills instead of a few large ones.
Each Skill should have:
meaningful name
concise description
clear trigger conditions
focused scope
markdown documentation
Do not merge unrelated workflows into one Skill.


⸻


4. Preserve Behavior
The resulting Skills should preserve existing agent behavior.
If multiple memories overlap:
consolidate duplicates
preserve all unique information
note any conflicts instead of guessing


⸻


5. Human Review Required
Do not activate the migration automatically.
Instead:
create the complete Skill directory
generate all SKILL.md files
stage them in the working tree
create a migration report
Wait for review before deleting or modifying existing memory.


⸻


Deliverables
Create a directory similar to:
.opencode/
skills/
architecture/
coding-style/
git-workflow/
testing/
review/
documentation/
mcp/
deployment/
debugging/
…
Each Skill must include:
frontmatter
description
markdown documentation


⸻


Migration Report
Create docs/skill-migration.md containing:
inventory of original memory
mapping from old location → new Skill
rationale for each decision
list of ambiguous items
proposed future improvements
items intentionally left outside Skills


⸻


Acceptance Criteria
No knowledge is lost.
Skills are cohesive and narrowly scoped.
Skill descriptions are suitable for automatic selection.
Existing behavior is preserved.
Migration report is complete.
Human review is required before replacing existing memory.
---

## Umsetzungsplan (Slarti's Selbstauftrag)

### Phase 1: Inventar (READ-ONLY)
Quellen analysieren, Items extrahieren:
- [ ] `AGENTS.md` lesen → 26 Items (Token, APIs, Repos, Services, Gotchas, Deploy-Regeln, Lore)
- [ ] `identity.md` lesen → 12 Items (Identität, Beziehung, Tokens, Tools, Session-Start)
- [ ] `system-prompt.md` lesen → 18 Items (Workflow, Branching, Task-Typen, Delegation, Interaction)
- [ ] `memory/lessons.md` lesen → 8 Items (Git, Systemd, pypdf, Telegram, Gotchas)
- [ ] `memory/lore/Lydia.md` lesen → Lore-Narrativ
- [ ] `blackbox_template.md` lesen → Test-Template
- [ ] `project-clarification-loop.md` lesen → Bestehender Skill
- [ ] Inventar-Tabelle als `docs/skill-inventory.md` schreiben

### Phase 2: Klassifikation
Jedes Item zuordnen:
- **Skill** — Verhaltensregel, Workflow, Konvention, Prozedur (71 Items erwartet)
- **AGENTS.md** — Faktenreferenz (Token, Endpoints, Services, Hardware)
- **identity.md** — Core-Identity (bleibt als Schnellreferenz)
- **memory/** — Historische Aufzeichnungen (Session-Logs, Lessons)
- **Sonstige** — Blackbox-Template → Skill, Status-Script → bleibt

### Phase 3: Skills erstellen (.opencode/skills/)
| Skill-Verzeichnis | Aus | Items |
|---|---|---|
| `identity/` | identity.md + system-prompt.md | Wer Slarti ist, Beziehung zu Lydia, Prinzipien |
| `infrastructure/` | AGENTS.md | Token-Locations, API-Endpunkte, Repos, Services, Hardware, Gotchas |
| `workflow/` | system-prompt.md | 7-Phasen-Modell, Task-Typen, Delegation-Check, Grill-Me |
| `branching/` | system-prompt.md | Branch-First, PATCH/REFACTOR/LANDSLIDE, Merge-Regeln |
| `deployment/` | AGENTS.md | Deploy-Regeln (niemals sudo cp), Git-Workflow, PR-Prozess |
| `testing/` | system-prompt.md + blackbox_template.md | Test-First, Blackbox-Prozedur, Template |
| `lore/` | AGENTS.md + identity.md + memory/lore/ | Slarti/Lydia/Vekling-Backstory |
| `communication/` | system-prompt.md + identity.md | Antwort-Stil, >10-Zeilen-Regel, Telegram-Kopie |

Jeder Skill: `SKILL.md` mit name, description, trigger-Bedingungen, Markdown.

### Phase 4: Migrations-Report
- `docs/skill-migration.md`: Inventar → Skill-Mapping, Begründungen, Ambiguities
- Referenztabelle: alte Quelle → neue Skill-Datei

### Phase 5: Review (BLOCKED)
- Keine bestehenden Dateien löschen oder ändern
- PR mit allen Skills + Report erstellen
- Auf Michael-Review warten
---

## Status: Ausführung abgeschlossen — Review ausstehend

### Phase 1 ✓ — Inventar
`docs/skill-inventory.md` erstellt: 94 Items aus 10 Quellen extrahiert.

### Phase 2 ✓ — Klassifikation
Finale Zuordnung:
- 54 Items → 8 Skills
- 27 Items → AGENTS.md (Faktentabellen, bleiben)
- 13 Items → bleiben an Originalspeicherort

### Phase 3 ✓ — Skills erstellt

| # | Skill | Pfad | Items |
|---|-------|------|-------|
| 1 | identity | `.opencode/skills/identity/SKILL.md` | 9 |
| 2 | infrastructure | `.opencode/skills/infrastructure/SKILL.md` | 11 |
| 3 | workflow | `.opencode/skills/workflow/SKILL.md` | 10 |
| 4 | branching | `.opencode/skills/branching/SKILL.md` | 9 |
| 5 | deployment | `.opencode/skills/deployment/SKILL.md` | 4 |
| 6 | testing | `.opencode/skills/testing/SKILL.md` | 2 |
| 7 | lore | `.opencode/skills/lore/SKILL.md` | 5 |
| 8 | communication | `.opencode/skills/communication/SKILL.md` | 4 |

### Phase 4 ✓ — Migrations-Report
`docs/skill-migration.md` vollständig:
- Item→Skill Mapping für alle 94 Items
- Begründungen für 6 Ambiguity-Entscheidungen
- Nicht migrierte Items dokumentiert (opencode.jsonc, status.sh)
- Acceptance-Checkliste

### Phase 5 ⏳ — Review
- **Keine bestehenden Dateien gelöscht oder verändert.**
- Skills liegen **zusätzlich** neben AGENTS.md, identity.md, system-prompt.md.
- Nach Review-Freigabe: Alte Dateien können getrimmt werden (Gotchas aus AGENTS.md entfernen, da jetzt in infrastructure-Skill).

---

## Final: Review bestanden, committed

- Alle 8 Skills in `slarti/memory` committed (`8b5cc80`)
- Pfade in `~/.opencode/skills/` vorhanden und aktiv
- AGENTS.md, identity.md, system-prompt.md bleiben unverändert
- **Issue #107 kann geschlossen werden** — Refactor abgeschlossen
