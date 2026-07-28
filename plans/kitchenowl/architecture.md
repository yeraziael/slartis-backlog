# Target architecture

## Components

1. **KitchenOwl web** — existing user-facing web client extended with role-aware admin and stock-maintenance views.
2. **KitchenOwl backend** — system of record for catalog, lists, households and stock.
3. **Receipt ingestion worker** — reads Paperless metadata and documents, parses positions and emits idempotent stock events.
4. **Normalization service/module** — canonical products, variants, units, pack conversion and mapping confidence.
5. **Forecast engine** — consumption, season, weather, occasion, confidence and shopping-cycle calculations.
6. **Notification orchestrator** — Matrix-first delivery with Signal bridge, reply correlation, deadlines and escalation.
7. **Identity adapter** — maps Keycloak groups and identities to KitchenOwl authorization.
8. **Audit store** — append-only decision and mutation history linked to source events.
9. **Homelab status adapter** — exports only compact KitchenOwl health/status plus a deep link; detailed administration remains in KitchenOwl.

## Boundary rules

- The browser never receives Paperless, Matrix, Signal or Keycloak administrative credentials.
- The receipt worker has read-only Paperless access and narrow write access to the ingestion API.
- Stock mutation occurs only through typed, idempotent commands.
- Forecast output is advisory unless a rule explicitly permits automatic rate adjustment.
- Minimum-stock, weather, occasion, split and global model changes follow their defined approval gates.
- Keycloak is authoritative for role membership; KitchenOwl stores a cached effective-role snapshot only for audit and resilience.
- Signal phone linkage is personal data and must be encrypted at rest or referenced through a dedicated secrets store.

## Event model

Important immutable events include:

- receipt discovered / parsed / position accepted / skipped / remapped;
- stock added / measured / corrected;
- product normalized / merged / split;
- forecast calculated / rate adjusted / proposal approved or rejected;
- list created / updated / protected / migrated / closed;
- season, weather, household or occasion context changed;
- notification sent / escalated / muted / acted upon;
- authorization snapshot changed.

Derived state must be reproducible from durable domain data plus model versions. Every model output records its input horizon, version and confidence.

## Reliability

- At-least-once input delivery with idempotent consumers.
- Transactional outbox for notifications and cross-component events.
- Dead-letter handling for malformed receipts and uncorrelated replies.
- Health endpoints for web, backend, database, ingestion, forecasting and Matrix/Signal delivery.
- Backup and restore must include database, mapping/model metadata and encrypted linkage configuration.
- Replaying historical receipts must support dry-run and shadow modes before stock mutation.

## Upstream strategy

KitchenOwl upstream must remain mergeable. Custom code should be isolated behind modules, extension points and additive schema migrations. Direct invasive patches require an ADR documenting why a stable extension boundary was impossible and how future upstream merges are tested.