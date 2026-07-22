# Audiobookshelf — Operations

## Service Lifecycle

### Start Service

```bash
ssh pi5
cd /home/lydia/workspace/repos/home-repo
docker compose -f pi/compose/audiobookshelf.yml up -d
```

Expected result: Container healthy within ~8 s.

### Stop Service

```bash
docker compose -f pi/compose/audiobookshelf.yml down
```

### Restart Service

```bash
docker compose -f pi/compose/audiobookshelf.yml restart
```

### View Logs

```bash
docker compose -f pi/compose/audiobookshelf.yml logs -f
```

### Check Container Status

```bash
docker ps --filter name=audiobookshelf --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Expected output: `audiobookshelf   Up (healthy)   80/tcp`

## Health Check

| Parameter | Value |
|---|---|
| Endpoint | `GET http://localhost:80/status` |
| Expected | HTTP 200 |
| Container check | Docker healthcheck runs every 15 s |
| Manual check | `docker inspect --format='{{json .State.Health}}' audiobookshelf` |

### Health Status Interpretation

| Status | Meaning | Action |
|---|---|---|
| `healthy` | Service responding normally | None |
| `starting` | Container started, within start period | Wait up to 60 s |
| `unhealthy` | Healthcheck failed repeatedly | Check logs, restart container |

## Backup and Restore

### Backup Configuration and Database

```bash
# Manual backup
BACKUP_DIR="/mnt/hardDrive/backups/audiobookshelf/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -a /mnt/hardDrive/audiobookshelf/config "$BACKUP_DIR/"
cp -a /mnt/hardDrive/audiobookshelf/metadata "$BACKUP_DIR/"
```

### Restore Configuration and Database

```bash
# Stop the container
docker compose -f pi/compose/audiobookshelf.yml down

# Restore from backup
rm -rf /mnt/hardDrive/audiobookshelf/config
cp -a /path/to/backup/config /mnt/hardDrive/audiobookshelf/config
rm -rf /mnt/hardDrive/audiobookshelf/metadata
cp -a /path/to/backup/metadata /mnt/hardDrive/audiobookshelf/metadata

# Start the container
docker compose -f pi/compose/audiobookshelf.yml up -d
```

**Note:** Automated backup is planned but not yet implemented. See `backlog.md` for the backup issue.

## NFS Mount Operations (Planned)

### Mount NAS Shares

```bash
# audiobooks
mount -t nfs -o rsize=8192,wsize=8192,hard,intr,noatime 192.168.2.141:/path/to/audiobooks /mnt/ro/nas_audiobooks

# podcasts
mount -t nfs -o rsize=8192,wsize=8192,hard,intr,noatime 192.168.2.141:/path/to/podcasts /mnt/ro/nas_podcasts
```

### Verify Mount

```bash
mount | grep nas_audiobooks
ls /mnt/ro/nas_audiobooks
```

### Unmount

```bash
umount /mnt/ro/nas_audiobooks
umount /mnt/ro/nas_podcasts
```

**Note:** The exact NFS export path is an open question (Q-001). NFS mount implementation is a planned child issue.

## OIDC Operations (Planned)

### Setup Keycloak Client

```bash
# Run from Homelab/Architecture checkout on the machine with Keycloak admin access
bash pi/audiobookshelf/scripts/setup-keycloak.sh
```

### Apply Audiobookshelf OIDC Settings

```bash
# Apply OIDC configuration to Audiobookshelf
bash pi/audiobookshelf/scripts/apply-abs-settings.sh
```

### Rotate OIDC Client Secret

```bash
bash pi/audiobookshelf/scripts/rotate-keycloak-secret.sh
```

### Setup Break-Glass Admin

```bash
bash pi/audiobookshelf/scripts/break-glass-setup.sh
# Password is generated and sent via Telegram automatically
```

### Verify Break-Glass Access

```bash
bash pi/audiobookshelf/scripts/verify-break-glass.sh
```

## User Management

### Adding a New User

