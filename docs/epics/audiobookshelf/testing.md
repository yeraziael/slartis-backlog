# Audiobookshelf — Testing

## Test Strategy

Testing is structured in three layers:

1. **Architecture Tests** — versioned in `Homelab/Architecture`, execute against Compose files, scripts and configuration.
2. **Deployment Tests** — executed on the Pi5 after deployment, verify container health and connectivity.
3. **Acceptance Tests** — verify requirements from `requirements.md` manually or semi-automated.

All tests MUST be versioned. No secrets or passwords in test output.

## Architecture Tests

Versioned in `Homelab/Architecture`, executed in CI and locally.

### Compose Validation

| Test | Command | Expected |
|---|---|---|
| Compose config valid | `docker compose -f pi/compose/audiobookshelf.yml config` | Exit 0, valid YAML |
| Image pinned by digest | `grep -c '@sha256:' pi/compose/audiobookshelf.yml` | ≥ 1 |
| No host ports exposed | `grep -E 'ports:.*\d+:\d+' pi/compose/audiobookshelf.yml` | No match |
| ARM64 platform set | `grep 'linux/arm64' pi/compose/audiobookshelf.yml` | Match found |
| Resource limits present | `grep -E 'mem_limit|cpus' pi/compose/audiobookshelf.yml` | Both present |
| Healthcheck configured | `grep -c 'healthcheck' pi/compose/audiobookshelf.yml` | ≥ 2 sections |
| Internal network exists | `grep 'internal: true' pi/compose/audiobookshelf.yml` | Match found |

### Proxy Configuration Tests

See `docs/review/gh59-audiobookshelf-proxy-tls/TESTING.md` for full 27-assertion test suite.

Key assertions:

| Test | Expected |
|---|---|
| VIRTUAL_HOST set | `audiobookshelf.hl.maier.wtf` |
| VIRTUAL_PORT = 80 | `80` |
| Container joins `frontproxy_default` | Present in networks |
| Container joins `audiobookshelf_internal` | Present in networks |
| vhost.d `client_max_body_size 0` | Configured |
| vhost.d WebSocket Upgrade header | Configured |
| vhost.d WebSocket Connection header | Configured |

### OIDC Configuration Tests (Planned)

See `requirements.md` §4 and §5 for full specification.

| Test | Expected |
|---|---|
| Authorization Code Flow only | No DAG, no Implicit |
| Confidential Client | Client requires secret |
| Token validation enabled | Issuer, signature, audience, expiry checked |
| `sub`-based identity binding | Local user stored by `sub`, not username |
| Group-based access control | `audiobookshelf-users` required for login |
| Admin role mapping | `audiobookshelf-admins` → full admin |

### Secret Scan

| Test | Command | Expected |
|---|---|---|
| No secrets in repository | `scan-secrets` CI job | PASS |

### Link Check

| Test | Command | Expected |
|---|---|---|
| All internal links valid | `check-links` CI job | PASS |

### Git Diff Check

| Test | Command | Expected |
|---|---|---|
| No trailing whitespace, merge markers | `git diff --check` | PASS |

## Deployment Tests

Executed on Pi5 after deployment. Currently manual; automation is planned.

### Container Health

```bash
# Test 1: Container is running and healthy
docker ps --filter name=audiobookshelf --format "{{.Status}}" | grep -q "healthy"
# Expected: exit 0

# Test 2: Healthcheck endpoint responds
docker exec audiobookshelf node -e "
  require('http').get('http://localhost:80/status', r => {
    process.exit(r.statusCode === 200 ? 0 : 1)
  })
"
# Expected: exit 0

# Test 3: No host ports bound
docker port audiobookshelf
# Expected: empty output (no port mappings)
```

### Persistence

