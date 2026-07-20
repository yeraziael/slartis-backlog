# INSTRUCTIONS.md — GH-59 Audiobookshelf Reverse Proxy und TLS

## Review target

This PR is the complete review surface for GH-59: adding reverse proxy and TLS
to the Audiobookshelf Docker service on Pi5.

## Source PRs

### Gitea PR #68 (merged by eddie-policy)
- Repo: `Homelab/Architecture`
- Head: `501fbebcf977c034acc44f6ba3c57a720556ffec`
- Base: `fd0477f1b3ea78b486bbd7460bce3debd742ee67`
- Diff SHA-256: `4e729ccb2da9e76251d8f8dfd8a470c3b235139f0a1a835b8d667be386aeb69d`
- Changes: proxy env vars, frontproxy_default network, vhost.d, tests, docs

### Gitea PR #70 (fix, merged 2026-07-20)
- Repo: `Homelab/Architecture`
- Head: `3ad3a55bed521b9058a789fdfd0734cc26603926`
- Base: `43610581f9ae69a9fd2541620fae7c2ada41f6cf`
- Merge base: `5ffba322320810f8a9e0541e927d2044c6bcae14`
- Diff SHA-256: `042cbc3ef0a9a980e7026634433d2c43e93de3eaef818626d8e4f1a0b63397e8`
- Changes: VIRTUAL_PORT "13378" → "80" (port correction)

## Effective configuration

| Setting | Value |
|---------|-------|
| VIRTUAL_HOST | `audiobookshelf.hl.maier.wtf` |
| VIRTUAL_PORT | `80` |
| LETSENCRYPT_HOST | `audiobookshelf.hl.maier.wtf` |
| LETSENCRYPT_EMAIL | `webmaster@maier.wtf` |
| expose | `["80"]` |
| networks | `audiobookshelf_internal`, `frontproxy_default` |
| vhost.d | `client_max_body_size 0`, WebSocket headers |

Both source PRs (#68 and #70) are now merged. The effective configuration is complete.

## Gate

Approval records the proxy and TLS configuration as versioned infrastructure.
Deployment to Pi5 is a separate operator action.
