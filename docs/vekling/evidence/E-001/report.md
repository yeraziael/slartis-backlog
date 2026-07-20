# E-001 — Execution Capability Baseline

- **Protocol:** `vekling.execution.v0.4`
- **Experiment:** E-001
- **Objective:** Observe and model the worker's current execution capabilities without changing them. These artifacts become the baseline for future protocol evolution and capability measurements.
- **Mode:** documentation-only. No runtime, configuration, or environment changes were made.

Every statement below is classified as **observed**, **inferred**, or **assumed** per the protocol's research rules.

---

## Method

1. **Phase 1 — Observation (record only).** Enumerated the worker's skills, extensions, and tool entrypoints directly from the filesystem and the runtime tool/skill interface. No interpretation applied.
2. **Phase 2 — Model extraction.** Derived the execution model, capability model, and dependency graph from the observed material. Models were not modified.
3. **Phase 3 — Canonicalization.** Assigned canonical skill and capability ids and produced the capability mapping.

Observation sources:
- Filesystem: `~/.opencode/skills`, `~/.config/opencode/skills`, `~/.config/opencode/agent`, `~/.config/opencode/opencode.jsonc`, `~/.config/opencode/package.json`.
- Runtime: the tool interface (tool entrypoints) and the `available_skills` block.

---

## Phase 1 — Observations

### Tool entrypoints (observed)

Twelve tool entrypoints are exposed at runtime:
`bash`, `edit`, `glob`, `grep`, `question`, `read`, `skill`, `task`, `todowrite`, `webfetch`, `websearch`, `write`.

Classification: **observed** — directly present in the runtime tool interface.

### Skills (observed)

27 skill units on disk:

- **24 custom skills** under `~/.opencode/skills` (each a directory with `SKILL.md`, except `project-clarification-loop.md` which is a bare file).
- **3 project skills** under `~/.config/opencode/skills`: `eldir-debug`, `eldir-setup`, `vekling-delegation`.
- **1 builtin skill** exposed only at runtime: `customize-opencode` (`<built-in>`).

Discrepancy (observed): the runtime `available_skills` block lists 27 skills but **excludes** the disk-only `project-clarification-loop.md` and **includes** the builtin `customize-opencode`. Both counts are 27; the sets differ by one element. This is recorded, not resolved.

### Extensions (observed)

- **6 subagent policy profiles** under `~/.config/opencode/agent`: `policy-flash-free`, `policy-local-coder` (`disable: true`), `policy-local-fast`, `policy-luna`, `policy-sol` (`variant: high`), `policy-terra`. Each has `mode: subagent` and `permission.task: deny`.
- **Plugin dependency** `@opencode-ai/plugin` declared in `package.json`; **no** `plugin/` directory present.
- **Custom commands** `status` and `gs` and **local Ollama provider** declared in `opencode.jsonc`.
- **Runtime permission** `permission.task: ask` — subagent launches are gated.

---

## Phase 2 — Derived models (inferred)

### Execution model (inferred)

A control-plane orchestrator plans and delegates; execution follows a 7-phase workflow (`workflow` skill) under a branch-first model with three modes — PATCH / REFACTOR / LANDSLIDE (`branching` skill) — governed by a Git-workflow deployment mandate (`deployment` skill). Subagent delegation (`vekling-delegation`) is realized through the `task` tool and is gated by explicit operator approval.

Justification: derived from the `workflow`, `branching`, `deployment`, and `vekling-delegation` SKILL.md descriptions.

### Capability model (inferred)

44 capabilities total (see `capabilities.json`):
- 12 **tool capabilities** (observed) — `cap.tool.*`.
- 28 **skill capabilities** (inferred) — `cap.skill.*`, one per skill.
- 4 **implicit capabilities** (inferred) — subagent-orchestration, custom-command, local-model-inference, reference-access.

### Dependency graph (inferred)

37 `depends_on` edges (see `dependency_graph.json`). No dependency metadata is declared in machine-readable form; every edge is inferred from the procedures described in each SKILL.md. Notable skill-to-skill relationships:

- `grill-with-docs` → `workflow`, `adr`
- `triage` → `gitea`, `workflow`
- `gitea-dashboard-report` → `gitea`
- `tdd` → `testing`
- `diagnose` → `infrastructure`
- `pi-docker` → `deployment`
- `workflow` → `branching`, subagent-orchestration
- `vekling-delegation` → subagent-orchestration

No directed cycles were observed.

---

## Phase 3 — Canonicalization

- **Canonical skill id scheme (assumed):** `skill.<name>`, adopting the skill directory name.
- **Canonical capability id scheme (assumed):** `cap.tool.<entrypoint>`, `cap.skill.<name>`, `cap.implicit.<name>`.

Both schemes are **assumed** conventions chosen for this baseline; they are not observed from any declaration. Mapping is 1:1 (skill ↔ `cap.skill.<name>`, entrypoint ↔ `cap.tool.<entrypoint>`); see `capabilities.json`.

---

## Metrics

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

`assumed_ratio` is 0 because assumptions occur only in the Phase-3 id schemes, which are not counted as capabilities.

---

## Unknowns (preferred over guesses)

- Runtime availability of the configured Ollama local models — **assumed**, not exercised.
- The full transitive dependency set per skill — **assumed**; only dependencies described in SKILL.md text were captured (undescribed dependencies are unknown by omission).
- Whether `project-clarification-loop.md` is loadable at runtime — **assumed**; present on disk but absent from `available_skills`.

---

## Artifacts

- `research/E-001/report.md` — this report.
- `research/E-001/findings.json` — canonical experimental data.
- `research/E-001/skills.json` — observed skills.
- `research/E-001/capabilities.json` — observed capability model.
- `research/E-001/dependency_graph.json` — machine-readable dependency graph.
