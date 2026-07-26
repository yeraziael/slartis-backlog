# Architecture: infra-market-research-executor

## Current State

The executor server (`executor_server.py`) listens for Eddie dispatches and runs ops commands via `sudo -n -u michael`. All ops commands run as the `michael` user on Pi5.

## Changes

### Per-Command User Mapping

A new `OPS_COMMANDS_USERS` dictionary maps job types to target users. The `_run_ops` method reads this mapping and uses the appropriate user:

- `infra.market.research` → `lydia`
- All other ops commands → `michael` (default, via `.get()`)

### Conditional Sudo

When the target user is `lydia`, the command runs directly (lydia owns the script and has the necessary environment). For other users, sudo is used as before.

### Research Script

`infra-market-research.sh` is a new script that:
1. Sets lydia's HOME and PATH (including opencode binary)
2. Clones or pulls the `yeraziael/infra` repo
3. Runs opencode headless with a research prompt
4. Exits with opencode's exit code

## Interfaces

- **Input:** Eddie dispatch via HTTP POST to executor
- **Output:** opencode runs headless, writes findings to `infra` repo
- **Logs:** `/tmp/infra-market-research-<timestamp>.log`

## Data Flow

```
Eddie → executor_server.py (port 8081)
  → _run_ops(job_type="infra.market.research")
  → OPS_COMMANDS_USERS["infra.market.research"] = "lydia"
  → [command] (no sudo, runs as lydia)
  → infra-market-research.sh
  → opencode run --auto --format json
  → findings/current/ in yeraziael/infra
```
