# Audiobookshelf — Contracts

## Service Contract — Audiobookshelf to Homelab Infrastructure

### Service Level

| Parameter | Target | Measured By |
|---|---|---|
| Availability | > 99% (planned, not yet measured) | Docker healthcheck uptime |
| Startup time | < 15 s to healthy | Docker healthcheck start period |
| Restart recovery | < 10 s to healthy | Docker restart + healthcheck |
| Response time (web UI) | < 2 s (LAN) | User observation (not yet instrumented) |
| Response time (media streaming) | LAN-dependent | User observation |

### Resource Commitment

| Resource | Limit | Source |
|---|---|---|
| Memory | 512 MB (hard limit) | Docker `mem_limit` |
| CPU | 1.0 core | Docker `cpus` |
| Persistent storage (config) | ~100 MB (SQLite database) | Observed during GH-58 |
| Persistent storage (metadata) | ~1 GB (cache, covers, images) | Estimated |
| Persistent storage (test library) | 0 bytes (empty) | Current state |

### Data Durability

| Data | Location | Durability | Backup |
|---|---|---|---|
| SQLite database (users, state, config) | Pi5 SSD, `/mnt/hardDrive/audiobookshelf/config/` | SSD reliability | Planned, not implemented |
| Metadata cache (covers, images) | Pi5 SSD, `/mnt/hardDrive/audiobookshelf/metadata/` | SSD reliability | Regenerable from media |
| Media files | QNAP NAS (via NFS, planned) | NAS RAID | NAS-level backup |
| OIDC client secret | Docker runtime secret | Operator-managed | Rotated, not backed up |

---

## Keycloak OIDC Contract

### Identity Provider Obligations

Keycloak MUST:

- Serve the `audiobookshelf` Confidential Client with valid OIDC configuration.
- Publish correct `issuer`, JWKS, authorization, token and `end_session` endpoints.
- Return the `groups` claim with `audiobookshelf-users` and/or `audiobookshelf-admins` group membership.
- Return a stable, immutable `sub` claim for every user.
- Respect token expiry, refresh token rotation and session revocation.
- Accept RP-Initiated Logout via `id_token_hint` + `post_logout_redirect_uri`.

### Audiobookshelf OIDC Obligations

Audiobookshelf MUST:

- Validate the issuer, audience, signature, `exp` and `nbf` of every ID token.
- Bind every local user account exclusively via the `sub` claim.
- Reject logins from users without the `audiobookshelf-users` group claim.
- Map `audiobookshelf-admins` group membership to full administrative rights.
- Enforce read-only access for users without `audiobookshelf-admins`.
- Re-evaluate group membership at every login (no session-cached permissions beyond token lifetime).
- Perform RP-Initiated Logout when the user clicks the logout button.
- Preserve exactly one local break-glass account `admin` that is not bound to Keycloak.

### Security Constraints

| Constraint | Enforced By |
|---|---|
| Authorization Code Flow only (no Implicit, no DAG) | Keycloak client config + ABS OIDC config |
| Confidential Client with Client Secret | Keycloak client config + Docker runtime secret |
| HTTPS-only for all OIDC endpoints | Architecture (DNS + proxy) |
| No wildcard redirect URIs | Keycloak client config |
| No `*` as Web Origin | Keycloak client config |
| Client secret never in version control | Deployment policy |
| Token validation never disabled | ABS OIDC configuration |

---

## Front Proxy Contract

### Reverse Proxy Obligations

nginx-proxy (frontproxy) MUST:

- Terminate TLS for `audiobookshelf.hl.maier.wtf` using Let's Encrypt certificates.
- Forward `VIRTUAL_PORT=80` traffic to the Audiobookshelf container.
- Support WebSocket upgrade by forwarding `Upgrade` and `Connection` headers.
- Allow unlimited upload body size (`client_max_body_size 0`).
- Redirect HTTP → HTTPS automatically.

### Audiobookshelf Obligations

Audiobookshelf MUST:

