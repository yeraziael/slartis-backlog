# Audiobookshelf — Requirements

Normative keywords: **MUST** / **MUST NOT** / **REQUIRED** / **SHALL** / **SHALL NOT** / **SHOULD** / **SHOULD NOT** / **RECOMMENDED** / **MAY** / **OPTIONAL** per RFC 2119.

## 1. Audiobook Serving and Playback

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-001 | Audiobookshelf **MUST** serve audiobooks and podcasts to authenticated users via web UI and mobile apps. | Confirmed | Confirmed — native capability |
| R-002 | The service **MUST** track playback progress per user. | Confirmed | Confirmed — native capability |
| R-003 | The service **MUST** support chapter navigation for chapterised audiobooks. | Confirmed | Confirmed — native capability |
| R-004 | The service **SHOULD** support variable playback speed. | Confirmed | Confirmed — native capability |
| R-005 | The service **SHOULD** support sleep timer. | Confirmed | Confirmed — native capability |
| R-006 | The service **MUST** support podcast RSS subscriptions. | Confirmed | Confirmed — native capability |

## 2. Multiple Libraries

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-010 | Audiobookshelf **MUST** maintain separate libraries for audiobooks and podcasts. | Confirmed | Confirmed — native capability |
| R-011 | Library configuration (paths, media type) **MUST** be backed by persistent configuration storage. | Confirmed | EPICS/media-platform contract |

## 3. User and Family Access

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-020 | Family members **MUST** be able to access Audiobookshelf through their personal Keycloak identity. | Confirmed | GH-60, confirmed in Homelab/Architecture PR #76 |
| R-021 | Guest users (read-only, no upload) **MUST** be supported. | Confirmed | GH-60, audiobookshelf-users group |
| R-022 | Admin users **MUST** have full management access. | Confirmed | GH-60, audiobookshelf-admins group |
| R-023 | The service **MUST** auto-provision local user accounts on first successful OIDC login. | Confirmed | GH-60 |
| R-024 | Auto-provisioning **MUST** apply group-based access control before creating a local account. | Confirmed | GH-60 |
| R-025 | The service **MUST NOT** create local accounts for unauthenticated or unauthorised users. | Confirmed | GH-60 |

## 4. Keycloak / OIDC Authentication

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-030 | Audiobookshelf **MUST** use Keycloak as its sole external identity provider. | Confirmed | GH-57, GH-60 |
| R-031 | OIDC Authorization Code Flow **MUST** be used. | Confirmed | GH-60 |
| R-032 | The OIDC client **MUST** be configured as a Confidential Client. | Confirmed | GH-60 |
| R-033 | Direct Access Grants **MUST** be disabled. | Confirmed | GH-60 |
| R-034 | Implicit Flow **MUST** be disabled. | Confirmed | GH-60 |
| R-035 | PKCE with S256 **SHOULD** be enabled. | Assumption | GH-60 documents that ABS 2.35.1 does not expose PKCE for web flow; mobile-only. Confirmed non-blocking. |
| R-036 | OIDC Discovery (`/.well-known/openid-configuration`) **MUST** be used if supported. | Confirmed | GH-60 |
| R-037 | HTTPS **MUST** be used for all OIDC endpoints, redirect URIs and logout endpoints. | Confirmed | GH-60 |
| R-038 | Internal container names or private HTTP endpoints **MUST NOT** be used as issuer or redirect targets. | Confirmed | GH-60 |