```bash
# Test 4: Config directory persists
test -f /mnt/hardDrive/audiobookshelf/config/absdatabase.sqlite
# Expected: file exists

# Test 5: Metadata directory persists
test -d /mnt/hardDrive/audiobookshelf/metadata
# Expected: directory exists

# Test 6: Restart preserves data
docker restart audiobookshelf
sleep 10
docker ps --filter name=audiobookshelf --format "{{.Status}}" | grep -q "healthy"
test -f /mnt/hardDrive/audiobookshelf/config/absdatabase.sqlite
# Expected: healthy, database file exists
```

## Acceptance Tests

These tests verify requirements from `requirements.md`. Status reflects current implementation.

### R-001 — R-006: Audiobook Serving

| Test | Requirement | Status |
|---|---|---|
| Web UI serves over HTTPS | R-001 | Deployed |
| Web UI login via OIDC | R-001 | Pending (GH-60) |
| Playback progress tracked per user | R-002 | Deployed (native) |
| Chapter navigation works | R-003 | Deployed (native) |
| Podcast RSS subscriptions work | R-006 | Deployed (native) |

### R-010 — R-011: Multiple Libraries

| Test | Requirement | Status |
|---|---|---|
| Audiobooks and podcasts in separate libraries | R-010 | Deployed (native) |
| Library config persists after restart | R-011 | Deployed |

### R-020 — R-025: User Access

| Test | Requirement | Status |
|---|---|---|
| User logs in via Keycloak OIDC | R-020 | Pending (GH-60) |
| Guest user has read-only access | R-021 | Pending (GH-60) |
| Admin user has full management | R-022 | Pending (GH-60) |
| Auto-provisioning on first login | R-023 | Pending (GH-60) |
| Unauthorised user denied at login | R-024 | Pending (GH-60) |
| No account for unauthorised user | R-025 | Pending (GH-60) |

### R-030 — R-038: OIDC Authentication

| Test | Requirement | Status |
|---|---|---|
| Login uses Authorization Code Flow | R-031 | Pending (GH-60) |
| OIDC Discovery used | R-036 | Pending (GH-60) |
| All OIDC endpoints use HTTPS | R-037 | Deployed (proxy) |

### R-040 — R-047: Authorisation

| Test | Requirement | Status |
|---|---|---|
| `audiobookshelf-users` → read-only | R-040 | Pending (GH-60) |
| `audiobookshelf-admins` → admin | R-041 | Pending (GH-60) |
| No group → access denied | R-042 | Pending (GH-60) |
| Admin group alone → access denied | R-043 | Pending (GH-60) |
| Group changes effective at next login | R-044 | Pending (GH-60) |
| Admin removal → no admin at next login | R-045 | Pending (GH-60) |
| User removal → login denied at next attempt | R-046 | Pending (GH-60) |

### R-050 — R-054: Identity Binding

| Test | Requirement | Status |
|---|---|---|
| User bound via `sub` claim | R-050 | Pending (GH-60) |
| Username change → no duplicate account | R-052 | Pending (GH-60) |
| Two different `sub` → two accounts | R-053 | Pending (GH-60) |

### R-060 — R-065: Break-Glass

| Test | Requirement | Status |
|---|---|---|
| `admin` account exists and works | R-060 | Pending (GH-60) |
| Break-glass login independent of Keycloak | R-061 | Pending (GH-60) |
| Password ≥ 192 bit entropy | R-063 | Pending (GH-60) |
| Password delivered once via Telegram | R-064 | Pending (GH-60) |
| No password in git, logs, CI | R-065 | Pending (GH-60) |

### R-070 — R-075: Pi5 Resources

| Test | Requirement | Status |
|---|---|---|
| Image platform linux/arm64 | R-070 | Deployed |
| Memory ≤ 512 MB | R-071 | Deployed |
| CPU ≤ 1.0 core | R-072 | Deployed |
| Restart policy unless-stopped | R-073 | Deployed |
| no-new-privileges set | R-074 | Deployed |
| Log rotation configured | R-075 | Deployed |

### R-080 — R-087: NAS Storage

All planned — not implemented.

### R-090 — R-095: Configuration Persistence

