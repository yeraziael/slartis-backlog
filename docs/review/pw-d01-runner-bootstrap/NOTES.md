# PW-D01 Review Notes

## Scope

Corrective source PR `#79` changes only
`docs/decisions/playwright/runner-bootstrap.md`. The complete effective decision
selects:

- Playwright and `@playwright/test` `1.61.1`;
- official Noble image tag plus immutable linux/amd64 manifest digest;
- image-supplied Node `24.17.0` and npm `11.13.0`;
- npm with a committed lockfile-v3 contract;
- Chromium-only MVP;
- one local/CI Make entry point and one Docker wrapper authority;
- an explicit non-browser bootstrap spec and lock provenance validator;
- an ephemeral dependency volume and separate dependency/test phases;
- network-none test execution, private shared memory, and non-root invoking
  UID/GID result ownership;
- an atomic image/package/browser/lockfile upgrade and Git-revert rollback.

## Principal Tradeoffs

- Every invocation performs a fresh `npm ci`; clean state and reproducibility
  take priority over initial speed.
- The dependency phase uses general Docker bridge egress. It receives no
  secrets, host environment, service variables, results mount, or browser
  execution, disables lifecycle scripts, and validates registry-only lock URLs
  plus integrity before installation.
- Chromium's sandbox is explicitly disabled for the controlled local-content
  MVP. Isolation instead relies on network-none execution, an ephemeral
  container, read-only root/source/dependency mounts, dropped capabilities,
  no-new-privileges, no Docker socket, and no persistent browser state.
- The runtime identity is the linux/amd64 manifest digest. The multi-platform
  index digest remains provenance only.

## Findings

- Resolved contract ambiguity: PW-I01 had no exact package script or owned test
  input despite requiring a successful target. It now has both without masking
  an empty suite or launching Chromium before PW-I02.
- Resolved contract ambiguity: Docker bridge was described as registry-only.
  The decision now states general egress and separately enforces lock URL and
  integrity provenance on every run.
- Resolved security contradictions: host IPC is replaced by private shared
  memory; root invokers are rejected; tmpfs/cache, environment, read-only mount,
  capability, and cleanup boundaries are exact.
- Resolved hidden decisions: discovery, output, retries, deferred seams,
  normative verification, and allowed implementation freedom are explicit.
- Resolved rollback gap: every version-coupled file, prior digest availability,
  atomic revert, and post-revert verification are required.
- Process friction: `make test` refreshed a tracked Python bytecode cache. It
  was restored before commit and is absent from the source PR.
- Domain learning: the official image supplies browser binaries and system
  libraries, not the project `@playwright/test` dependency; versions must match.
- No unresolved contract, prerequisite, implementation, test, infrastructure,
  evidence, or model finding remains in the corrected architecture.
- Governance finding: source PR `#78` was policy-merged before independent
  review. Corrective PR `#79` is WIP; external-review enforcement remains a
  five-ticket ACP checkpoint candidate.

## Explicit Exclusions

- No Playwright project files or CI edits.
- No dependency installation or browser execution.
- No live service, Keycloak, identity, selector, evidence-retention, retry, or
  secondary-browser contract.
- No merge, deployment, DNS, secret, account, container, or runtime mutation.

## Completion Boundary

Independent approval must bind to corrective source head
`5e4e566ab143f3e1a3f9b6a7bbd8b5798dc1bacb` and the new review-package head.
Only after approval may Eddie or the Operator remove WIP and merge source PR
`#79`. The decision remains `Proposed`, and PW-I01 remains blocked by both this
acceptance gate and the still-open canonical planning PR
`yeraziael/slartis-backlog#82`.
