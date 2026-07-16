---
snapshot_version: gitea-epic-issue/v1
source: slarti/backlog#176
state: open
updated_at: 2026-07-14T00:35:49+02:00
labels:
  - "Systemarchitektur"
  - "epic"
  - "project:homelab-agenten-ausbau"
  - "ready"
publication: sanitized
---

# Disaster Recovery & Backup Resilience

# EPIC: Disaster Recovery & Backup Resilience

**Status:** Proposed / Planning
**Priority:** High
**Scope:** Homelab control plane: Pi5, Pi SSD, Pi microSD, and rechenknecht.

## Goal

The Homelab must be recoverable after a host, system disk, or storage failure without relying on memory, an intact Pi5, or a single local backup disk. Recovery must be documented, tested, and measurable.

## Recovery Objectives

Initial targets, to be confirmed during M0:

| Asset | Target RPO | Target RTO |
|---|---:|---:|
| Gitea repositories, issues, and configuration | 24 hours | 4 hours |
| Messenger, Eddie, Docker, and Pi service configuration | 24 hours | 4 hours |
| Paperless exports and metadata | 24 hours | 8 hours |
| Slarti/Lydia workspace, memory, and credentials inventory | 24 hours | 8 hours |
| rechenknecht compute host | 24 hours | 24 hours |

## Non-Negotiable Principles

- Apply 3-2-1-1-0: at least 3 copies, 2 storage media, 1 offsite copy, 1 protected or immutable copy where feasible, and 0 unverified restores.
- Encrypt every offsite backup before it leaves the LAN. Backup encryption keys and cloud credentials must not be stored only on the backed-up host.
- A backup is not complete until a documented restore verification succeeds.
- Do not use iCloud, Google, or Strato as the only recovery copy.
- Recovery runbooks must work from a replacement host and a printed or offline emergency copy.

## Current Baseline

- Pi5 keeps Paperless exports and Gitea dumps on `/mnt/hardDrive`; this is local only and shares the Pi failure domain.
- Current host cron backups: Paperless Francine at 01:00, Paperless NGX at 03:00, Gitea at 04:00.
- Pi root runs from microSD; `/mnt/hardDrive` is the Pi SSD.
- Eddie currently owns zero backup schedules.
- rechenknecht has its own root and RAID0 workspace storage, but no verified offsite DR copy is established here.

## Target Backup Topology

| Tier | Location | Purpose |
|---|---|---|
| Local fast restore | Pi SSD `/mnt/hardDrive` | Current Pi exports, Gitea dumps, service data. |
| LAN independent copy | rechenknecht `/mnt/raid0` | Encrypted mirror of Pi recovery set; protects against Pi, SSD, or microSD loss. |
| Offsite primary | Google Cloud storage via rclone/restic or equivalent | Encrypted, automated retention for recovery-critical data. |
| Offsite secondary | Strato WebDAV/SFTP storage via rclone/restic or equivalent | Independent encrypted copy of the critical recovery set. |
| Manual emergency archive | iCloud Drive | Small, encrypted recovery manifest, runbooks, key-location record, and periodic critical configuration export. Not an unattended primary backup target. |

M1 selects exact tooling and available capacities before bulk data is enabled. Google and Strato must be evaluated for API reliability, retention, cost, and restore bandwidth.

## Milestones

### M0: Inventory, Classification, and Threat Model

- Inventory all stateful data, secrets, Docker volumes, Git repositories, compose files, credentials, and recovery dependencies.
- Classify each item as rebuildable, restorable, or irreplaceable.
- Record owner, source host, size, RPO, RTO, backup inclusion, and restore destination.
- Define the encrypted key custody model, including an offline recovery copy held by Michael.
- Capture the baseline in a versioned DR inventory.

### M1: Backup Plans and Offsite Copies

- Define the canonical backup tool and encrypted repository layout.
- Add versioned backup manifests for Pi5 and rechenknecht.
- Keep existing Pi local exports/dumps until replacement jobs are proven.
- Replicate the Pi recovery set to rechenknecht and to both selected offsite targets.
- Back up Gitea repositories plus Gitea dump, Paperless exports plus configuration, messenger/Eddie/compose configuration, workspace/memory, and a credentials inventory without raw secrets.
- Configure retention, bandwidth limits, failure alerts, and log rotation.
- Produce a backup-location map: what is stored where, encrypted with which key reference, and when it was last verified.

**M1 acceptance tests**