## 5. Authorisation and Role Mapping

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-040 | Keycloak group `audiobookshelf-users` **MUST** grant login access with read-only permissions. | Confirmed | GH-60 |
| R-041 | Keycloak group `audiobookshelf-admins** **MUST** grant full administrative access. | Confirmed | GH-60 |
| R-042 | Users without `audiobookshelf-users` **MUST** be denied access with an explicit error. | Confirmed | GH-60 |
| R-043 | `audiobookshelf-admins` membership alone **MUST NOT** grant login access. | Confirmed | GH-60 |
| R-044 | Group changes **MUST** take effect at the next successful login. | Confirmed | GH-60 |
| R-045 | Loss of `audiobookshelf-admins` **MUST** remove administrative rights at next login. | Confirmed | GH-60 |
| R-046 | Loss of `audiobookshelf-users` **MUST** prevent the next login attempt. | Confirmed | GH-60 |
| R-047 | The initial sole member of `audiobookshelf-admins` **MUST** be the Keycloak user Michael. | Confirmed | GH-60 |

## 6. Persistent Identity Binding

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-050 | Every local Audiobookshelf user **MUST** be persistently bound via the Keycloak `sub` claim. | Confirmed | GH-60 |
| R-051 | `preferred_username` **MUST** be used only as a display name, never as a stable primary key. | Confirmed | GH-60 |
| R-052 | A change of `preferred_username` in Keycloak **MUST NOT** create a second local account. | Confirmed | GH-60 |
| R-053 | Two different `sub` values **MUST NOT** map to the same local account. | Confirmed | GH-60 |
| R-054 | Existing local accounts **MUST NOT** be auto-linked to OIDC identities solely by username or email. | Confirmed | GH-60 |

## 7. Break-Glass Access

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-060 | A local `admin` user **MUST** be retained for break-glass access. | Confirmed | GH-57, GH-60 |
| R-061 | The `admin` account **MUST NOT** be bound to Keycloak. | Confirmed | GH-60 |
| R-062 | No other local production accounts **MUST** exist as parallel standard access. | Confirmed | GH-60 |
| R-063 | The break-glass password **MUST** be generated with at least 192 bits of entropy. | Confirmed | GH-60 |
| R-064 | The break-glass password **MUST** be delivered exactly once via Telegram to the operator. | Confirmed | GH-60 |
| R-065 | The password **MUST NOT** appear in any repository, log, CI output, or persistent configuration. | Confirmed | GH-60 |

## 8. Pi5 Resource Constraints

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-070 | The Docker container **MUST** be pinned to `linux/arm64`. | Confirmed | GH-58 |
| R-071 | Memory **MUST** be limited to 512 MB. | Confirmed | GH-58 |
| R-072 | CPU **MUST** be limited to 1.0 core. | Confirmed | GH-58 |
| R-073 | The container **MUST** use the restart policy `unless-stopped`. | Confirmed | GH-58 |
| R-074 | The container **MUST** run with `no-new-privileges`. | Confirmed | GH-58 |
| R-075 | Logging **SHOULD** be limited to 10 MB per file, 7 files max rotation. | Confirmed | GH-58 |

## 9. NAS-Backed Media Storage

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-080 | Audiobookshelf's media libraries **MUST** be served from NAS storage via NFS. | Confirmed | GH-57, AUDIOBOOKSHELF.md |
| R-081 | The NAS address **MUST** be `192.168.2.141`. | Confirmed | GH-57 |
| R-082 | The NAS protocol **MUST** be NFSv3. | Confirmed | GH-57, Homelab/Architecture PR #58 |
| R-083 | Media **MUST** be mounted read-only for the Audiobookshelf container. | Confirmed | GH-57, AUDIOBOOKSHELF.md |
| R-084 | Two NAS shares **MUST** be served: `audiobooks` and `podcasts`. | Confirmed | GH-57, Homelab/Architecture PR #60 |
| R-085 | Pi5 mount points **MUST** be `/mnt/ro/nas_audiobooks` and `/mnt/ro/nas_podcasts`. | Confirmed | GH-57 |
| R-086 | NFS mount options **SHOULD** use `rsize=8192,wsize=8192`. | Confirmed | GH-57 |
| R-087 | NFS mount implementation **MUST** be a separate child issue. | Confirmed | GH-57 |

## 10. Configuration Persistence

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-090 | Configuration data **MUST** be persisted on the Pi5 SSD (not NAS). | Confirmed | GH-58 |
| R-091 | The config volume **MUST** live at `/mnt/hardDrive/audiobookshelf/config/`. | Confirmed | GH-58 |
| R-092 | The metadata volume **MUST** live at `/mnt/hardDrive/audiobookshelf/metadata/`. | Confirmed | GH-58 |
| R-093 | Cache data (covers, images, items) **MUST** be persisted under `/metadata/cache/`. | Confirmed | GH-58 |
| R-094 | The config directory **MUST** contain the SQLite database `absdatabase.sqlite`. | Confirmed | GH-58 |
| R-095 | A test library **SHOULD** be available for integration testing. | Confirmed | GH-58, test library at `/mnt/hardDrive/audiobookshelf/testlibrary/` |

## 11. Secure Secret Handling

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-100 | The OIDC client secret **MUST** be provided as a runtime secret, never committed to version control. | Confirmed | GH-60 |
| R-101 | Configuration examples **MUST** use placeholders only. | Confirmed | GH-60 |
| R-102 | All evidence **MUST** be redacted for secrets, tokens, cookies and personal data before publication. | Confirmed | GH-60 |
| R-103 | Secrets **MUST NOT** appear in shell history, process arguments, logs, CI output, issues, PRs or comments. | Confirmed | GH-60 |
| R-104 | Secret rotation **MUST** be documented and tested. | Confirmed | GH-60 |

## 12. TLS-Only External Access

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-110 | All external access **MUST** be via HTTPS (TLS). | Confirmed | GH-59 |
| R-111 | HTTP **MUST** redirect to HTTPS automatically. | Confirmed | GH-59, via nginx-proxy acme-companion |
| R-112 | The TLS certificate **MUST** be obtained from Let's Encrypt. | Confirmed | GH-59, LETSENCRYPT_HOST + email webmaster@maier.wtf |
| R-113 | The public FQDN **MUST** be `audiobookshelf.hl.maier.wtf`. | Confirmed | GH-59, GH-77 |
| R-114 | WebSocket connections **MUST** be supported through the proxy. | Confirmed | GH-59, vhost.d Upgrade/Connection headers |

## 13. Backup and Restore

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-120 | Audiobookshelf configuration and database **MUST** be backed up regularly. | Confirmed | EPICS/media-platform, GH-62 |
| R-121 | Backup **MUST** include the SQLite database, metadata directory and any custom configuration. | Assumption | Derived from config persistence layout |
| R-122 | Restore procedure **MUST** be documented. | Confirmed | GH-62, EPICS/media-platform |
| R-123 | Media on NAS **MUST NOT** be backed up as part of Audiobookshelf backup (NAS has separate backup). | Assumption | NAS backup is a separate concern |
| R-124 | Backup **SHOULD** be automated and verifiable. | Confirmed | EPICS/media-platform dod.md: "Backup und Restore der Konfiguration sind dokumentiert" |

## 14. Monitoring and Health Checks

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-130 | A healthcheck **MUST** be configured on the container. | Confirmed | GH-58: `GET /status` → HTTP 200, interval 15s, timeout 10s, retries 5, start period 60s |
| R-131 | The healthcheck **MUST** use `http://localhost:80/status`. | Confirmed | GH-58, GH-59 |
| R-132 | The healthcheck **MUST** be available through the Docker runtime. | Confirmed | GH-58 |
| R-133 | Monitoring integration **SHOULD** be added to the Homelab monitoring system. | Open question | Not yet specified |

