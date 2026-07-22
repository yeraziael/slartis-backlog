# Audiobookshelf — Decision Register

## Purpose

This register records architectural and planning decisions for the Audiobookshelf epic. It is **not** a substitute for Architecture Decision Records (ADRs). Cross-epic or Homelab-wide decisions belong in `docs/adrs/`. This register tracks decisions scoped to this epic.

Stable decision IDs are prefixed `ABDEC-`. Status values: `Accepted`, `Implemented`, `Proposed`, `Superseded`.

## Register

### ABDEC-001: Docker Compose on Pi5

| Field | Value |
|---|---|
| **Status** | Implemented |
| **Decision** | Deploy Audiobookshelf as a Docker Compose service on Raspberry Pi 5 |
| **Rationale** | Consistent with all other Homelab services; Pi5 is the designated Docker host |
| **Alternatives** | Native install (inconsistent), rechenknecht (wrong host) |
| **Consequences** | Compose in Homelab/Architecture, resource limits (512 MB RAM, 1 CPU) |
| **Source** | GH-57, GH-58 |
| **Related ADR** | None (Homelab-wide Docker standard) |

### ABDEC-002: Read-Only Media Access

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Decision** | Audiobookshelf reads media read-only. Import pipeline handles all writes |
| **Rationale** | Risk of corruption without separate write path; audit trail required |
| **Alternatives** | Direct write from ABS (no audit), manual copy (not scalable) |
| **Consequences** | Import pipeline is a separate component; 9-step replacement workflow; FINO forbidden |
| **Source** | GH-57, AUDIOBOOKSHELF.md (Homelab/Architecture) |
| **Related ADR** | None |

### ABDEC-003: Keycloak OIDC as Sole External IdP

| Field | Value |
|---|---|
| **Status** | Accepted (scripts versioned, runtime pending) |
| **Decision** | Keycloak is the sole external IdP. OIDC Authorization Code Flow with Confidential Client |
| **Rationale** | Homelab SSO standard; no alternative IdP available |
| **Alternatives** | Local accounts (inconsistent with SSO), LDAP (not available) |
| **Consequences** | `sub`-based binding, group role mapping, RP-Initiated Logout, break-glass `admin` retained |
| **Source** | GH-57, GH-60, Homelab/Architecture PR #76 |
| **Related ADR** | None |

### ABDEC-004: Pinned Image by Immutable Digest

| Field | Value |
|---|---|
| **Status** | Implemented |
| **Decision** | Container image pinned by SHA-256 digest, not version tag |
| **Rationale** | Reproducible deployments; no surprise updates |
| **Alternatives** | `:latest` tag (non-reproducible), version tag (mutable) |
| **Consequences** | Manual update process; current digest: `ghcr.io/advplyr/audiobookshelf@sha256:1eef6716...` |
| **Source** | GH-58, GH-59 |
| **Related ADR** | None |

### ABDEC-005: No Host Port Binding

| Field | Value |
|---|---|
| **Status** | Implemented |
| **Decision** | Container exposes port 80 internally only. All external access via frontproxy |
| **Rationale** | TLS termination, access control, reduced attack surface |
| **Alternatives** | Host port mapping (bypasses proxy) |
| **Consequences** | Two Docker networks (`frontproxy_default` + `audiobookshelf_internal`) |
| **Source** | GH-58, GH-59 |
| **Related ADR** | None |

### ABDEC-006: NAS Storage via NFSv3

| Field | Value |
|---|---|
| **Status** | Accepted (not yet implemented) |
| **Decision** | Media served from QNAP NAS (192.168.2.141) via NFSv3. Shares: `audiobooks`, `podcasts` |
| **Rationale** | NAS is the Homelab media store; NFSv3 is the Homelab NAS standard per STORAGE.md |
| **Alternatives** | NFSv4 (not standard), SMB (Linux complexity), local SSD (insufficient capacity) |
| **Consequences** | Separate NFS mount issue; read-only mount for ABS; NFS options `rsize=8192,wsize=8192` |
| **Source** | GH-57, Homelab/Architecture PRs #58, #60 |
| **Related ADR** | None |

### ABDEC-007: Import Pipeline as Separate Component

| Field | Value |
|---|---|
| **Status** | Accepted (not yet implemented) |
| **Decision** | Import pipeline is separate from ABS. Executed by Lydia. Handles normalisation, duplicate detection, quarantine |
| **Rationale** | ABS lacks built-in duplicate detection and metadata normalisation |
| **Alternatives** | Built-in upload (no quality control), manual import (not scalable) |
| **Consequences** | 10-stage pipeline defined; idempotency required; source preserved until verification; write path via separate NFS mount |
| **Source** | GH-57, AUDIOBOOKSHELF.md |
| **Related ADR** | None |

### ABDEC-008: Single Local Break-Glass Account

| Field | Value |
|---|---|
| **Status** | Accepted (scripts versioned, runtime pending) |
| **Decision** | Exactly one local `admin` account, not bound to Keycloak. No other local production accounts |
| **Rationale** | Access when Keycloak is unavailable; minimal local surface |
| **Alternatives** | No local accounts (no access if KC down), one per user (undermines SSO) |
| **Consequences** | Password ≥ 192 bit entropy, delivered once via Telegram, never in version control |
| **Source** | GH-57, GH-60 |
| **Related ADR** | None |
