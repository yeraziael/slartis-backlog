# Audiobookshelf — Architecture Decision Records

## ADR-001: Docker Compose on Pi5

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Source** | GH-57, GH-58 |
| **Date** | 2026-07-20 |

**Decision:** Deploy Audiobookshelf as a Docker Compose service on the Raspberry Pi 5.

**Alternatives considered:**
- Native installation on Pi5 — rejected: inconsistent with Homelab Docker standard.
- Deployment on rechenknecht — rejected: rechenknecht is not a Docker service host.

**Consequences:**
- Consistent with all other Homelab services.
- Compose file versioned in `Homelab/Architecture`.
- Resource limits (512 MB RAM, 1 CPU) enforced via Docker.

---

## ADR-002: Read-Only Media Access

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Source** | GH-57, AUDIOBOOKSHELF.md (Homelab/Architecture) |
| **Date** | 2026-07-20 |

**Decision:** Audiobookshelf accesses media read-only. A separate import pipeline (executed by Lydia) handles all write operations.

**Alternatives considered:**
- Audiobookshelf writes directly to media directory — rejected: risk of corruption, no audit trail.
- Manual file copy — rejected: not scalable, no duplicate detection.

**Consequences:**
- Import pipeline is a separate component with its own issue.
- 9-step replacement workflow with retention period defined.
- FINO behaviour (delete source on import) explicitly forbidden.

---

## ADR-003: Keycloak OIDC as Sole External Identity Provider

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Source** | GH-57, GH-60, Homelab/Architecture PR #76 |
| **Date** | 2026-07-20 |

**Decision:** Keycloak is the sole external identity provider. Audiobookshelf uses OIDC Authorization Code Flow with a Confidential Client.

**Alternatives considered:**
- Local accounts for all users — rejected: inconsistent with Homelab SSO standard.
- LDAP integration — rejected: not available in Homelab.
- OIDC with Public Client — rejected: less secure than Confidential Client.

**Consequences:**
- Stable identity binding via `sub` claim (not username or email).
- Role mapping via Keycloak groups (`audiobookshelf-users`, `audiobookshelf-admins`).
- RP-Initiated Logout for full SSO session termination.
- Break-glass `admin` account retained for Keycloak-unavailable scenarios.

---

## ADR-004: Pinned Image by Immutable Digest

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Source** | GH-58, GH-59 |
| **Date** | 2026-07-20 |

**Decision:** Pin the Audiobookshelf container image by its immutable SHA-256 digest, not by a version tag.

**Alternatives considered:**
- `:latest` tag — rejected: non-reproducible.
- Semantic version tag (e.g. `:2.19.0`) — accepted during development, but final deployment must use digest.

**Consequences:**
- Reproducible deployments across environments.
- Manual image update process (update digest, test, deploy).
- Current pinned digest: `ghcr.io/advplyr/audiobookshelf@sha256:1eef6716183c52abafe5405e7d6be8390248ecd59c7488c44af871757ac8fc4d`.

---

## ADR-005: No Host Port Binding

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Source** | GH-58, GH-59 |
| **Date** | 2026-07-20 |

**Decision:** The Audiobookshelf container exposes port 80 internally only. No `ports:` mapping to the host. All external access goes through the frontproxy (nginx-proxy + acme-companion).

**Alternatives considered:**
- Host port mapping with direct access — rejected: bypasses proxy, TLS, and access control.
- Host port mapping behind proxy — rejected: unnecessary attack surface.

**Consequences:**
- Container joins `frontproxy_default` network for ingress.
- Container has its own `audiobookshelf_internal` (internal: true) network for isolation.
- Healthcheck runs on internal port 80.

---

## ADR-006: NAS Storage via NFSv3

| Field | Value |
|---|---|
| **Status** | Accepted (not yet implemented) |
| **Source** | GH-57, Homelab/Architecture PRs #58, #60 |
| **Date** | 2026-07-20 |

**Decision:** Media is served from the QNAP NAS (192.168.2.141) via NFSv3. Two shares: `audiobooks` and `podcasts`.

**Alternatives considered:**
- NFSv4 — rejected: STORAGE.md documents NFSv3 as Homelab standard.
- SMB/CIFS — rejected: NFS is simpler for Linux-only serving.
- Local SSD storage — rejected: insufficient capacity for media library.

**Consequences:**
- NFS mount is a separate child issue (not yet implemented).
- Mount points: `/mnt/ro/nas_audiobooks`, `/mnt/ro/nas_podcasts`.
- NFS options: `rsize=8192,wsize=8192,hard,intr,noatime`.
- Media mounted read-only for Audiobookshelf container.

---

## ADR-007: Import Pipeline as Separate Component

| Field | Value |
|---|---|
| **Status** | Accepted (not yet implemented) |
| **Source** | GH-57, AUDIOBOOKSHELF.md |
| **Date** | 2026-07-20 |

**Decision:** The import pipeline is a separate component from Audiobookshelf. It handles metadata normalisation, duplicate detection, quarantine and library writes. Executed by Lydia.

**Alternatives considered:**
- Audiobookshelf built-in upload — rejected: no duplicate detection, no metadata normalisation, no quarantine workflow.
- Manual import by operator — rejected: not scalable.

**Consequences:**
- 10-stage pipeline defined (Ingest → Analyse → Normalise → Duplicate Check → Quarantine/Library Write → Verify → Scan Trigger → Retention → Delete Source).
- Source material preserved until successful normalisation verified.
- Idempotency required.
- Write access to NAS via separate NFS path (rw, not ro).

---

## ADR-008: Single Local Break-Glass Account

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Source** | GH-57, GH-60 |
| **Date** | 2026-07-20 |

**Decision:** Exactly one local account `admin` is retained for break-glass access. It is not bound to Keycloak. No other local production accounts exist.

**Alternatives considered:**
- No local accounts — rejected: no access if Keycloak is unavailable.
- One local account per family member — rejected: undermines SSO purpose.
- Local accounts with same permissions as OIDC — rejected: break-glass should be minimal.

**Consequences:**
- `admin` has full administrative rights.
- Password ≥ 192 bit entropy, delivered once via Telegram.
- Password never stored in version control.
- Password rotation requires manual Telegram delivery.

---

## Superseded Decisions

| ADR | Decision | Superseded By | Reason |
|---|---|---|---|
| CWAuto OIDC Fork | Fork Calibre-Web Automated for OIDC support | Upstream Generic-OAuth Provider (ADR 0001 in docs/adr/) | Upstream v4.0.6+ has built-in OIDC via `metadata_url` |
