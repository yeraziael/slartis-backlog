# Architecture — ACP v0.2 Review Fix

No architectural changes. All changes are corrective to existing specifications and schemas.

## Key Architectural Invariants Maintained

1. **Eddie contains no execution logic** — unchanged
2. **Executor (Lydia) interprets nothing** — unchanged
3. **Contract immutability after submission** — reinforced by immutable identity model
4. **Deterministic audit trails** — new identity model ensures every execution traces to exactly one trigger version

## Contract Identity Model (New)

```
Trigger identity = (trigger_id, activation.version)

Constraints:
  - (trigger_id, version) pair MUST be unique in Eddie's registry
  - Changing ANY field requires a new activation.version
  - Eddie MUST reject registration with same (trigger_id, version) but different content
```

This replaces the implicit single-version model from v0.1 and aligns with ACP's principle that all contracts are immutable after registration.
