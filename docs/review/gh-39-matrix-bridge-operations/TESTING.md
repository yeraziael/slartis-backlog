# GH-39 Test Evidence

## Test First

The initial contract test failed because
`pi/synapse/BRIDGE-OPERATIONS.md` did not exist. A second RED/GREEN cycle failed
until the existing `BRIDGES.md` installation guide linked the new operations
runbook.

## Full Local Validation

All commands passed on implementation head
`42101fe2a43ccd98633f0da48fd44fa80673931b`:

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