## 15. Deterministic Deployment

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-140 | Deployment **MUST** use Docker Compose as the sole mechanism. | Confirmed | GH-57, GH-58 |
| R-141 | The Compose file **MUST** be versioned in `Homelab/Architecture` under `pi/compose/audiobookshelf.yml`. | Confirmed | GH-58 |
| R-142 | The container image **MUST** be pinned by immutable digest. | Confirmed | GH-58, GH-59 |
| R-143 | No host port **MUST** be exposed; only internal Docker networking. | Confirmed | GH-58, GH-59 |
| R-144 | The container **MUST** join two networks: `audiobookshelf_internal` (internal) and `frontproxy_default` (external). | Confirmed | GH-59 |
| R-145 | Restart **MUST** preserve configuration, database and metadata. | Confirmed | GH-58 |

## 16. Metadata Quality

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-150 | Imported audiobooks **SHOULD** have correct title, author, series and cover art. | Confirmed | EPICS/media-platform: "Qualitaet, Benennung und Zielpfad geprueft" |
| R-151 | Metadata enrichment **SHOULD** be performed during import. | Confirmed | GH-57 architecture: child issue #12 "Metadaten-Anreicherung" |
| R-152 | The system **MUST** support manual metadata correction. | Assumption | Audiobookshelf native feature |

## 17. Duplicate Detection

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-160 | The import pipeline **MUST** detect duplicate audiobooks before writing to the library. | Confirmed | GH-57: uncertain matches → quarantine |
| R-161 | Detection **MUST** use content-based matching (not just filename). | Assumption | Desired behaviour, exact method not specified |
| R-162 | Matches below a confidence threshold **MUST** be placed in quarantine for manual review. | Confirmed | GH-57 |
| R-163 | A manual review workflow **MUST** exist for quarantined items. | Confirmed | GH-57 |

## 18. Import Safety

| ID | Requirement | Priority | Status |
|---|---|---|---|
| R-170 | Import **MUST** be idempotent — running the same import twice **MUST NOT** create duplicates. | Confirmed | GH-57 |
| R-171 | Source material **MUST** be preserved until normalisation is successful and the item is verified in the target library. | Confirmed | GH-57: "fino_behavior_forbidden" — deletion of source only after retention period |
| R-172 | Import **MUST** use a write pipeline separate from the read-only Audiobookshelf container. | Confirmed | GH-57: library_writer = "versioned_import_service_executed_by_lydia" |
| R-173 | Destructive source changes **MUST NOT** occur without separate authorisation. | Confirmed | GH-57 |
| R-174 | A replacement workflow **MUST** exist for re-importing already-normalised items. | Confirmed | GH-57: 9-step replacement workflow with retention period |

## 19. Open Questions

| ID | Question | Relevant To |
|---|---|---|
| Q-001 | What is the exact NFS export path on the QNAP NAS? | R-080 — R-087 |
| Q-002 | What is the NFS access control model on the NAS (IP allowlist, export options)? | R-080 — R-087 |
| Q-003 | Where will the import pipeline service run (Pi5, rechenknecht, separate container)? | R-170 — R-174 |
| Q-004 | What is the quarantine directory location? | R-162, R-163 |
| Q-005 | What is the retention period before source material is deleted after successful import? | R-171 |
| Q-006 | Which metadata provider(s) will be used for enrichment? | R-150, R-151 |
| Q-007 | How will the Homelab monitoring system be integrated? | R-133 |
| Q-008 | Will Audiobookshelf's built-in backup be used, or a custom solution? | R-120 — R-124 |
| Q-009 | What is the schedule for automated import runs? | R-170 — R-174 |
| Q-010 | How will the test library be populated for integration testing? | R-095 |
