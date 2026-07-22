# PW-D01 Review Notes

## Scope

The source PR adds only
`docs/decisions/playwright/runner-bootstrap.md`. It selects:

- Playwright and `@playwright/test` `1.61.1`;
- official Noble image tag plus immutable linux/amd64 manifest digest;
- image-supplied Node `24.17.0` and npm `11.13.0`;
- npm with a committed lockfile-v3 contract;
- Chromium-only MVP;
- one local/CI Make entry point and one Docker wrapper authority;
- an ephemeral dependency volume and separate dependency/browser phases;
- network-none browser execution and invoking-UID/GID result ownership;
- an atomic image/package/browser/lockfile upgrade and Git-revert rollback.

## Principal Tradeoffs

- Every invocation performs a fresh `npm ci`; clean state and reproducibility
  take priority over initial speed.
- The dependency phase uses Docker bridge networking to reach the configured
  npm registry, but receives no secrets, service variables, results mount, or
  browser execution.
- Chromium's sandbox is explicitly disabled for the controlled local-content
  MVP. Isolation instead relies on network-none execution, an ephemeral
  container, read-only root/source/dependency mounts, dropped capabilities,
  no-new-privileges, no Docker socket, and no persistent browser state.
- The runtime identity is the linux/amd64 manifest digest. The multi-platform
  index digest remains provenance only.

## Findings

- Resolved contract ambiguity: a one-phase design could not combine `npm ci`
  registry access with network-free browser execution. The decision separates
  those phases.
- Resolved draft defect: image-root browser execution could create root-owned
  host results. The browser phase now uses the invoking host UID/GID.
- Process friction: `make test` refreshed a tracked Python bytecode cache. It
  was restored before commit and is absent from the source PR.
- Domain learning: the official image supplies browser binaries and system
  libraries, not the project `@playwright/test` dependency; versions must match.
- No unresolved contract, prerequisite, implementation, test, infrastructure,
  evidence, or model finding remains.
- No generic ACP candidate was identified by this ticket.

## Explicit Exclusions

- No Playwright project files or CI edits.
- No dependency installation or browser execution.
- No live service, Keycloak, identity, selector, evidence-retention, retry, or
  secondary-browser contract.
- No merge, deployment, DNS, secret, account, container, or runtime mutation.

## Completion Boundary

Independent approval must bind to both the source head and the review-package
head. Eddie or the Operator alone may merge the source PR. The decision remains
`Proposed` until that merge, and PW-I01 remains blocked by both this acceptance
gate and the still-open canonical planning PR `yeraziael/slartis-backlog#82`.
