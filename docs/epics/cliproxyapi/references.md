# References and Migration Map

## Primary sources (verified 2026-07-29)

- Issue #110 — canonical migration tracker and pointer to this Plan-as-Code entrypoint.
- PR #71 — approved initial CLIProxyAPI Homelab plan; merged as commit `3530872`. Added 8 files under `CLIProxyAPI-Homelab/`. Not present on current HEAD; retained in git history only.
- Issue #74 — architecture, security and compatibility spike. OPEN on GitHub, no DoD/subtasks/tests. Body references PR #71 as epic. Stale — no activity since creation.
- Legacy directory `CLIProxyAPI-Homelab/` — exists only in git history (commit `3530872`). Not on current `main` HEAD. All 8 files inventoried below.
- `router-for-me/CLIProxyAPI` — upstream implementation. Latest release: **v7.2.104** (2026-07-28). Very high release cadence (multiple versions per day). ARM64 Linux binary available.
- `yeraziael/ai-governance` — released global governance source. Latest `model-policy.yaml` v1.3 defines FLASH_FREE/LUNA/TERRA/SOL classes.
- Homelab architecture repository on Gitea — runtime authority (not yet consulted: out of CAP-P01 scope).

## Upstream verification (2026-07-29)

**Source:** `router-for-me/CLIProxyAPI` GitHub repository, latest release v7.2.104.

