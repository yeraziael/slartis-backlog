# Audiobookshelf — Security

## Threat Model

| Threat | Impact | Mitigation | Status |
|---|---|---|---|
| Unauthorised access to audiobook library | Data exposure (media files) | Keycloak OIDC, Authorization Code Flow, TLS | Deployed (proxy) / Pending (OIDC runtime) |
| Credential theft (OIDC client secret) | Attacker can impersonate Audiobookshelf to Keycloak | Confidential Client + runtime secret, no secret in version control | Planned |
| Session hijacking | Attacker can act as authenticated user | HTTPS-only, short access token lifetime | Deployed (TLS) |
| Token forgery | Attacker can mint fake identities | Token validation (issuer, signature, audience, expiry, `sub`) | Planned (OIDC runtime) |
| NAS unauthorised read | Access to media files outside Audiobookshelf | IP-allowlisted NFS export | Planned |
| Break-glass password compromise | Unrestricted local admin access | ≥ 192 bit entropy, single delivery via Telegram, offline storage | Planned |
| Denial of service (resource exhaustion) | Service unavailable | Docker resource limits (512 MB RAM, 1 CPU) | Deployed |
| Supply chain (compromised image) | Malicious code in container | Immutable digest pinning, `linux/arm64` platform pin | Deployed |
| Privilege escalation from container | Host compromise | `no-new-privileges:true`, no host port binding, internal-only network | Deployed |

## Security Boundaries

```
External (Internet)        ─── TLS 1.2+ ───→  Trust Boundary 1: Proxy
Trust Boundary 1: Proxy    ─── HTTP ────→    Trust Boundary 2: Application
Trust Boundary 2: App                        Internal Docker network only
       │                                          │
       ├── HTTPS ──→ Keycloak (OIDC)              │
       └── NFSv3 ──→ QNAP NAS (planned)           │
```

## Authentication

| Layer | Mechanism | Status |
|---|---|---|
| External access | HTTPS + Keycloak OIDC | Deployed (TLS) / Pending (OIDC) |
| Container → Keycloak | OIDC Authorization Code Flow, Confidential Client | Planned (scripts versioned) |
| Break-glass | Local password (≥ 192 bit entropy) | Planned |
| Docker runtime access | SSH key (Operator), Pi5 local access | Deployed |
| Internal healthcheck | None (HTTP internal-only) | Acceptable risk — no data exposure |

## Authorisation

See `requirements.md` §5 for the full role matrix and `contracts.md` §Keycloak OIDC Contract for obligations.

Summary:
- `audiobookshelf-users` → read-only guest access
- `audiobookshelf-admins` → full administrative access
- No `audiobookshelf-users` → access denied
- `audiobookshelf-admins` alone → access denied (must also be in `audiobookshelf-users`)

## Secret Management

| Secret | Storage | Rotation | Status |
|---|---|---|---|
| OIDC client secret | Docker runtime secret (not in version control) | Scripted via `rotate-keycloak-secret.sh` | Planned |
| Break-glass password | Offline (Operator) | Manual regeneration + Telegram delivery | Planned |
| Keycloak master realm key | Keycloak deployment | Keycloak-native | Deployed |
| TLS private key | acme-companion | Automatic (Let's Encrypt) | Deployed |

### Rules

Per `requirements.md` §11 (R-100 — R-104):
- R-100: OIDC client secret MUST be runtime secret, never committed.
- R-101: Configuration examples MUST use placeholders only.
- R-102: All evidence MUST be redacted before publication.
- R-103: Secrets MUST NOT appear in logs, CI, issues, PRs or comments.
- R-104: Secret rotation MUST be documented and tested.

## Break-Glass Security

Per `requirements.md` §7 (R-060 — R-065):

| Measure | Detail |
|---|---|
| Username | `admin` (not bound to Keycloak) |
| Password entropy | ≥ 192 bits |
| Generation | Cryptographically secure OS RNG |
| Delivery | Exactly once via Telegram, password only |
| Storage | Offline (Operator) |
| Repository | Never committed |
| Additional accounts | Zero — this is the only local account |

## Network Security

| Interface | Exposure | Protection |
|---|---|---|
| Public HTTPS (443) | Internet | TLS 1.2+, Let's Encrypt, frontproxy terminates |
| Internal HTTP (80) | Docker networks only | Unreachable from host or LAN |
| NFS (2049) | LAN (planned) | IP allowlist (assumed) |
| Healthcheck | Docker internal | No auth, no data exposure |
| Container → Keycloak | Homelab LAN | HTTPS, OIDC |

No host ports are bound. The container has no external network interface visible outside Docker.

## Security Verification

| Test | Method | Automated |
|---|---|---|
| OIDC token validation | Negative tests with invalid tokens | Planned |
| Authorisation enforcement | Login with wrong groups | Planned |
| Secret exposure scan | `scan-secrets` CI check | Deployed (repo-wide) |
| TLS certificate validity | `openssl s_client` | Manual |
| No host ports | `docker ps` port binding check | Manual (during deployment) |
| Break-glass access | Blackbox login test | Planned (via `verify-break-glass.sh`) |

## Known Open Security Questions

| ID | Question |
|---|---|
| S-001 | What is the NAS IP allowlist configuration? (Q-002 in requirements) |
| S-002 | Are there any additional Keycloak security measures needed beyond the Audiobookshelf client? (see #55) |
| S-003 | What is the access token lifetime configuration in Keycloak? |
| S-004 | Should the internal healthcheck endpoint be authenticated? |
