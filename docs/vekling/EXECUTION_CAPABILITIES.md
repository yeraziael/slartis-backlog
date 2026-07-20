# Vekling Execution Capabilities — Reviewer Entrypoint

> Canonical reviewer entrypoint for future ChatGPT reviewer sessions using the
> GitHub connector. This document summarizes the worker's execution skills and
> capabilities as measured by experiment **E-001** (protocol
> `vekling.execution.v0.4`). It is a publication of pre-existing findings; it does
> not repeat E-001 discovery or analysis, and it does not change E-001's findings.

## Purpose

This file exists so that a future reviewer optimizing worker prompts can, from a
single entrypoint:

- see which skills and capabilities the worker actually has,
- know whether each statement is **observed**, **inferred**, or **assumed**, and
- reach every underlying E-001 evidence artifact through repository-relative links.

Everything below is sourced from the E-001 evidence copied into this repository
(see [Source Artifacts](#source-artifacts)). No capability, version, entrypoint,
or constraint is asserted here that is not supported by E-001.

## E-001 Baseline

- **Experiment:** E-001 — Execution Capability Baseline
- **Protocol:** `vekling.execution.v0.4`
- **Mode:** documentation-only (no runtime, configuration, or environment changes) — *observed*
- **Source of record:** Gitea `Homelab/Architecture`, pull request #35 (merged), source commit `75a967b`

Headline metrics (from `findings.json`):

| Metric | Value | Classification |
|---|---|---|
| skills_discovered | 27 | observed |
| capabilities_discovered | 44 | observed |
| observed_ratio | 0.2727 | observed |
| inferred_ratio | 0.7273 | observed |
| assumed_ratio | 0.0 | observed |
| duplicate_capabilities | 0 | observed |
| orphan_capabilities | 0 | inferred |
| dependency_cycles | 0 | inferred |
| average_dependencies_per_skill | 1.3704 | inferred |
| capability_to_skill_ratio | 1.6296 | observed |

Capability composition: 12 tool entrypoints (**observed**) + 28 skill
capabilities (**inferred**) + 4 implicit capabilities (**inferred**) = 44.

## Observed Skills

27 skill units were observed on disk (evidence: `skills.json`). A runtime
discrepancy was recorded, not resolved: the runtime `available_skills` list also
contains 27 entries but **excludes** the disk-only `project-clarification-loop`
and **includes** the builtin `customize-opencode`.

**Custom skills (24)** — `~/.opencode/skills` (*observed*):

`adr`, `aegir`, `api-design`, `architecture`, `branching`, `communication`,
`deployment`, `diagnose`, `gitea`, `gitea-dashboard-report`, `github-cli`,
`grill-with-docs`, `grow-dream`, `handoff`, `identity`, `infrastructure`, `lore`,
`pi-docker`, `project-clarification-loop`, `prototype`, `tdd`, `testing`,
`triage`, `workflow`.

**Project skills (3)** — `~/.config/opencode/skills` (*observed*):

`eldir-debug`, `eldir-setup`, `vekling-delegation`.

**Builtin skills (1)** — exposed only at runtime (*observed*):

`customize-opencode` (`<built-in>`).

> Note (*observed*): `project-clarification-loop` is present on disk as a bare
> `.md` file but is **absent** from the runtime `available_skills` block. Whether
> it is loadable at runtime is **assumed / unknown** (see
> [Dependencies and Limitations](#dependencies-and-limitations)).

## Capability Reference

Source: `capabilities.json`. Canonical id schemes are **assumed** conventions
adopted by E-001 (`cap.tool.<entrypoint>`, `cap.skill.<name>`,
`cap.implicit.<name>`); they are not observed from any declaration.

### Tool entrypoints (12) — *observed*

Directly present in the runtime tool interface:

`bash`, `edit`, `glob`, `grep`, `question`, `read`, `skill`, `task`,
`todowrite`, `webfetch`, `websearch`, `write`.

### Skill capabilities (28) — *inferred*

One `cap.skill.<name>` per skill (24 custom + 3 project + 1 builtin), each
derived from that skill's `SKILL.md` description. See `capabilities.json` for the
full per-skill capability text and justification.

### Implicit capabilities (4) — *inferred*

- `subagent-orchestration` — orchestrate subagents through policy profiles
  (flash-free, local-fast, luna, sol, terra). *Observed constraint:* each
  subagent start requires explicit operator approval (`permission.task = ask`).
- `custom-command` — invoke custom slash-commands (`status`, `gs`).
- `local-model-inference` — route inference to local Ollama models
  (configured, not exercised — see limitations).
- `reference-access` — access project reference directories (memory, backlog,
  context, workspace, tools).

## Skill-to-Capability Mapping

Source: `capabilities.json` and `dependency_graph.json`.

- Mapping is **1:1**: each skill maps to exactly one `cap.skill.<name>`
  capability; each tool entrypoint maps to exactly one `cap.tool.<entrypoint>`
  capability. `duplicate_capabilities = 0` (*observed*).
- Skill capabilities depend on tool capabilities and on other skill capabilities
  through `depends_on` edges. All 37 edges are **inferred** from `SKILL.md`
  procedure text; no dependency metadata is declared in machine-readable form.

Notable skill-to-skill relationships (*inferred*, from `dependency_graph.json`):

| Skill | Depends on |
|---|---|
| `grill-with-docs` | `workflow`, `adr` |
| `triage` | `gitea`, `workflow` |
| `gitea-dashboard-report` | `gitea` |
| `tdd` | `testing` |
| `diagnose` | `infrastructure` |
| `pi-docker` | `deployment` |
| `workflow` | `branching`, subagent-orchestration |
| `vekling-delegation` | subagent-orchestration |

## Dependencies and Limitations

From `dependency_graph.json` and `findings.json`:

- **No dependency cycles** were observed in the inferred edge set
  (`dependency_cycles = 0`, *inferred*).
- **No orphan capabilities**: every dependency edge endpoint is defined in
  `capabilities.json` (`orphan_capabilities = 0`, *inferred*). Leaf/standalone
  nodes (e.g. `cap.tool.glob`) are not treated as orphans.
- **Average dependencies per skill = 1.3704** (*inferred*; 37 edges / 27 skills).
- **Coverage limit (*assumed*):** only dependencies described in `SKILL.md` text
  were captured. Undescribed dependencies are unknown by omission — absence of an
  edge does not prove absence of a dependency.

Explicit unknowns carried from E-001 (`findings.json`):

- Runtime availability of the configured Ollama local models — **assumed**
  (configured in `opencode.jsonc`, not exercised under documentation-only mode).
- The full transitive dependency set per skill — **assumed / incomplete**.
- Whether `project-clarification-loop.md` is loadable at runtime — **assumed**
  (on disk but absent from the runtime `available_skills` block).

Operational constraint (*observed*): subagent launches are gated by explicit
operator approval; subagent policy profiles set `permission.task: deny`.

## Prompt Authoring Guidance

This guidance is derived only from E-001 findings. It tells a reviewer what may
safely be referenced in future worker prompts.

**Skills that can be referenced directly in worker prompts** (present and
runtime-exposed, *observed*): all 24 custom skills except
`project-clarification-loop`, all 3 project skills (`eldir-debug`,
`eldir-setup`, `vekling-delegation`), and the builtin `customize-opencode`.
Reference skills by their canonical id (the skill name).

- **Do not** rely on `project-clarification-loop` being loadable — it is on disk
  but not in the runtime `available_skills` list (*assumed / unknown*).

**Capabilities that are supported and safe to assume** (*observed* tool
entrypoints): `bash`, `edit`, `glob`, `grep`, `question`, `read`, `skill`,
`task`, `todowrite`, `webfetch`, `write`, `websearch`. A prompt may direct the
worker to read/search/edit/write files, run shell commands, load skills, ask the
operator questions, maintain a todo list, and fetch/search the web.

**Capabilities that require caution** (*inferred* or *assumed*, do not assume
without verification):

- Subagent orchestration exists (`task`) but **every** subagent start needs
  explicit operator approval — never author a prompt that self-approves
  delegation.
- Local Ollama model inference is configured but **unverified**; do not assume it
  is available at runtime.
- Skill-to-skill dependencies are *inferred*; do not assume a skill silently
  pulls in another beyond the relationships listed above.

**Do not invent.** Do not reference skills, tool entrypoints, model versions, or
constraints that are not listed in this document or its evidence files. If a
capability is not in E-001, treat it as unknown.

## Evidence Classification

E-001 classifies every assertion as one of:

- **observed** — read directly from the filesystem or the runtime tool/skill
  interface (e.g. the 12 tool entrypoints, the 27 skills, the headline counts).
- **inferred** — derived by interpreting observed material (e.g. the 28 skill
  capabilities, the 4 implicit capabilities, all 37 dependency edges).
- **assumed** — a chosen convention or an explicit unknown (e.g. the canonical id
  schemes, Ollama runtime availability, `project-clarification-loop`
  loadability).

`assumed_ratio` over capabilities is 0.0 because assumptions live in the id
schemes and unknowns, which are not counted as capabilities.

## Source Artifacts

All evidence is copied unchanged from the E-001 source of record (Gitea
`Homelab/Architecture`, PR #35, commit `75a967b`). JSON files are byte-identical
copies.

- [Human-readable report](./evidence/E-001/report.md) — `report.md`
- [Canonical findings](./evidence/E-001/findings.json) — `findings.json`
- [Observed skills](./evidence/E-001/skills.json) — `skills.json`
- [Capability model](./evidence/E-001/capabilities.json) — `capabilities.json`
- [Dependency graph](./evidence/E-001/dependency_graph.json) — `dependency_graph.json`