| Test | Requirement | Status |
|---|---|---|
| Config lives on Pi5 SSD at proper path | R-090, R-091 | Deployed |
| Metadata lives on Pi5 SSD at proper path | R-092 | Deployed |
| Cache under /metadata/cache/ | R-093 | Deployed |
| SQLite database present | R-094 | Deployed |
| Test library exists | R-095 | Deployed (empty) |

### R-100 — R-104: Secret Handling

| Test | Requirement | Status |
|---|---|---|
| No secrets committed to repo (via scan) | R-100 | Deployed (CI check) |
| No secrets in test output | R-102 | Deployed (manual) |

### R-110 — R-114: TLS

| Test | Requirement | Status |
|---|---|---|
| HTTPS works, HTTP redirects to HTTPS | R-110, R-111 | Deployed |
| Let's Encrypt certificate valid | R-112 | Deployed |
| FQDN resolves | R-113 | Deployed |
| WebSocket connections work | R-114 | Deployed |

### R-120 — R-124: Backup

All planned — not implemented.

### R-130 — R-133: Monitoring

| Test | Requirement | Status |
|---|---|---|
| Docker healthcheck configured and working | R-130 — R-132 | Deployed |

### R-140 — R-145: Deterministic Deployment

| Test | Requirement | Status |
|---|---|---|
| Compose file exists and valid | R-140, R-141 | Deployed |
| Image pinned by digest | R-142 | Deployed |
| No host ports | R-143 | Deployed |
| Two networks joined | R-144 | Deployed |
| Restart preserves data | R-145 | Deployed (verified) |

### R-150 — R-152: Metadata Quality

All planned — not implemented.

### R-160 — R-163: Duplicate Detection

All planned — not implemented.

### R-170 — R-174: Import Safety

All planned — not implemented.

## Verification Matrix (OIDC)

From GH-60 specification. To be executed after OIDC runtime deployment.

### Login

| # | Test | Expected |
|---|---|---|
| 1 | OIDC login with `audiobookshelf-users` member | Success, auto-provision, redirect to library |
| 2 | OIDC login without `audiobookshelf-users` | Access denied, error message |
| 3 | OIDC login with invalid redirect URI | Redirect denied |

### Auto-Provisioning

| # | Test | Expected |
|---|---|---|
| 4 | First login creates exactly one local user | One user created |
| 5 | Second login does not create duplicate | Same user, no duplicate |
| 6 | Username change still maps to same user | Same user, new display name |

### Authorisation

| # | Test | Expected |
|---|---|---|
| 7 | Guest user has read-only access | No upload/admin options visible |
| 8 | Admin user (Michael) has full admin | All admin functions available |
| 9 | Admin group removed → no admin at next login | Admin features not available |
| 10 | User group removed → login denied | Access denied |

### Logout

| # | Test | Expected |
|---|---|---|
| 11 | Logout ends local ABS session | Return to login page |
| 12 | Logout ends Keycloak SSO session | Keycloak login required again |
| 13 | Reload after logout stays unauthenticated | Login page remains |
| 14 | Different user can log in after logout | New user session starts |

### Restart

| # | Test | Expected |
|---|---|---|
| 15 | OIDC config survives container restart | Login still works |
| 16 | User permissions survive restart | Access rights unchanged |

### Secret Rotation

| # | Test | Expected |
|---|---|---|
| 17 | New secret works after rotation | Login successful |
| 18 | Old secret no longer works | Login fails |

### Break-Glass

| # | Test | Expected |
|---|---|---|
| 19 | Local `admin` login works (independent of Keycloak) | Full admin access |
| 20 | No password leakage in evidence | Password not visible |

### Security Negative Tests

| # | Test | Expected |
|---|---|---|
| 21 | Expired token rejected | Login denied |
| 22 | Wrong issuer rejected | Login denied |
| 23 | Wrong audience rejected | Login denied |
| 24 | Invalid signature rejected | Login denied |
| 25 | Missing `sub` rejected | Login denied |
| 26 | No allowed group rejected | Login denied |
