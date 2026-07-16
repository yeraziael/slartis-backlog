---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#69
state: closed
updated_at: 2026-06-30T22:08:17+02:00
is_epic: false
labels:
  []
publication: sanitized
---

# M2 Blackbox Tests (Issue #54)

## Kontext

M2 Resilience R1-R7 wurde implementiert (Commits `724483d`, `464ec87`), aber die laufende Service-Instanz hatte noch den alten Code ohne Queue-Integration. Nach Reboot + Deploy müssen diese Tests durchgeführt werden.

## Post-Reboot Setup

```bash
# 1. Queues-Verzeichnis anlegen
mkdir -p <home>/home-repo/runtime/state/queues

# 2. Service neustarten
sudo systemctl restart lydia-messenger@lydia

# 3. Log prüfen auf RECOVERY-Meldungen
journalctl -u lydia-messenger@lydia --since "1 min ago" | grep -i recovery

# 4. Task-Loop aktiv?
systemctl status lydia-messenger@lydia
```

## Blackbox-Tests

### Test 1: Worker Dispatch (vollständig automatisiert)

**Erwartung:** Worker-Task → Queue → GPU-Lock → Ollama → Ergebnis-Post

```bash
curl -s -X POST \
  -H "Authorization: <credential-redacted>" \
  -H "Content-Type: application/json" \
  "<internal-gitea-reference> \
  -d '{
    "title": "BB-1: Worker Dispatch",
    "body": "worker {\"task\":\"write test_bb1.py\",\"output_path\":\"<home>/tmp/test_bb1.py\",\"model\":\"qwen2.5-coder:7b-instruct\",\"requires_gpu\":true}"
  }'
```

Check:
- [ ] Issue wird von Task-Loop auf `✅ Executed` gesetzt und geschlossen
- [ ] Issue hat WORKER RESULT Kommentar (success/failed + Output)
- [ ] `<home>/tmp/test_bb1.py` existiert
- [ ] Worker-Queue ist leer: `jq ".queue | length" <home>/home-repo/runtime/state/queues/worker-queue.json`
- [ ] GPU-Lock ist frei: `test ! -f /tmp/lydia-gpu.lock && echo "frei"`

---

### Test 2: GPU-Blockade (manuell, 2 Terminals)

**Erwartung:** GPU-Task bleibt in Queue, wenn GPU belegt ist → wird nach Freigabe ausgeführt

**Terminal 1 — GPU blockieren:**
```bash
echo '{"pid":999999,"type":"ollama","task_id":"bb2-block","acquired_at":0}' > /tmp/lydia-gpu.lock

source <home>/home-repo/runtime/hardening/gpu_lock.sh
gpu_is_free && echo "frei" || echo "belegt"
```

**Terminal 2 — GPU-Task enqueuen:**
```bash
curl -s -X POST \
  -H "Authorization: <credential-redacted>" \
  -H "Content-Type: application/json" \
  "<internal-gitea-reference> \
  -d '{
    "title": "BB-2: GPU Blockade",
    "body": "worker {\"task\":\"write test_bb2.py\",\"output_path\":\"<home>/tmp/test_bb2.py\",\"model\":\"qwen2.5-coder:7b-instruct\",\"requires_gpu\":true}"
  }'
```

Check:
- [ ] Issue wird von Task-Loop auf `✅ Executed` gesetzt
- [ ] Worker-Task bleibt in Queue: `jq ".queue | length" <home>/home-repo/runtime/state/queues/worker-queue.json`
- [ ] `gpu_busy` Flag ist true: `jq ".gpu_busy" <home>/home-repo/runtime/state/queues/worker-queue.json`

**GPU freigeben (Terminal 1):**
```bash
rm /tmp/lydia-gpu.lock
# Warten auf Poll (15s)
```

Check nach 30s:
- [ ] Worker-Queue ist leer
- [ ] WORKER RESULT Kommentar im Issue
- [ ] `<home>/tmp/test_bb2.py` existiert

---

### Test 3: Retry (vollständig automatisiert)

**Erwartung:** Worker failt → Retry-Queue (1min Backoff) → max 4 Versuche → endgültig failed

```bash
curl -s -X POST \
  -H "Authorization: <credential-redacted>" \
  -H "Content-Type: application/json" \
  "<internal-gitea-reference> \
  -d '{
    "title": "BB-3: Retry",
    "body": "worker {\"task\":\"write test_bb3.py mit Code der nie akzeptiert wird\",\"output_path\":\"<home>/tmp/test_bb3.py\",\"model\":\"qwen2.5-coder:7b-instruct\",\"requires_gpu\":true}"
  }'
```

Check nach 15s:
- [ ] Erster Versuch gestartet (task_state.db: running→failed)
- [ ] Retry-Queue hat 1 Eintrag: `jq ". | length" <home>/home-repo/runtime/state/queues/retry-queue.json`

Check nach 20 min:
- [ ] Max 4 Versuche erreicht
- [ ] WORKER RESULT "failed" im Issue
- [ ] Retry-Queue leer (cleanup)

---

### Test 4: Crash Recovery (manuell, SSH)

**Erwartung:** Nach kill + Restart: stale running→failed, GPU-Lock cleaned, Flags resettet

```bash
# 1. Task-Loop killen:
sudo kill $(cat /tmp/lydia-task-loop.lock)
ps aux | grep task_loop | grep -v grep || echo "tot"

# 2. Stale Einträge simulieren:
echo "bb4-crash|running|1000|||0" >> <home>/home-repo/runtime/state/task_state.db
echo '{"pid":999999,"type":"ollama","task_id":"zombie","acquired_at":0}' > /tmp/lydia-gpu.lock

# 3. Service neustarten:
sudo systemctl restart lydia-messenger@lydia

# 4. Recovery-Logs prüfen:
journalctl -u lydia-messenger@lydia --since "30 sec ago" | grep RECOVERY
```

Erwartete RECOVERY-Meldungen:
- [ ] `cleaned stale GPU lock`
- [ ] `marked 1 stale running tasks as failed`
- [ ] `reset stale gpu_busy + running flags`
- [ ] `queues initialized, retry queue processed`

## Fehlerdiagnose

| Symptom | Ursache | Check |
|---------|---------|-------|
| Issue wird nicht geschlossen | Task-Loop läuft nicht | `systemctl status lydia-messenger@lydia` |
| "✅ Executed" aber kein RESULT | Worker-Scheduler läuft nicht | `journalctl | grep scheduler` |
| GPU-Lock ewig | Stale PID | `cat /tmp/lydia-gpu.lock | jq .pid` → `kill -0` |
| Queue voll | running=true blockt | `jq .running <home>/home-repo/runtime/state/queues/worker-queue.json` |

## Referenzen

- Commits: `724483d` (R1-R7), `464ec87` (Trap-Cleanup)
- Unit-Tests: `runtime/tests/test_resilience.sh` — 51/51 PASS
- Architektur: `docs/RESILIENCE.md`
- Design Rules: `docs/DESIGN_RULES.md` Rule 6