1. Operator adds the user to Keycloak.
2. Operator adds the user to the `audiobookshelf-users` group.
3. Optionally add to `audiobookshelf-admins` for admin rights.
4. User logs in via OIDC SSO — account is auto-provisioned.

### Removing a User

1. Operator removes the user from `audiobookshelf-users` in Keycloak.
2. User's next login attempt is denied.
3. Existing sessions expire at token TTL.

### Changing User Permissions

- Change Keycloak group membership.
- Takes effect at next user login.
- No manual action required in Audiobookshelf.

## Troubleshooting

| Symptom | Likely Cause | Check | Action |
|---|---|---|---|
| Container unhealthy | Healthcheck endpoint not responding | `docker logs audiobookshelf` | Restart container |
| 502 Bad Gateway | VIRTUAL_PORT mismatch | Verify compose proxy env vars | Correct VIRTUAL_PORT, recreate |
| Login fails | Keycloak unreachable | Check Keycloak container | Restart Keycloak |
| OIDC login error | Client secret wrong | Verify Docker runtime secret | Rotate secret |
| Media not visible | NAS mount missing | `mount \| grep nas` | Remount NFS share (planned) |
| Cannot access externally | DNS or proxy issue | `curl https://audiobookshelf.hl.maier.wtf/` | Check DNS, frontproxy, TLS cert |
| Podcast RSS not updating | Import scheduler not running | Check Eddie job queue | Trigger scan manually (planned) |
| High memory usage | Resource limit exceeded | `docker stats audiobookshelf` | Check container is within 512 MB limit |

## Maintenance Procedures

### Update Audiobookshelf Image

1. Pull new digest from `ghcr.io/advplyr/audiobookshelf`.
2. Update Compose file with new digest.
3. Backup config and metadata.
4. `docker compose -f pi/compose/audiobookshelf.yml pull`
5. `docker compose -f pi/compose/audiobookshelf.yml up -d`
6. Verify health.
7. Rollback by reverting digest and repeating.

### Periodic Tasks

| Task | Frequency | Actor | Status |
|---|---|---|---|
| Verify container healthy | Daily (visual) | Operator | Manual |
| Verify OIDC login works | Weekly | Operator | Manual |
| Verify break-glass access | Monthly | Operator | Manual |
| Rotate OIDC client secret | Quarterly | Operator | Planned |
| Check config volume disk usage | Weekly | Operator | Manual |
| Verify backup integrity | After each backup | Planned | Not implemented |
| Review quarantined items | Weekly | Operator | Not implemented |
| Test restore procedure | Quarterly | Operator | Not implemented |

## Incident Response

### Keycloak Unavailable

1. **Impact:** No new OIDC logins possible. Existing sessions continue until token expiry.
2. **Response:**
   - Check Keycloak container status.
   - Restart Keycloak if needed.
   - If extended outage expected, communicate to users.
3. **Break-glass:** Use local `admin` account (password via Telegram). See `contracts.md` §Break-Glass Procedure.

### NAS Unavailable

1. **Impact:** Media not accessible; Audiobookshelf may be slow or error.
2. **Response:**
   - Check NAS power and network.
   - Check NFS mount on Pi5 (`mount | grep nas`).
   - Remount if needed.
3. **Recovery:** Media becomes available automatically when NAS returns.

### Container Crash Loop

1. **Impact:** Service unavailable.
2. **Response:**
   - `docker logs audiobookshelf` to identify cause.
   - Check resource limits (memory, disk).
   - Restore from backup if database corrupted.
3. **Escalation:** If unable to recover, restore config + metadata from backup.

## Monitoring (Planned)

See `interfaces.md` §7 and `contracts.md` §Monitoring Contract for the full specification.

Current monitoring is limited to:
- Docker healthcheck (container level)
- Manual Docker status checks

Planned monitoring additions:
- Homelab integration for alerts (Telegram)
- Disk usage warnings
- NFS mount health
- Container restart tracking
