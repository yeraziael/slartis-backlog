# References and Migration Map

## Primary sources (verified 2026-07-29)

- Issue #110: canonical migration tracker and Plan-as-Code entrypoint.
- PR #71: merged initial CLIProxyAPI Homelab plan, commit `3530872`; its eight legacy files remain in Git history.
- PR #130: open CAP-P01 verification at commit `9b77bb7`; its evidence is incorporated here because it is not an ancestor of PR #131.
- Issue #74: open architecture, security and compatibility spike mapped below.
- [`router-for-me/CLIProxyAPI` v7.2.104](https://github.com/router-for-me/CLIProxyAPI/tree/v7.2.104): CLI/OAuth subscription gateway upstream.
- [`BerriAI/litellm`](https://github.com/BerriAI/litellm): LiteLLM gateway upstream; version pin remains CAP-L01 scope.
- [LiteLLM proxy](https://docs.litellm.ai/docs/simple_proxy), [OpenAI-compatible upstreams](https://docs.litellm.ai/docs/providers/openai_compatible), [Ollama](https://docs.litellm.ai/docs/providers/ollama), [virtual keys](https://docs.litellm.ai/docs/proxy/virtual_keys), [health routing](https://docs.litellm.ai/docs/proxy/health_check_routing) and [fallbacks](https://docs.litellm.ai/docs/proxy/reliability).
- [OpenCode providers](https://opencode.ai/docs/providers) and [OpenCode Zen](https://opencode.ai/docs/zen).
- `yeraziael/ai-governance`: released global governance source.
- Homelab architecture repository on Gitea: runtime authority; not mutated by this plan.

## LiteLLM and OpenCode verification

| Claim | Primary-source evidence | Verdict and required follow-up |
|---|---|---|
| OpenCode can use one LiteLLM endpoint | OpenCode custom providers accept an OpenAI-compatible `baseURL`; LiteLLM exposes an OpenAI-compatible proxy | Confirmed; OpenCode config must contain only the LiteLLM provider |
| LiteLLM can call Zen Free | Zen documents an OpenAI-compatible `/v1/chat/completions` endpoint; LiteLLM documents OpenAI-compatible upstreams with `openai/` model prefix and `/v1` API base | Confirmed for compatible Zen models; pin exact model IDs and API variants in CAP-L01/L03 |
| LiteLLM can call Ollama | LiteLLM documents `ollama_chat/<model>` routing, streaming and tool calling | Confirmed; container-to-host/network address is runtime-specific and not assumed to be `localhost` |
| Per-client LiteLLM credentials | LiteLLM virtual keys support model restrictions, budgets and rate limits | Confirmed; real keys remain operator-only CAP-X02 scope |
| Model discovery | LiteLLM exposes model metadata, but OpenCode custom-provider documentation requires explicit model declarations | Automatic discovery is not assumed; CAP-L03 owns explicit model-ID mapping and drift validation |
| Health and fallback | LiteLLM documents background health routing, cooldown and model-group fallbacks | Confirmed capability; CAP-R019 still forbids silent subscription-to-paid fallback |
| Deterministic dry-run, Decision Hash and probes | No primary source establishes the complete project contract as native behavior | Custom management-layer work under CAP-R01/I04 per CAP-D030 |

Zen Free offers have no availability SLA and may be time-limited. Their use is an availability optimization, not a production guarantee. API compatibility must be tested per exact model because Zen exposes multiple API styles.

## CLIProxyAPI upstream verification

**Verified source:** `router-for-me/CLIProxyAPI` release v7.2.104, 2026-07-29.

| Property | Actual upstream | Plan disposition |
|---|---|---|
| Primary purpose | Wrap supported CLI/OAuth subscriptions behind compatible APIs | Retained only as LiteLLM downstream; never OpenCode frontdoor |
| Providers | Kimi, OpenAI/Code paths, Claude, Antigravity, Grok, Codex and compatible relays, depending on release | Every provider requires an exact-version capability and compliance decision |
| Authentication | OAuth and provider-specific keys | Credentials stay inside CLIProxyAPI; technical support is not policy approval |
| Default image | Upstream examples use mutable image conventions | Compliance blocker; CAP-B01 must pin source and digest |
| Ports | Upstream Compose exposes 8317 plus OAuth callback ports 8085, 1455, 54545, 51121 and 11451 | Compliance blocker; deny by default and decide each provider port separately |
| Network bind | Defaults may expose the API beyond the intended private path | Compliance blocker; CAP-I01 must bind only to the LiteLLM service network |
| Management API | Full management surface under `/v0/management/` | Disabled remotely by default; approved operator path only |
| Plugin system | Native in-process plugins can access process capabilities | Compliance blocker; disabled under CAP-D029 |
| Control panel | Bundled management asset with update/download behavior | Compliance blocker; disabled under CAP-D029 |
| Cloaking | Request-modification/cloaking functionality exists | Compliance blocker; disabled under CAP-D029 |
| Routing | Multi-credential pools support strategies including `fill-first`; session affinity is configurable | CAP-D031 selects `fill-first` and requires normalized affinity propagation |
| Retry behavior | Native retries, cooldown and quota switching exist | Exact 1-minute to 6-hour probe contract is custom CAP-I04 work |
| Architecture support | Linux ARM64 artifacts/build path exist | Build feasibility confirmed; host suitability remains operator-gated CAP-X01 |

## Legacy inventory

All eight files introduced by PR #71 are classified:

| File | Classification | Canonical target |
|---|---|---|
| `CLIProxyAPI-Homelab/context.md` | Superseded | `README.md`, `architecture.md`, CAP-D024 |
| `CLIProxyAPI-Homelab/contract.md` | Partially retained | `requirements.md`, CAP-D029 through CAP-D031 |
| `CLIProxyAPI-Homelab/prerequisites.md` | Retained, runtime verification required | CAP-L01, CAP-B01, CAP-X01 |
| `CLIProxyAPI-Homelab/tests.md` | Retained and expanded | `testing.md`, CAP-E04, CAP-A01 |
| `CLIProxyAPI-Homelab/dod.md` | Superseded | `backlog.md`, `plan.yaml` |
| `CLIProxyAPI-Homelab/ci-cd.md` | Retained | CAP-G03 and per-task CI evidence |
| `CLIProxyAPI-Homelab/milestones/M01/context.md` | Superseded | CAP-P01, CAP-P02 |
| `CLIProxyAPI-Homelab/milestones/M01/contract.md` | Superseded | CAP-P01, CAP-P02, CAP-B01, CAP-X01 |

## Issue #74 mapping

| #74 obligation | Resolution |
|---|---|
| Current releases, registry, architectures and reproducibility | Source facts completed in CAP-P01; exact pins delegated to CAP-L01 and CAP-B01 |
| ARM64 start and resource capture | Operator-gated CAP-X01; no runtime action in this epic |
| Permanent and temporary ports | Six upstream ports inventoried; each remains denied until CAP-I01/CAP-X02 approval |
| API, management, panel, plugin, debug and logging surfaces | Completed by CAP-P01 and hardened by CAP-D029 |
| API-key versus OAuth/subscription provider assessment | Technical classes documented; provider-policy approval remains CAP-X02 |
| OpenCode endpoint test | CAP-A01 prepares evidence contract; CAP-X03 executes runtime pilot |
| Secure baseline | Defined by CAP-D027, CAP-D029 and CAP-D031; implementation CAP-I01/I02 |
| Go/No-Go and host decision | CAP-X01 operator gate |

Issue #74 is superseded as an execution packet only after PR #131 merges and all mapped CAP issues exist. Its provenance remains linked.

## Detailed source-to-target migration matrix

| # | Legacy statement | Classification | Canonical target |
|---|---|---|---|
| 1 | One gateway endpoint for OpenCode and later agents | Retained with corrected frontdoor | CAP-D024, CAP-R001 |
| 2 | CLIProxyAPI is that frontdoor | Superseded | LiteLLM frontdoor, CAP-D025 |
| 3 | Zen Free traverses CLIProxyAPI | Conflicting | LiteLLM direct, CAP-R003 |
| 4 | Internal-only reachability | Retained and strengthened | CAP-R017, CAP-D029 |
| 5 | OAuth tokens and API keys are critical secrets | Retained | CAP-D027, CAP-X02 |
| 6 | Reproducible Compose service | Split by gateway | CAP-L02, CAP-I01 |
| 7 | ARM64 verification before host decision | Retained | CAP-X01 |
| 8 | Pinned image, no `latest` | Retained; upstream default blocks | CAP-L01, CAP-B01 |
| 9 | API port internal-only | Retained | CAP-R017, CAP-I01 |
| 10 | Management API disabled or local | Retained and strengthened | CAP-D029 |
| 11 | No unchecked control-panel downloads | Retained | CAP-D029 |
| 12 | Secrets outside Git in restricted mounts | Retained | CAP-D027, CAP-X02 |
| 13 | Separate client gateway keys | Retained at LiteLLM | CAP-R004, CAP-L03 |
| 14 | Provider activation requires compliance | Retained | CAP-R010, CAP-X02 |
| 15 | Cloaking and identity confusion disabled | Retained | CAP-D029 |
| 16 | Logs exclude prompts, responses and secrets | Retained; verification required | CAP-O01, CAP-E04 |
| 17 | Health, backup, restore, update and rollback tested | Retained | CAP-O02, CAP-E04, CAP-X03 |
| 18 | OpenCode pilots before Slarti/Lydia | Retained | CAP-A01, CAP-X03, CAP-X04 |
| 19 | Current upstream facts verified | Completed | this file |
| 20 | Runtime resource usage measured | Operator-gated | CAP-X01 |
| 21 | Ports documented per provider | Inventory complete; activation pending | CAP-I01, CAP-X02 |
| 22 | Management/plugin/debug audit | Completed; secure defaults decided | CAP-D029 |
| 23 | API-key versus OAuth assessed per provider | Technical inventory complete, compliance open | CAP-X02 |
| 24 | OpenCode internal endpoint tested | Runtime-gated | CAP-X03 |
| 25 | Secure baseline defined | Completed as plan decision | CAP-D027, CAP-D029, CAP-D031 |
| 26 | Go/No-Go and host selected | Operator-gated | CAP-X01 |

## Independent review disposition

Three read-only reviews were completed on PR #131 head `8635f78`: LiteLLM/OpenCode upstream validation, CLIProxyAPI upstream/security validation and cross-document consistency review. Accepted findings and resolutions:

| Finding | Resolution |
|---|---|
| CAP-P01 evidence was stranded in open PR #130 | Incorporated into this file; PR #130 may be superseded after PR #131 merge |
| Hard-coded free-model ladder conflicted with governance authority | CAP-R021/R022/R024 and CAP-D028 make released governance authoritative |
| Classification timing contradicted routing order | `governance.md` now requires pre-routing proposals |
| Sequential use was not tied to upstream configuration | CAP-D031 selects `fill-first` |
| Probe, dry-run and audit were implied native | CAP-D030 marks them custom implementation |
| Plugin, control-panel, cloaking and remote management controls were incomplete | CAP-D029, operations and tests fail closed |
| OpenCode custom-provider model discovery was assumed | Explicit mapping and drift test assigned to CAP-L03 |

## Verification rule

All upstream-sensitive and provider-policy claims are rechecked against primary sources in the execution task that pins or activates them. No credential method, subscription forwarding path or exposed callback port is approved merely because it is technically possible.
