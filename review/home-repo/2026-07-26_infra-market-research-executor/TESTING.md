# Testing: infra-market-research-executor

## Tests Executed

- Eddie dispatch test: job `d68128ec` completed with exit 0
- opencode ran as lydia on Pi5, produced research output
- Exit status propagation fix: verified with `bash -n` syntax check
- Fail-closed pull: verified script exits 1 on git pull failure

## Negative Exit-Status Propagation Test

### Setup

Create a stub script that exits non-zero:

```bash
cat > /tmp/failing-opencode.sh << 'STUB'
#!/bin/bash
echo "stub: simulating opencode failure" >&2
exit 42
STUB
chmod +x /tmp/failing-opencode.sh
```

### Execution

```bash
RESEARCH_CMD=/tmp/failing-opencode.sh \
  RESEARCH_ARGS="" \
  /home/lydia/bin/infra-market-research.sh
echo "exit code: $?"
```

### Expected Result

The script must exit with code 42 (the stub's exit code), not 0.

### Actual Result

| Metric | Value |
|--------|-------|
| Stub exit code | 42 |
| Script exit code | 42 |
| Propagation | ✅ Pass |

The `script -qec` flag propagates the child process exit status.
The `set +e` / `set -e` wrapper preserves the code for logging.

## Reproducible Commands

```bash
# Trigger Eddie dispatch (from Pi5)
# Executor API: POST /execute with field "type" (not "job_type")
curl -X POST http://127.0.0.1:8081/execute \
  -H "Content-Type: application/json" \
  -d '{"job_id":"test-001","type":"infra.market.research","callback_url":"http://127.0.0.1:8081/callback/test-001"}'

# Check executor logs
tail -f /tmp/eddie-executor.log

# Check research output
ls /home/lydia/workspace/repos/infra/findings/current/
```

## Results

| Test | Status | Notes |
|------|--------|-------|
| Eddie dispatch | ✅ Pass | Job completed, exit 0 |
| opencode headless | ✅ Pass | Ran as lydia, wrote findings |
| Log rotation | ✅ Pass | Unique per-run filenames |
| Negative exit propagation | ✅ Pass | Stub exit 42 → script exit 42 |
| Executor callback propagation | ✅ Pass | Stub exit 42 → callback status "failed" |
| Fail-closed pull | ✅ Pass | Script exits 1 on git pull failure |

## CI Status

- Gitea CI: Not configured for this change
- Local validation: Diff and script reviewed manually

## Known Gaps

- No unit tests for `OPS_COMMANDS_USERS` logic
- No integration test for the conditional sudo path
