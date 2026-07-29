# References and Migration Map

## Primary sources

- Issue #110 — canonical migration tracker and pointer to this Plan-as-Code entrypoint.
- PR #71 — approved initial CLIProxyAPI Homelab plan; mandatory migration input.
- Issue #74 — architecture, security and compatibility spike; must be explicitly mapped before closure or replacement.
- Legacy directory `CLIProxyAPI-Homelab/` — retained as provenance until CAP-P01 classifies every file.
- `router-for-me/CLIProxyAPI` — upstream implementation; exact supported version remains an open decision pending dated verification.
- `BerriAI/litellm` — upstream LiteLLM implementation; exact supported version remains an open decision pending dated verification.
- `yeraziael/ai-governance` — released global governance source.
- Homelab architecture repository on Gitea — runtime authority.

## Migration classifications

CAP-P01 assigns every inherited statement one of:

- Confirmed and retained
- Retained but needs runtime verification
- Changed upstream
- Superseded
- Conflicting
- Open question
- Compliance blocker

## Initial source-to-target map

| Source concern | Canonical target |
|---|---|
| Purpose, authority and progress | `README.md` |
| Stable requirements | `requirements.md` |
| Runtime and trust boundaries | `architecture.md` |
| Model routing and quality policy | `governance.md` |
| Experiment and Playwright behavior | `experiments.md` |
| Backup, degraded mode and provider operations | `operations.md` |
| Verification and evidence | `testing.md` |
| Milestones | `roadmap.md` |
| Executable decomposition and #74 mapping | `backlog.md` |
| Approved decisions | `decisions.md` |
| Provenance and dated external verification | this file |

## Verification rule

All upstream-sensitive or provider-policy claims must be rechecked against primary sources during CAP-P01 and recorded with source and verification date. No provider credential method is approved merely because it is technically possible.
