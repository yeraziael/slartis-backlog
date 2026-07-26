# Summary: infra-market-research-executor

## Problem Statement

Eddie needs to trigger daily infrastructure market research via opencode on Pi5, but the current executor runs all ops commands as `michael` via sudo. The research script must run as `lydia` (the opencode user on Pi5) with its own environment and credentials.

## Goal

Enable Eddie to dispatch `infra.market.research` jobs that execute as `lydia` on Pi5, running opencode headless against the `yeraziael/infra` repository for automated daily market research.

## Scope

- New `infra-market-research.sh` script that runs opencode headless as lydia
- Per-command user mapping in executor_server.py (`OPS_COMMANDS_USERS`)
- Conditional sudo bypass when running as lydia (lydia owns the script)

## Not in Scope

- Eddie scheduling configuration (handled separately)
- The `yeraziael/infra` repository contents or research methodology
- Other ops commands (remain as michael-only)

## Affected Components

- `runtime/processor/executor_server.py` — executor dispatch logic
- `runtime/infra-market-research.sh` — new research trigger script

## References

- Canonical PR: `lydia/home-repo#389` (Gitea)
- Supersedes: PR #388 (exit status fix)
- Issue: Eddie daily market research trigger
- Base commit: `5ce6ecd`
- Head commit: `1cd019c`