- Listen on port 80 (internal).
- Return HTTP 200 on `GET /status`.
- Join the `frontproxy_default` Docker network.
- Set the environment variables `VIRTUAL_HOST`, `VIRTUAL_PORT`, `LETSENCRYPT_HOST`, `LETSENCRYPT_EMAIL`.

### Network Topology

```
Client → Internet → [TLS] → frontproxy (port 443)
     → [HTTP, Docker internal] → Audiobookshelf (port 80)
```

No host port is bound. The container is reachable only via the frontproxy network.

---

## NAS / NFS Contract (Planned)

### NAS Obligations

The QNAP NAS MUST:

- Export the `audiobooks` share via NFSv3, readable by the Pi5 IP address.
- Export the `podcasts` share via NFSv3, readable by the Pi5 IP address.
- Maintain stable export paths and availability.
- Provide consistent file listing performance for read-only media access.

### Pi5 Host Obligations

The Pi5 host MUST:

- Mount both NFS shares at `/mnt/ro/nas_audiobooks` and `/mnt/ro/nas_podcasts`.
- Use NFS options `rsize=8192,wsize=8192,hard,intr,noatime`.
- Remount shares automatically on reboot (via fstab or equivalent).
- Bind the host mounts into the Audiobookshelf container as read-only volumes.

### Audiobookshelf Obligations

Audiobookshelf MUST:

- Treat `/media/audiobooks` and `/media/podcasts` as read-only media sources.
- Never attempt to write to media directories.
- Index media through library configuration, not filesystem write access.

---

## Import Pipeline Contract (Planned)

### Guarantees

| Guarantee | Description |
|---|---|
| **Idempotency** | Running the import twice with the same source MUST NOT create duplicates. |
| **Non-destructive** | Source material MUST be preserved until normalisation is verified in the target library. |
| **Content-based matching** | Duplicate detection MUST use content (hash, metadata) not just filename. |
| **Quarantine** | Uncertain matches MUST be placed in quarantine for operator review. |
| **Preservation** | Source material SHALL NOT be deleted until a retention period expires after successful normalisation. |
| **Atomicity** | Each import batch is self-contained; partial failures do not corrupt the library. |

### Pipeline Stages

```
Source Media → 1. Ingest → 2. Analyse → 3. Normalise
     → 4. Duplicate Check → 5. Quarantine (if match < threshold)
                           → 6. Library Write (if match > threshold)
     → 7. Verify → 8. Trigger Library Scan → 9. Retention Timer
     → 10. Delete Source (after retention period)
```

### Roles

| Role | Responsibility |
|---|---|
| Import pipeline | Execute stages 1–10 deterministically |
| Quarantine reviewer (Operator) | Review uncertain matches, accept or reject |
| Audiobookshelf | Serve normalised media, index via library scan |

### Failure Modes

| Failure | Behaviour |
|---|---|
| Duplicate detection fails | Duplicate enters library → manual operator cleanup |
| Import pipeline crashes mid-batch | Idempotent retry on next run; no data loss |
| NAS write fails | Pipeline stops, reports error, preserves source |
| Quarantine fills unchecked | Operator notified via Telegram (planned) |

---

## Backup Contract (Planned)

### Obligations

The backup system MUST:

- Back up the `config/` directory (SQLite database) daily.
- Back up the `metadata/` directory daily.
- Verify backup integrity after each run.
- Support point-in-time restore of configuration and metadata.
- Exclude NAS media files (backed up at NAS level).
- Document restore procedure in the operations runbook.

### Retention

| Backup Type | Retention | Target |
|---|---|---|
| Daily config + metadata | 7 days | Pi5 local or NAS |
| Weekly config + metadata | 4 weeks | NAS |
| Monthly config + metadata | 12 months | NAS |

### Restore Test

The restore procedure MUST be tested at least once per quarter. Test evidence MUST include:

- Successful database restore.
- Successful metadata cache rebuild.
- Functional login and library access after restore.

---

## Monitoring Contract (Planned)

