# Playwright — References

## GitHub Issues and PRs

| Reference | Title | State | Scope |
|---|---|---|---|
| [#81](https://github.com/yeraziael/slartis-backlog/pull/81) | docs(epic): migrate Audiobookshelf to Plan-as-Code structure | Merged | Reference implementation for Plan-as-Code conventions |
| [#82](https://github.com/yeraziael/slartis-backlog/pull/82) | docs(playwright): define shared browser test platform and roadmap | Open | This epic |
| [#57](https://github.com/yeraziael/slartis-backlog/issues/57) | ACP Pilot 1: Audiobookshelf Zielarchitektur | Open | ACP protocol patterns, architecture conventions |
| [#55](https://github.com/yeraziael/slartis-backlog/issues/55) | Keycloak Authorization | Open | Homelab-wide authorization model |

## Audiobookshelf Epic (Reference Implementation)

| Document | Path | Relevance |
|---|---|---|
| README.md | `docs/epics/audiobookshelf/README.md` | Plan-as-Code structure reference |
| requirements.md | `docs/epics/audiobookshelf/requirements.md` | Requirement ID convention (R-XXX), RFC 2119 usage |
| contracts.md | `docs/epics/audiobookshelf/contracts.md` | Contract structure reference |
| decisions.md | `docs/epics/audiobookshelf/decisions.md` | Decision register format (ABDEC-XXX) |
| backlog.md | `docs/epics/audiobookshelf/backlog.md` | Child issue graph, provisional IDs |

## Architecture Documents (Homelab/Architecture, Gitea)

| Document | Path | Purpose |
|---|---|---|
| AUDIOBOOKSHELF.md | `docs/AUDIOBOOKSHELF.md` | Authoritative Audiobookshelf architecture |
| PI_SERVICES.md | `docs/PI_SERVICES.md` | Pi5 service registry |
| keycloak-service-sso.md | `docs/keycloak-service-sso.md` | Keycloak SSO runbook |

## External References

| Resource | URL | Purpose |
|---|---|---|
| Playwright | https://playwright.dev/ | Official documentation |
| Playwright GitHub | https://github.com/microsoft/playwright | Source code, releases |
| Playwright Docker | https://mcr.microsoft.com/en-us/product/playwright/about | Official container images |
| Keycloak | https://www.keycloak.org/ | Identity provider |
| OpenID Connect | https://openid.net/connect/ | OIDC protocol specification |
| nginx-proxy | https://github.com/nginx-proxy/nginx-proxy | Reverse proxy used by Homelab |

## Homelab Infrastructure References

| Subject | Source | Notes |
|---|---|---|
| Repository structure | `PROTOCOL.md` | Machine-to-Machine Engineering Protocol |
| Gitea backlog context | `context.md` | Issue types, API paths, epic discovery |
| Deployment rules | `AGENTS.md` (Slarti) | Git-workflow mandate, Slarti/Lydia boundary |
| ACP findings | `docs/review/gh64-acp-pilot57-findings/` | ACP protocol refinements from GH-57 |
| CI gotchas | `AGENTS.md` (Slarti) | Gitea Actions YAML 1.1, artifact upload, runner image |
| Testing conventions | `~/.opencode/skills/testing/SKILL.md` | Test-first principle, blackbox procedure |
