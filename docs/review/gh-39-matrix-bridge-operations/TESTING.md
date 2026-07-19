# GH-39 Test Evidence

## Test First

The initial contract test failed because
`pi/synapse/BRIDGE-OPERATIONS.md` did not exist. A second RED/GREEN cycle failed
until the existing `BRIDGES.md` installation guide linked the new operations
runbook.

## Full Local Validation

All commands passed on implementation head
`cca3131d262ad0a48be11b3238c699e507af47f6`:

```bash
make lint
make test
git diff --check
bash scripts/scan-secrets.sh --staged
```

The focused test verifies operations, backup, restore, upgrade, rollback,
resource acceptance, three independent bridge boundaries, Signal/Telegram
regression gates, executable blackbox steps, and exclusion of credential
patterns from the runbook.

After the first review requested changes, additional RED/GREEN cycles added
release-checkout binding, staged and unstaged worktree checks, active Synapse
configuration and appservice-list backup/restore, and per-bridge immediate
restart gates that prevent an unintended multi-bridge outage.