- A fresh restore workspace can list and decrypt each repository.
- A sampled Gitea dump, Paperless export, and configuration archive restore successfully.
- At least one full Pi recovery set is retrievable from each offsite target without LAN access.
- Backup failure produces an actionable alert.

### M2: Pi5 Restore Runbooks

- Write and rehearse separate procedures for Pi hardware loss, Pi SSD loss, and microSD loss.
- Automate base OS bootstrap, Docker/Gitea/Paperless/messenger/Eddie deployment, and recovery validation where safe.
- Verify a replacement Pi can restore services from offsite data alone.

### M3: rechenknecht Restore Runbook

- Define rebuild steps for OS, users, workspace, memory, credentials recovery, Ollama models, and GPU services.
- Verify restoration to replacement hardware or a temporary recovery target.

### M4: Drills, Monitoring, and Continuous Improvement

- Run quarterly restore drills: one file-level, one service-level, and one host-level scenario.
- Monitor backup freshness, repository integrity, offsite reachability, free capacity, and restore-test age.
- Record actual RPO/RTO and revise the plan after every drill or incident.

## Emergency Handlungsanweisung

### First 15 Minutes: Any Incident

1. Do not repeatedly reboot, recreate containers, or run cleanup commands. Preserve the failed state if diagnostics are still reachable.
2. Record time, affected host, last known healthy service, and visible errors. Save `journalctl`, `dmesg`, Docker status, and disk status when possible.
3. Stop automatic jobs only if they can overwrite a good backup or worsen corruption. Do not delete volumes, queues, or backup archives.
4. Check the backup-location map and select the newest verified copy.
5. Declare the recovery mode and use the scenario below.

### Scenario A: Pi5 Hardware Failure

1. Do not attach or format the Pi SSD until its contents are copied or assessed read-only.
2. Prepare replacement Pi hardware and a new microSD boot disk.
3. Install the documented base OS and apply the Pi bootstrap runbook.
4. Attach the surviving Pi SSD read-only first; otherwise retrieve the latest encrypted recovery set from rechenknecht or offsite storage.
5. Restore Docker/Gitea/Paperless/messenger/Eddie in dependency order, then validate health endpoints and data counts.

### Scenario B: Pi SSD Failure (`/mnt/hardDrive`)

1. Stop write-heavy affected services to avoid repeated I/O failures.
2. Replace the SSD and create the documented filesystem/mount.
3. Restore Pi service data from the latest verified LAN or offsite recovery set.
4. Start services in dependency order and confirm Gitea, Paperless, messenger, Eddie, and backups.

### Scenario C: Pi microSD Failure

1. Preserve the Pi SSD; it contains the service data and must not be reformatted.
2. Flash a replacement microSD with the documented Pi base image.
3. Reapply bootstrap, mount the existing Pi SSD, and restore only root/configuration state needed for service startup.
4. Validate memory cgroups, Docker limits, persistent journald, networking, and backup jobs before declaring recovery complete.

### Scenario D: rechenknecht Failure

1. Do not depend on rechenknecht-hosted credentials or local workspace as the only recovery source.
2. Rebuild a replacement host from the documented OS and user bootstrap.
3. Restore workspace, memory, configuration, credentials through the key-custody process, then GPU/Ollama services.
4. Restore the Pi-to-rechenknecht backup mirror from offsite storage if the RAID0 data is lost.
5. Validate remote Pi integrations only after local services pass health checks.

## Definition of Done

- M1 through M4 are complete and each has a linked evidence record.
- Every listed failure scenario has a tested runbook and an owner.
- At least two independent encrypted offsite copies exist for the critical recovery set.
- A complete Pi and rechenknecht recovery drill has met or documented variance from the target RPO/RTO.
- The emergency handlungsanweisung and backup-location map are available offline to Michael.

## M1 Clarification: rechenknecht Service Source of Truth

rechenknecht is not part of the Eddie-only scheduler scope. It is, however, part of Disaster Recovery. Every rechenknecht service must have its deployable source of truth in a named Gitea repository, including its service definition, configuration template, dependency/version manifest, and recovery instructions. This explicitly includes OpenCode configuration, agents, skills, context, and the repositories that hold Slarti and Lydia operational knowledge. No production-only local configuration may be the sole copy of a rechenknecht service.

M1 must inventory each rechenknecht service and map it to its Gitea source repository. Because Gitea itself is hosted on the Pi5, M1 must also create encrypted offsite mirrors of those repositories and periodically verify a clone from the mirror. Gitea provides the canonical collaboration source, not the only disaster-recovery copy.
