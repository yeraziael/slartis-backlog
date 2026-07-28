# Audiobookshelf — References

## GitHub Issues

| Issue | Title | State | Scope |
|---|---|---|---|
| [#55](https://github.com/yeraziael/slartis-backlog/issues/55) | Keycloak Authorization | Open | Homelab-wide authorization model (Audiobookshelf is one client among many) |
| [#57](https://github.com/yeraziael/slartis-backlog/issues/57) | ACP Pilot 1: Audiobookshelf Zielarchitektur | Open | Architecture baseline, component boundaries, child-issue graph |
| [#58](https://github.com/yeraziael/slartis-backlog/issues/58) | Audiobookshelf: Docker-Service auf Pi5 | Closed | Compose deployment, volumes, healthcheck |
| [#59](https://github.com/yeraziael/slartis-backlog/issues/59) | Audiobookshelf: Reverse Proxy und TLS | Closed | VIRTUAL_HOST, LETSENCRYPT, vhost.d, WebSocket |
| [#60](https://github.com/yeraziael/slartis-backlog/issues/60) | Audiobookshelf: Keycloak-OIDC und SSO | Open | OIDC client, group-based access, break-glass, secret rotation |
| [#62](https://github.com/yeraziael/slartis-backlog/issues/62) | ABS Configuration & Storage | Open | Volume layout, backup strategy, environment config |
| [#77](https://github.com/yeraziael/slartis-backlog/issues/77) | Hosting Baseline & Hostname Registry | Open | Authoritative hostname registry, DNS, TLS strategy |

## Gitea (Homelab/Architecture) Pull Requests

| PR | Title | Status | Related GH Issue |
|---|---|---|---|
| [#56](http://192.168.2.30:3000/Homelab/Architecture/pulls/56) | docs: AUDIOBOOKSHELF.md baseline | Superseded | #57 |
| [#57](http://192.168.2.30:3000/Homelab/Architecture/pulls/57) | docs: STORAGE.md (NAS baseline) | Merged | — |
| [#58](http://192.168.2.30:3000/Homelab/Architecture/pulls/58) | fix: align AUDIOBOOKSHELF.md with STORAGE.md | Superseded | #57 |
| [#59](http://192.168.2.30:3000/Homelab/Architecture/pulls/59) | docs: STORAGE.md podcasts | Merged | — |
| [#60](http://192.168.2.30:3000/Homelab/Architecture/pulls/60) | docs: podcasts in AUDIOBOOKSHELF.md | Superseded | #57 |
| [#61](http://192.168.2.30:3000/Homelab/Architecture/pulls/61) | docs: consolidated AUDIOBOOKSHELF.md | Superseded | #57 |
| [#62](http://192.168.2.30:3000/Homelab/Architecture/pulls/62) | docs: final AUDIOBOOKSHELF.md | Merged | #57 |
| [#63](http://192.168.2.30:3000/Homelab/Architecture/pulls/63) | feat: audiobookshelf compose | Merged | #58 |
| [#65](http://192.168.2.30:3000/Homelab/Architecture/pulls/65) | fix: healthcheck port | Merged | #58 |
| [#68](http://192.168.2.30:3000/Homelab/Architecture/pulls/68) | feat: audiobookshelf proxy + TLS | Merged | #59 |
| [#70](http://192.168.2.30:3000/Homelab/Architecture/pulls/70) | fix: VIRTUAL_PORT correction | Merged | #59 |
| [#76](http://192.168.2.30:3000/Homelab/Architecture/pulls/76) | feat: audiobookshelf OIDC | Merged | #60 |

## Review Packages (yeraziael/slartis-backlog)

| Review | Path | Scope |
|---|---|---|
| GH-57 (v4) | `docs/review/gh64-acp-pilot57-findings/` | ACP Pilot 1 findings, architecture baseline |
| GH-58 (v2) | `review/gh58-v2/` | Docker service review evidence |
| GH-59 | `docs/review/gh59-audiobookshelf-proxy-tls/` | Proxy + TLS review package |

## Architecture Documents (Homelab/Architecture, Gitea)

| Document | Path | Purpose |
|---|---|---|
| AUDIOBOOKSHELF.md | `docs/AUDIOBOOKSHELF.md` | Authoritative architecture document (source for GH-57) |
| PI_SERVICES.md | `docs/PI_SERVICES.md` | Pi5 service registry |
| STORAGE.md | `docs/STORAGE.md` | NAS storage baseline |
| keycloak-service-sso.md | `docs/keycloak-service-sso.md` | Keycloak SSO runbook |
| audiobookshelf-oidc.md | `pi/audiobookshelf/audiobookshelf-oidc.md` | OIDC implementation doc (GH-60) |
| audiobookshelf-runbook.md | `pi/audiobookshelf/audiobookshelf-runbook.md` | Operations runbook (GH-60) |

## Key Files (Homelab/Architecture, Gitea)

| File | Path | Purpose |
|---|---|---|
| Compose | `pi/compose/audiobookshelf.yml` | Docker Compose service definition |
| Proxy test | `pi/tests/test_audiobookshelf_proxy.sh` | 27-assertion proxy contract test |
| vhost.d | `pi/compose/vhost.d/audiobookshelf.hl.maier.wtf_location` | nginx-proxy location config |
| OIDC setup | `pi/audiobookshelf/scripts/setup-keycloak.sh` | Keycloak client creation |
| ABS settings | `pi/audiobookshelf/scripts/apply-abs-settings.sh` | Audiobookshelf OIDC config |
| Break-glass | `pi/audiobookshelf/scripts/break-glass-setup.sh` | Password generation + Telegram |
| Verify break-glass | `pi/audiobookshelf/scripts/verify-break-glass.sh` | Blackbox break-glass test |
| Secret rotation | `pi/audiobookshelf/scripts/rotate-keycloak-secret.sh` | OIDC client secret rotation |
| Build evidence | `docs/gh58-deployment-evidence.md` | GH-58 deployment evidence |

## External References

| Resource | URL | Purpose |
|---|---|---|
| Audiobookshelf | https://www.audiobookshelf.org/ | Official project site |
| Audiobookshelf GitHub | https://github.com/advplyr/audiobookshelf | Source code, releases |
| nginx-proxy | https://github.com/nginx-proxy/nginx-proxy | Reverse proxy used by Homelab |
| acme-companion | https://github.com/nginx-proxy/acme-companion | Let's Encrypt automation |
| Keycloak | https://www.keycloak.org/ | Identity provider |
| OpenID Connect | https://openid.net/connect/ | OIDC protocol specification |
| Let's Encrypt | https://letsencrypt.org/ | TLS certificate authority |
| QNAP | https://www.qnap.com/ | NAS manufacturer |

## Homelab Infrastructure References

| Subject | Source | Notes |
|---|---|---|
| Repository structure | `PROTOCOL.md` | Machine-to-Machine Engineering Protocol |
| Gitea backlog context | `context.md` | Issue types, API paths, epic discovery |
| Deployment rules | `AGENTS.md` (Slarti) | Git-workflow mandate, Slarti/Lydia boundary |
| ACP findings | `docs/review/gh64-acp-pilot57-findings/` | ACP protocol refinements from GH-57 |
| Matrix architecture | `docs/review/matrix-server/` | Reference for similar Homelab service architecture |
