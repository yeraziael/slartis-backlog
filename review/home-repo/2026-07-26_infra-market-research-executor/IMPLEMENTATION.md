# Implementation: infra-market-research-executor

## Files Changed

| File | Action | Lines |
|------|--------|-------|
| `runtime/infra-market-research.sh` | Added | +27 |
| `runtime/processor/executor_server.py` | Modified | +8/-2 |

## Semantic Summary

### executor_server.py

- Added `OPS_COMMANDS_USERS` dict mapping `infra.market.research` to `lydia`
- Modified `_run_ops` to read per-command user via `.get(job_type, "michael")`
- Conditional command construction: no sudo for lydia, sudo for others
- Path updated from `/home/michael/infra-market-research.sh` to `/home/lydia/bin/infra-market-research.sh`

### infra-market-research.sh

- New shell script (27 lines) that:
  - Sets `HOME=/home/lydia` and includes opencode in PATH
  - Clones or pulls `yeraziael/infra` repo
  - Runs `opencode run --auto --format json` with a research prompt
  - Logs to `/tmp/infra-market-research-<timestamp>.log`
  - Exits with opencode's exit code

## Breaking Changes

None. The change is backward-compatible:
- Existing ops commands continue to run as `michael` via sudo
- The new `OPS_COMMANDS_USERS` dict is additive
- The `.get()` default ensures old behavior for unmapped commands

## Migration Requirements

- Deploy updated `executor_server.py` to Pi5 processor
- Deploy `infra-market-research.sh` to `/home/lydia/bin/`
- Ensure lydia has read access to the script
