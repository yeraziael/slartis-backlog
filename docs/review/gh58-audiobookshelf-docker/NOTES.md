# NOTES.md — GH-58 Scope, Risks, and Correction Record

## Scope

GH-58 covers the reproducible Docker Compose service definition for
Audiobookshelf on Pi5. It excludes:
- Reverse proxy / TLS (GH-59)
- Keycloak / OIDC (GH-60)
- NAS mounts / NFS (separate child issue)
- Production media import
- Monitoring

## Versioned Source Repository

All changes are versioned in **Homelab/Architecture** on Gitea
(`192.168.2.30:3000`). The review package is published on GitHub because
the reviewer (ChatGPT) has no Gitea access.

## SHA Bindings

This review is bound to:
- Base: `92f1ed4d1ee4a79e75b1621d4e53aa4ed25b18c0`
- Head: `43610581f9ae69a9fd2541620fae7c2ada41f6cf`

Any change to the source branch after these SHAs invalidates this review.

## Correction Record

### v1 (PR #63)
- Initial compose with VIRTUAL_PORT 13378, expose 13378, healthcheck on /health
- **Blocked:** Wrong port/path in healthcheck, missing cache + test library

### v2 (PR #65 + #66)
- Fixed healthcheck to localhost:80/, expose: 80
- Added deployment evidence document
- **Blocked (review v2):** Cache path not explicit, test library missing, artifacts not accessible via GitHub

### v3 (PR #70 + #72)
- Fixed VIRTUAL_PORT: 13378 -> 80
- Added explicit cache bind-mount: /metadata/cache
- Added empty local test library: /audiobooks
- Updated contract tests to match

### Deployment Fixes (runtime, post-merge)
- Local bind target dirs created on Pi5 (missing initially -> mount error)
- Container healthy confirmed after PR #65 fix

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Image digest drift | Pinned by SHA256 digest, not tag |
| ARM64 incompatibility | Explicit `platform: linux/arm64` |
| Data loss | Persistent bind-mounts to HDD, database verified after restart |
| Unintended exposure | Internal Docker network only, no host ports |
| Credential leak | No secrets in compose or repo |

## Next Steps (post GH-58)

Per the child-issue graph in AUDIOBOOKSHELF.md:
1. GH-59: Reverse proxy / TLS — **done**
2. GH-60: OIDC authentication via Keycloak
3. NAS mount child issue: NFS bind for /audiobooks + /podcasts
