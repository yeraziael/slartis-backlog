---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#247
state: closed
updated_at: 2026-07-16T22:45:53+02:00
is_epic: false
labels:
  - "Systemarchitektur"
  - "in-progress"
  - "sub-task"
publication: sanitized
---

# Execution Gate: dauerhaften Approval-Speicher bereitstellen

Parent: #212. Predecessor of: #231.

## Scope
Repo: `home-repo`; branch: `feat/execution-approval-store`.

Implement a channel-neutral, durable Execution Gate approval store under `runtime/gate/approvals.py`. Approval records bind an opaque approval ID to one principal and one action reference, expire at a fixed timestamp, and permit exactly one terminal decision (`approved` or `rejected`). Atomic file replacement and inter-process locking are required. Corrupt state, unknown IDs, wrong principals, expired records, and replay attempts fail closed.

The store records only approval ID, principal ID, action reference, timestamps, status, and trace ID. It must not store commands, message bodies, credentials, or arbitrary error strings. It does not execute actions.

Tests first: `python3 runtime/tests/test_execution_approvals.py` covers create, valid approval, valid rejection, wrong principal, expiry, unknown ID, corrupt state, and replay. Register the test through `ci-manifest.yaml` and regenerate CI artifacts with `ci-generate.py`.

Done: #231 can map Matrix `/approve <id>` and `/reject <id>` to this stable interface without inventing persistence or bypassing `runtime/gate/execution_gate.sh`.

Do not: deploy, execute privileged commands, read production secrets, or add channel-specific policy.