### Obligations

The monitoring system MUST:

- Check container health every 5 minutes via Docker healthcheck.
- Alert on unhealthy container status for > 1 minute.
- Alert on container restart count > 3 in 5 minutes.
- Alert on config volume disk usage > 90%.
- Alert on NFS mount failure (once implemented).
- Integrate with the existing Homelab alerting channel (Telegram, planned).

### Healthcheck Contract

| Parameter | Value |
|---|---|
| Interval | 15 s |
| Timeout | 10 s |
| Retries | 5 |
| Start period | 60 s |
| Healthy after | ~8 s (observed) |

---

## Service Account Contracts

### Lydia (Execution Agent)

| Permission | Scope |
|---|---|
| Execute import pipeline | Write to NAS library directory |
| Deploy Docker service | `docker compose up -d` on Pi5 |
| Configure runtime secrets | Place OIDC client secret as Docker secret |
| Trigger library scan | POST to Audiobookshelf internal API |
| Read container status | `docker ps`, `docker inspect` |

### Slarti (Control Plane Agent)

| Permission | Scope |
|---|---|
| Read-only repository access | Homelab/Architecture |
| Plan and review | This epic and its child issues |
| Version compose configuration | Homelab/Architecture pi/compose/ |
| No runtime access | Never executes deployment commands |

### Eddie (Merge Authority)

| Permission | Scope |
|---|---|
| Merge PRs in Homelab/Architecture | After approval |
| No runtime access | Deployment delegated to Lydia |

---

## OIDC Secret Lifecycle

### Creation

1. Operator runs `setup-keycloak.sh` which creates the Keycloak client.
2. The script outputs the client secret to stdout (not stored).
3. Operator places the secret as a Docker runtime secret on Pi5.
4. Operator verifies OIDC login works with the new secret.

### Rotation

1. Operator runs `rotate-keycloak-secret.sh`.
2. Keycloak generates a new client secret.
3. The new secret is placed as a Docker runtime secret.
4. Audiobookshelf is restarted or config reloaded.
5. OIDC login is verified with the new secret.
6. The old secret is verified to no longer work.

### Revocation

- Disable the Keycloak `audiobookshelf` client.
- All active sessions continue until token expiry (AT: short, RT: longer).
- After token expiry, no new logins possible.
- Break-glass `admin` account remains available.

---

## Break-Glass Procedure (Contract)

### When to Use

Keycloak is unavailable, OIDC configuration is broken, or the Operator cannot authenticate via Keycloak.

### Procedure

1. Access Audiobookshelf at the local or internal URL.
2. Click "Log in with password" (not SSO).
3. Enter username `admin` and the offline password.
4. Perform required recovery or troubleshooting.
5. After recovery, verify Keycloak OIDC login works again.

### Password Management

- Password is generated once with ≥ 192 bit entropy.
- Delivered exactly once via Telegram to the Operator (no context, just the password).
- Operator stores the password offline.
- Password may be rotated by generating a new one and repeating delivery.
- No record of the password exists in any digital system.

---

## Interface Versioning

| Interface | Version Control Location | Versioning Scheme |
|---|---|---|
| Compose file | `Homelab/Architecture pi/compose/audiobookshelf.yml` | Git commit SHA |
| Proxy config | `Homelab/Architecture pi/compose/` (env vars + vhost.d) | Git commit SHA |
| OIDC client | Keycloak admin UI (scripted via `setup-keycloak.sh` in `Homelab/Architecture`) | Git commit SHA |
| Architecture doc | `Homelab/Architecture docs/AUDIOBOOKSHELF.md` | Git commit SHA |
| This epic | `yeraziael/slartis-backlog docs/epics/audiobookshelf/` | Git commit SHA |
| Keycloak realm | Keycloak admin UI / versioned export | Export file in repo |
| Backup/restore script | Not yet versioned | TBD |

All versioned artifacts in `Homelab/Architecture` are reviewed via Gitea PR and approved via ACP review process before merge.