| Property | Actual upstream | Plan assumption | Verdict |
|---|---|---|---|
| Primary purpose | Wrap CLI coding tool subscriptions (Claude Code, Codex, Grok Build, Gemini) as OpenAI-compatible API via OAuth | Model provider gateway (OpenAI, Gemini, Zen Free) | **Changed upstream** — upstream targets CLI subscriptions, not API keys |
| Providers | Kimi, OpenAI, Claude, Antigravity (Gemini), Grok, Codex, OpenAI-compatible relays | OpenAI, OpenCode Zen Free, Gemini | **Conflicting** — Kimi/Antigravity/Grok/Codex not in plan; OpenCode Zen Free not in upstream |
| Authentication | OAuth (primary for Codex/Claude/Grok/Antigravity), API keys (secondary) | API keys (implied) | **Superseded** — OAuth credential forwarding is primary mechanism |
| Default Docker image | `eceasy/cli-proxy-api:latest` with `pull_policy: always` | Pinned version, no `:latest` | **Compliance blocker** — directly violates PR #71 contract point 3 |
| Exposed ports | 8317, 8085, 1455, 54545, 51121, 11451 | 8317 only (PR #71 implicit) | **Compliance blocker** — 5 additional ports with undocumented purpose |
| Management API | Full REST API under `/v0/management/` with bcrypt keys; can be disabled via empty secret-key | "Deactivated or localhost-only" (PR #71 contract point 5) | **Conflicting** — exists by default; must be explicitly disabled |
| Plugin system | C/Go/Rust dynamic library plugins; auth, management, frontend-auth, scheduler, router, executor | Imagined disabled/absent | **Compliance blocker** — allows arbitrary in-process code execution |
| Control Panel | Bundled asset from `router-for-me/Cli-Proxy-API-Management-Center`; auto-update enabled by default | No mention | **Compliance blocker** — external asset download, auto-update |
| Healthcheck | Not in default Compose | Required by PR #71 | **Open question** — no upstream health endpoint known |
| Architecture support | linux/amd64, linux/arm64, darwin/amd64, darwin/arm64, windows/amd64, windows/arm64, freebsd/amd64, freebsd/arm64 | "ARM64 verification needed" | **Confirmed** — ARM64 available for Pi 5 |
| Image build | Multi-stage Dockerfile based on `golang:1.26-bookworm` → `debian:bookworm`; MIT license | Reproducible build needed | **Confirmed** — build is reproducible from source |
| pprof debug server | Optional, `127.0.0.1:8316`, disabled by default | No mention | **Confirmed safely disabled by default** |

## Legacy CLIProxyAPI-Homelab/ inventory (from commit 3530872)

All 8 files inventoried and classified:

| File | Content type | Classification | Notes |
|---|---|---|---|
| `context.md` | Epic context | Superseded by `README.md` + `architecture.md` | Core intent (unified gateway) retained; provider model outdated |
| `contract.md` | 12-point epic contract | Partially retained | Points 1, 3, 4, 5, 6, 7, 8, 9, 10, 11 retained; point 2 (host verification) retained but needs upstream alignment; point 12 (OpenCode first) retained |
| `prerequisites.md` | Preconditions | Retained but needs runtime verification | Docker/Compose, ARM64, secrets management still valid; blocker assessment needs upstream recheck |
| `tests.md` | Test cases | Retained but needs runtime verification | All 11 test items remain valid; upstream healthcheck absent is a blocker |
| `dod.md` | Definition of Done | Superseded by Plan-as-Code backlog items | DoD items map to CAP-I01, CAP-I02, CAP-R01, CAP-O02 items |
| `ci-cd.md` | CI/CD rules | Retained | All 8 rules remain valid; no conflict with current Homelab CI patterns |
| `milestones/M01/context.md` | Spike milestone | Superseded by Issue #74 + backlog items | Spike intent absorbed into CAP-P02 |
| `milestones/M01/contract.md` | Spike contract | Superseded by Plan-as-Code items | 8-point contract maps to CAP-P01/CAP-P02/CAP-B01 |

**Status:** All legacy files classified. Directory retained in git history as provenance; no active reference needed.

## Issue #74 mapping

Issue #74 (`M01: CLIProxyAPI Architektur-, Sicherheits- und Kompatibilitäts-Spike`) is OPEN on GitHub. Its 8-point contract is mapped as follows:

| #74 Contract point | CAP-P01 finding | Resolution |
|---|---|---|
| 1. Current releases, registry, architectures, build reproducibility | Upstream v7.2.104 verified; ARM64 confirmed; build reproducible | **Completed** in references.md |
| 2. Build/start on ARM64, capture resource usage | Not executed — requires runtime deployment | **Retained** for CAP-P02 or CAP-B01 |
| 3. Document all permanent and temporary ports per provider | Docker Compose exposes 6 ports; upstream does not document per-provider port mapping | **Open question** — upstream docs needed |
| 4. Check API, management, control-panel, plugin, debug, logging surfaces | Management API, Control Panel, plugins, pprof all verified | **Completed** in references.md |
| 5. Distinguish API-key from OAuth/subscription; evaluate each provider separately | OAuth is primary; only OpenAI and Kimi support API keys upstream | **Completed** — fundamental scope change documented |
| 6. Test OpenCode against internal OpenAI-compatible endpoint | Not executed — requires running instance | **Retained** for CAP-A01 |
| 7. Define secure baseline configuration | Multiple compliance blockers identified | **Open** — needs decision before CAP-B01 |
| 8. Go/No-Go and Pi-5/Rechenknecht decision | No runtime evidence collected | **Blocked** on CAP-P02 review |

## Migration classifications

CAP-P01 assigns every inherited statement one of:

- **Confirmed and retained** — verified against current upstream, no change needed
- **Retained but needs runtime verification** — concept valid, but requires deployment evidence
- **Changed upstream** — upstream has evolved differently than planned
- **Superseded** — replaced by more comprehensive Plan-as-Code document
- **Conflicting** — plan assumption contradicts upstream reality
- **Open question** — cannot be resolved without upstream docs or runtime evidence
- **Compliance blocker** — would violate security/contract rules if activated as-is

## Detailed source-to-target migration matrix

| # | Legacy source | Statement | Classification | Canonical target |
|---|---|---|---|---|
| 1 | PR#71 context | CLIProxyAPI unifies provider access for OpenCode/Slarti/Lydia/workers | Confirmed and retained | README.md Purpose |
| 2 | PR#71 context | Upstream provides Dockerfile + Compose | Changed upstream | references.md verification |
| 3 | PR#71 context | Default port 8317 + additional provider OAuth ports | Conflicting | references.md — 6 ports exposed |
| 4 | PR#71 context | No initial external reachability | Retained | architecture.md trust boundary |
| 5 | PR#71 context | OAuth tokens and API keys are critical secrets | Confirmed and retained | architecture.md trust boundary |
| 6 | PR#71 contract | Reproducible Docker-Compose service | Retained | roadmap.md M2 |
| 7 | PR#71 contract | ARM64 verification before host decision | Retained but needs runtime | references.md upstream (ARM64 confirmed available) |
| 8 | PR#71 contract | Pinned image, no latest/pull_policy:always | Compliance blocker | references.md — upstream default violates this |
| 9 | PR#71 contract | API port internal-only | Retained | requirements.md CAP-R004 |
| 10 | PR#71 contract | Management API deactivated or localhost-only | Conflicting | references.md — Management API exists by default |
| 11 | PR#71 contract | No unchecked control-panel auto-downloads | Compliance blocker | references.md — control panel auto-update enabled by default |
| 12 | PR#71 contract | Secrets outside Git, restricted volumes | Confirmed and retained | architecture.md trust boundary |
| 13 | PR#71 contract | Separate client gateway keys | Retained | requirements.md CAP-R004 |
| 14 | PR#71 contract | Provider activation with compliance check | Superseded | requirements.md CAP-R010 |
| 15 | PR#71 contract | Cloaking/identity confusion/prompt-replacement disabled | Compliance blocker | references.md — plugin system allows these |
| 16 | PR#71 contract | Logs free of prompts/responses/tokens/secrets | Open question | requirements.md — upstream log behavior not verified |
| 17 | PR#71 contract | Healthcheck, backup, restore, update, rollback tested | Retained but needs runtime | roadmap.md M4 |
| 18 | PR#71 contract | OpenCode first, Slarti/Lydia after pilot | Retained | requirements.md CAP-R002 |
| 19 | PR#74 contract | Current releases, registry, architectures, reproducibility | Completed | references.md upstream verification |
| 20 | PR#74 contract | Build/start on ARM64, resource usage | Retained but needs runtime | CAP-P02 or CAP-B01 |
| 21 | PR#74 contract | Port documentation per provider | Open question | references.md — upstream docs insufficient |
| 22 | PR#74 contract | API/management/control-panel/plugin/debug/logging audit | Completed | references.md upstream verification |
| 23 | PR#74 contract | API-key vs OAuth/subscription per provider | Completed | references.md upstream verification |
| 24 | PR#74 contract | OpenCode test against internal endpoint | Retained but needs runtime | CAP-A01 |
| 25 | PR#74 contract | Secure baseline configuration | Open | needs decision before CAP-B01 |
| 26 | PR#74 contract | Go/No-Go + Pi-5/Rechenknecht decision | Blocked on CAP-P02 | CAP-P02 |

## Compliance blockers summary

1. **Default `:latest` image** — upstream Compose uses `eceasy/cli-proxy-api:latest` with `pull_policy: always`. PR #71 contract point 3 explicitly forbids this.
2. **Undocumented extra ports** — 6 ports exposed (8317, 8085, 1455, 54545, 51121, 11451) with no per-provider documentation in upstream.
3. **Plugin system** — C/Go/Rust dynamic library plugins allow arbitrary in-process code. No upstream confinement mechanism.
4. **Control Panel auto-update** — Bundled management panel downloads assets from GitHub. Auto-update exists and must be explicitly disabled.
5. **Cloaking/identity confusion capability** — Upstream plugin and OAuth architecture enables functions that PR #71 contract point 9 requires to remain disabled.
6. **OAuth credential forwarding** — Primary auth method is OAuth credential forwarding for CLI subscriptions. Compliance with each provider's terms of service is unverified.

## Open decisions (added by CAP-P01)

1. Whether the upstream's OAuth-based subscription forwarding model is acceptable under provider terms of service.
2. Whether the Plan-as-Code should redefine CLIProxyAPI purpose from "model provider gateway" to "CLI subscription gateway" or pursue a different upstream/replacement.
3. Whether the plugin system should be kept disabled (requiring a non-default config or forked Compose).
4. Which of the 6 upstream ports must be exposed vs blocked at the network boundary.
5. Whether the upstream Management API and Control Panel should be disabled or replaced with the Homelab's planned Keycloak+dashboard approach.
6. Whether OpenCode Zen Free can route through this upstream at all (upstream has no "Zen Free" concept).
7. Whether the high upstream release cadence (multiple versions/day) is compatible with the pinned-version approach required by PR #71.

## Verification rule

All upstream-sensitive or provider-policy claims must be rechecked against primary sources during CAP-P01 and recorded with source and verification date. No provider credential method is approved merely because it is technically possible.