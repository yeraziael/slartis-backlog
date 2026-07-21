# ACP Epic: Browser Automation Framework (Playwright)

## Epic Metadata

| Field | Value |
|---|---|
| Epic ID | `ACP-EPIC-BROWSER-PLAYWRIGHT` |
| Title | ACP Browser Automation Framework (Playwright) |
| Priority | `P0` |
| Status | `PLANNED` |
| Owner | Slarti |
| ACP Reviewer | ChatGPT |
| Merge Authority | Eddie |
| Execution Model | Consecutive DeepSeek V4 Flash Free subagents |
| Integration Strategy | One feature branch, one final integration PR |
| Target Repository | Resolve during Child Issue 01; prefer the designated ACP repository, otherwise the architecture/runtime repository selected by Slarti from repository evidence |
| Planning Source | `yeraziael/slartis-backlog` |
| Planning Branch | `feature/acp-browser-automation-playwright` |
| Planning Artifact | `EPIC/ACP-BROWSER-AUTOMATION-PLAYWRIGHT.md` |

---

## 1. Vision

Create a secure, deterministic, ACP-governed browser automation framework based on Playwright that allows Homelab agents to execute approved browser workflows without granting unrestricted interactive browser access.

The framework shall expose a stable automation contract, enforce target and action policies, isolate browser contexts, capture reproducible evidence, support deterministic local tests, and produce review-ready ACP artifacts. It must be usable by Slarti for implementation, by Lydia for controlled execution, by Eddie for scheduling and merge orchestration, and by ChatGPT for SHA-bound final review.

The result is not a general-purpose remote browser. It is an agent execution capability with explicit boundaries, auditable inputs and outputs, controlled credentials, deterministic failure semantics, and ACP lifecycle integration.

---

## 2. Motivation

Several Homelab workflows cannot be completed through APIs alone. Examples include portals that expose only browser interfaces, administrative workflows requiring form interaction, downloads available only after authenticated navigation, and systems whose APIs are incomplete or unavailable.

Ad-hoc browser automation would create unacceptable operational risks:

- unrestricted navigation and data exfiltration;
- accidental destructive actions;
- credential leakage into logs, traces, screenshots, or source control;
- non-deterministic automation that cannot be reviewed or replayed;
- hidden coupling between agent prompts and page structure;
- no reliable evidence mapping between work orders, tests, and outcomes;
- no safe handoff from implementation to runtime operation.

This epic establishes the foundational framework before any production browser workflow is introduced.

---

## 3. Architecture Overview

### 3.1 Logical Components

```text
ACP Work Order
      |
      v
Browser Automation Contract Validator
      |
      v
Policy Gate ---------------------> Deny / Escalate
      |
      v
Execution Orchestrator
      |
      +--> Playwright Browser Runtime
      |       +--> isolated context
      |       +--> restricted target navigation
      |       +--> controlled downloads/uploads
      |       +--> redacted trace/screenshot capture
      |
      +--> Credential Resolver
      |       +--> runtime-only secret references
      |       +--> no plaintext credentials in work orders
      |
      +--> Evidence Collector
              +--> execution manifest
              +--> step results
              +--> screenshots/traces/logs
              +--> checksums
              +--> ACP evidence mapping
```

### 3.2 Proposed Technology Baseline

- Playwright with TypeScript and Node.js LTS.
- Chromium as the required initial browser engine.
- Firefox and WebKit are explicitly deferred unless repository evidence shows they are already mandatory.
- JSON Schema for machine-readable work orders, execution results, policy definitions, and evidence manifests.
- CLI-first execution surface suitable for Slarti, Lydia, CI, and future Eddie scheduling.
- Container-capable runtime, while retaining a deterministic local test mode.
- Dependency injection for browser launch, credential resolution, clock, filesystem paths, and network policy checks.
- Test fixtures based on a local static HTTP server; no public internet dependency in unit or integration tests.

### 3.3 Trust Boundaries

1. **ACP input boundary:** Work orders are untrusted until schema validation succeeds.
2. **Policy boundary:** Valid syntax does not imply authorization; targets and actions require policy approval.
3. **Credential boundary:** Work orders reference secret identifiers only. Secret values exist only at runtime.
4. **Browser boundary:** Every execution uses an isolated context and controlled storage lifecycle.
5. **Artifact boundary:** Logs, screenshots, traces, HTML snippets, and downloaded files are potentially sensitive and require redaction and retention rules.
6. **Merge boundary:** Implementation is not operationally approved until ChatGPT reviews the final head SHA and Eddie merges it.

---

## 4. Target State

At completion, the selected implementation repository contains:

- a versioned browser automation package;
- a CLI accepting an ACP Browser Work Order;
- schemas for work order, policy, result, and evidence manifest;
- a policy engine with deny-by-default target and action rules;
- isolated Playwright execution with deterministic timeouts and failure codes;
- runtime secret references without plaintext secret persistence;
- safe download handling and bounded artifact storage;
- configurable redaction for logs, screenshots, traces, and structured outputs;
- deterministic test fixtures and integration tests;
- CI gates for formatting, linting, type checking, unit tests, integration tests, schema validation, dependency audit, and secret scanning;
- operator and developer documentation;
- a final ACP review package bound to the final PR head SHA.

The first production release shall support narrowly defined workflows composed from approved primitives. Arbitrary JavaScript supplied in work orders is prohibited.

---

## 5. Scope and Non-Goals

### 5.1 In Scope

- Repository and runtime placement discovery.
- Playwright/TypeScript project bootstrap.
- ACP Browser Work Order schema.
- Declarative step model.
- CLI and execution orchestrator.
- Browser context isolation.
- Navigation allowlist and deny-by-default policy.
- Action-level policy controls.
- Secret reference resolution interface.
- Login/session state handling with explicit lifecycle rules.
- Download handling with path confinement and checksums.
- Evidence manifest and ACP acceptance-criterion mapping.
- Redaction of sensitive data.
- Deterministic local fixtures.
- CI and conformance tests.
- Documentation, examples, rollback instructions, and final review package.

### 5.2 Non-Goals

- CAPTCHA bypass.
- Anti-bot evasion or fingerprint spoofing.
- Generic remote desktop or VNC access.
- Arbitrary code execution inside browser steps.
- Autonomous discovery of destructive workflows.
- Password storage in repository files or work orders.
- Production workflows against real external services in CI.
- Multi-tenant browser sharing.
- Browser extension support.
- Persistent browser profiles by default.
- Firefox/WebKit parity in the initial release.
- Unattended financial transactions, legal declarations, purchases, or irreversible account changes.

---

## 6. Roles

### ChatGPT — ACP Architect and Final Reviewer

- defines the epic architecture and review expectations;
- reviews the final integration PR, its evidence package, and the exact head SHA;
- issues `APPROVED`, `APPROVED_WITH_FINDINGS`, or `CHANGES_REQUESTED`;
- does not merge the PR;
- may require remediation on the same feature branch.

### Slarti — Lead Implementer and Integration Owner

- resolves the target implementation repository;
- creates and remains on one feature branch for the entire epic;
- invokes exactly one DeepSeek V4 Flash Free subagent per Child Issue;
- provides each subagent only the issue-specific context and required repository files;
- runs deterministic tests after every Child Issue;
- reviews every diff before accepting it;
- commits each accepted Child Issue separately;
- proceeds automatically only when the issue gate passes;
- creates exactly one final integration PR unless an intermediate PR is technically unavoidable;
- assembles the final ACP review package.

### DeepSeek V4 Flash Free Subagents — Constrained Implementers

- each subagent receives exactly one Child Issue;
- each subagent works only within the declared file and behavior scope;
- no subagent decides architecture outside its issue contract;
- no subagent creates or merges PRs;
- no subagent modifies secrets, branch protection, production deployments, or unrelated files;
- each subagent returns changed files, test commands, test results, assumptions, and residual risks.

### Lydia — Runtime Consumer

- invokes approved browser work orders through the stable CLI or service interface;
- provides runtime secret references through approved mechanisms;
- stores and forwards execution evidence according to retention policy;
- does not bypass policy gates;
- does not dynamically inject arbitrary browser code.

### Eddie — Scheduler and Merge Authority

- may schedule approved runtime work orders after deployment;
- verifies the ACP review state before merge;
- merges only after all CI gates pass and ChatGPT approval is bound to the current head SHA;
- aborts merge if the head SHA changes after approval.

---

## 7. Branch Strategy

### 7.1 Required Branch Model

- Slarti creates one branch from the current default branch:
  - recommended name: `feature/acp-browser-automation-playwright`;
- all Child Issues are implemented consecutively on this branch;
- every Child Issue produces one logically scoped commit where practical;
- fixup commits are permitted before final review but must be squashed or clearly attributable before merge according to repository policy;
- direct pushes to the default branch are forbidden;
- no Child-Issue PRs are created.

### 7.2 Intermediate PR Exception

An intermediate PR is permitted only where a hard technical repository boundary makes a single PR impossible, for example:

- a required dependency must first be published from another repository;
- repository permissions prevent atomic implementation;
- a schema repository and runtime repository are independently protected and cannot be changed together.

If invoked, Slarti must document:

1. why the intermediate PR is technically unavoidable;
2. why a feature-branch-only integration is insufficient;
3. the dependency relation to the final integration PR;
4. how ChatGPT review remains SHA-bound across repositories.

Convenience, review size, or agent context limits are not valid reasons.

### 7.3 Final PR

Exactly one final integration PR shall represent the epic in the primary implementation repository. It must contain or link all required cross-repository commits and review evidence.

---

## 8. Workflow

```text
PLANNED
  -> TARGET_RESOLVED
  -> FEATURE_BRANCH_ACTIVE
  -> CHILD_01_RUNNING
  -> CHILD_01_TESTED
  -> CHILD_01_REVIEWED
  -> CHILD_01_ACCEPTED
  -> ... consecutive child execution ...
  -> INTEGRATION_TESTED
  -> REVIEW_PACKAGE_READY
  -> FINAL_PR_OPEN
  -> ACP_REVIEW_PENDING
  -> ACP_APPROVED
  -> EDDIE_MERGE_ALLOWED
  -> MERGED
  -> POST_MERGE_VERIFIED
```

For each Child Issue:

1. Slarti checks prerequisites.
2. Slarti creates a minimal issue-specific prompt.
3. Slarti invokes one fresh DeepSeek V4 Flash Free subagent.
4. The subagent implements only the contracted scope.
5. Slarti inspects the diff.
6. Slarti runs the issue's deterministic tests.
7. Slarti rejects or repairs any out-of-scope change.
8. Slarti records evidence and commits the accepted result.
9. Slarti advances automatically to the next Child Issue only when the issue DoD is true.

Failure handling:

- one retry with a fresh subagent is allowed after Slarti supplies precise failure evidence;
- repeated failure moves the epic to `BLOCKED` with the failing command, output, changed files, and root-cause hypothesis;
- Slarti must not silently weaken tests or acceptance criteria.

---

## 9. ACP Work Order

```yaml
apiVersion: acp.homelab/v1alpha1
kind: EpicWorkOrder
metadata:
  id: ACP-EPIC-BROWSER-PLAYWRIGHT
  title: ACP Browser Automation Framework (Playwright)
  priority: P0
  owner: slarti
  reviewer: chatgpt
  mergeAuthority: eddie
spec:
  executionMode: consecutive
  featureBranchOnly: true
  subagent:
    model: deepseek-v4-flash-free
    freshContextPerChild: true
    maxChildrenPerInvocation: 1
  pullRequests:
    intermediateAllowed: false
    exceptionPolicy: technically-unavoidable-cross-repository-boundary
    finalIntegrationPR: exactly-one
  review:
    shaBound: true
    finalReviewer: chatgpt
  merge:
    actor: eddie
    requires:
      - all-ci-gates-green
      - all-review-gates-green
      - chatgpt-approval-on-current-head-sha
  deliverables:
    - playwright-runtime
    - declarative-work-order-schema
    - policy-engine
    - credential-reference-interface
    - deterministic-test-suite
    - acp-evidence-package
```

### 9.1 Work Order Invariants

- No plaintext credentials.
- No arbitrary executable code in step definitions.
- No unapproved target origins.
- No execution without schema and policy validation.
- No merge without current-SHA approval.
- No automatic progression after a failing deterministic test.

---

## 10. Dependencies

### 10.1 Required

- Node.js LTS supported by the selected repository.
- Package manager already standardized by the repository, otherwise `pnpm` is preferred.
- Playwright and Chromium runtime dependencies.
- JSON Schema validator, preferably Ajv.
- Existing ACP artifact conventions or a local versioned compatibility layer.
- Secret source interface available to Lydia runtime, or a mockable adapter contract if the runtime implementation is deferred.
- CI runner capable of executing headless Chromium or a supported Playwright container.

### 10.2 Conditional

- Container build tooling if the target repository deploys containerized services.
- Object or filesystem artifact storage used by Lydia.
- Existing policy registry or tool-contract registry.
- Existing logging and observability library.

### 10.3 Dependency Resolution Rule

Child Issue 01 records actual versions, repository conventions, CI platform, package manager, deployment topology, and the ACP artifact location. Subsequent issues must use that recorded baseline and may not independently re-decide it.

---

## 11. Architecture Decisions (ADR)

### ADR-BA-001 — Playwright with TypeScript

- **Status:** Accepted for this epic.
- **Decision:** Implement the foundation in TypeScript using Playwright.
- **Rationale:** Strong Playwright support, type-safe contracts, broad tooling, deterministic test APIs, and maintainability within agent-generated code.
- **Consequence:** Node.js becomes a runtime dependency.

### ADR-BA-002 — Declarative Steps Only

- **Status:** Accepted.
- **Decision:** Work orders contain versioned declarative primitives, not arbitrary JavaScript or `eval`-equivalent content.
- **Rationale:** Enables validation, policy checks, review, replay, and bounded capability.
- **Consequence:** New actions require framework changes and review.

### ADR-BA-003 — Deny by Default

- **Status:** Accepted.
- **Decision:** Navigation origins, action types, uploads, downloads, and sensitive operations are denied unless explicitly authorized.
- **Rationale:** Browser automation is a high-impact capability.
- **Consequence:** Every production workflow requires a policy entry.

### ADR-BA-004 — Isolated Ephemeral Contexts

- **Status:** Accepted.
- **Decision:** Each execution receives a new browser context. Persistent state is opt-in, encrypted or externally protected, scoped, and separately reviewed.
- **Rationale:** Prevents cross-workflow contamination and session leakage.
- **Consequence:** Authentication may need explicit setup on every run or controlled storage-state injection.

### ADR-BA-005 — Evidence as a First-Class Output

- **Status:** Accepted.
- **Decision:** Every execution emits a structured result and evidence manifest with hashes and acceptance-criterion mappings.
- **Rationale:** ACP review requires deterministic evidence rather than narrative claims.
- **Consequence:** Artifact retention and redaction become mandatory concerns.

### ADR-BA-006 — Chromium First

- **Status:** Accepted.
- **Decision:** Chromium is mandatory for v1; other engines are deferred.
- **Rationale:** Reduces CI complexity and implementation surface while establishing the contract.
- **Consequence:** Cross-browser compatibility is not guaranteed in v1.

### ADR-BA-007 — CLI-First Interface

- **Status:** Accepted.
- **Decision:** The first stable execution interface is a CLI with file/stdin input and machine-readable output.
- **Rationale:** Simple integration with Slarti, Lydia, CI, and scripts; avoids premature service lifecycle complexity.
- **Consequence:** A daemon/API wrapper is a follow-up epic.

### ADR-BA-008 — No Network-Dependent CI Tests

- **Status:** Accepted.
- **Decision:** CI tests use local fixtures only.
- **Rationale:** Prevents flaky tests, accidental third-party actions, and credential requirements.
- **Consequence:** Real-site validation belongs to explicitly approved staging or operator acceptance.

---

## 12. Test Strategy

### 12.1 Test Pyramid

1. **Schema tests**
   - valid and invalid work orders;
   - version compatibility;
   - additional-property rejection where required.
2. **Unit tests**
   - policy decisions;
   - URL normalization;
   - redaction;
   - timeout and error mapping;
   - artifact hashing;
   - secret-reference validation.
3. **Component tests**
   - orchestrator with injected fake browser adapter;
   - filesystem confinement;
   - evidence generation.
4. **Playwright integration tests**
   - local fixture server;
   - navigation, selectors, inputs, clicks, waits, assertions, downloads;
   - isolated contexts;
   - deterministic screenshots and traces where stable.
5. **CLI contract tests**
   - exit codes;
   - JSON stdout/stderr contract;
   - malformed inputs;
   - policy denial;
   - browser failure.
6. **Security/conformance tests**
   - blocked origin;
   - path traversal;
   - secret leakage probes;
   - prohibited action types;
   - oversized artifact limits;
   - symlink escape checks where supported.

### 12.2 Determinism Rules

- Tests must not call public internet endpoints.
- Tests must not use real credentials.
- Fixtures must be versioned in the repository.
- Time and random identifiers must be injectable or normalized.
- Snapshot comparisons must exclude volatile fields.
- Retry counts must be explicit and minimal; retries must not conceal deterministic failures.
- Integration tests must clean up temporary directories and browser contexts.

### 12.3 Required Test Commands

Child Issue 01 defines repository-specific commands. The final suite must provide equivalents of:

```bash
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test:unit
pnpm test:integration
pnpm test:conformance
pnpm schema:check
pnpm build
```

---

## 13. CI Gates

All gates are mandatory on the final integration PR:

1. repository formatting check;
2. lint with zero errors;
3. TypeScript strict type check;
4. schema validation;
5. unit tests;
6. Playwright integration tests using local fixtures;
7. conformance/security tests;
8. production build;
9. dependency vulnerability audit according to repository policy;
10. secret scanning;
11. license policy check if present in the repository;
12. documentation link and example validation;
13. generated artifact cleanliness check (`git diff --exit-code` after generation/tests);
14. final review-package validation.

CI must fail closed. Optional or allowed-to-fail status is prohibited for gates 1–8 and 13–14.

---

## 14. Review Gates

### 14.1 Per Child Issue — Slarti Gate

Slarti records:

- issue ID;
- subagent model;
- changed files;
- diff scope result;
- deterministic commands executed;
- exit codes;
- review findings;
- accepted commit SHA.

Progression requires:

- all issue tests pass;
- no unrelated files changed;
- no acceptance criterion waived;
- no secret-like material introduced;
- documentation updated when the public contract changes.

### 14.2 Final ACP Review — ChatGPT Gate

The final PR must include a review package containing:

- final head SHA;
- epic ID and Child Issue completion matrix;
- acceptance criteria to evidence mapping;
- CI run identifiers and results;
- architecture decisions and deviations;
- security analysis;
- test inventory;
- artifact inventory with checksums;
- known limitations;
- rollback plan;
- operator validation instructions.

ChatGPT approval is valid only for the reviewed head SHA. Any subsequent commit invalidates approval and requires re-review.

---

## 15. Merge Gates

Eddie may merge only when all conditions are true:

- final integration PR exists and is not draft;
- PR targets the correct protected default branch;
- all required CI checks are green;
- no unresolved review threads remain;
- all Child Issues are marked complete in the review package;
- ChatGPT has approved the exact current head SHA;
- no new commits were added after approval;
- rollback instructions are present and executable;
- deployment is not bundled into the merge unless explicitly authorized by a separate work order.

Recommended merge method: repository-standard squash merge unless traceable child commits are an explicit ACP requirement in the target repository.

---

## 16. Rollback Strategy

### 16.1 Pre-Merge

- close or mark the final PR as draft;
- preserve the feature branch and evidence;
- do not alter the default branch.

### 16.2 Post-Merge, Pre-Deployment

- revert the merge commit or squash commit;
- run the full CI suite on the revert PR;
- merge the revert through normal protection rules.

### 16.3 Post-Deployment

- disable the browser automation capability through configuration or feature flag;
- stop scheduled Eddie invocations;
- revoke or rotate runtime credentials exposed to the framework if compromise is suspected;
- quarantine execution artifacts;
- revert the release or container image to the last known-good immutable version;
- run a post-rollback smoke test proving the capability is unavailable;
- create an incident record if security, privacy, or external side effects occurred.

### 16.4 Data Rollback

Browser actions may cause external side effects that code rollback cannot undo. Therefore production work orders must identify compensating actions or explicitly declare irreversibility. Irreversible workflows require operator approval and are outside this epic's implementation acceptance tests.

---

## 17. Artifacts

### 17.1 Source Artifacts

- TypeScript source package.
- JSON Schemas.
- policy configuration examples.
- local fixture application/pages.
- test suites.
- CLI documentation.
- operator runbook.
- ADRs or linked decision records.

### 17.2 Runtime Artifacts

- normalized work order copy with secret references only;
- execution result JSON;
- evidence manifest JSON;
- redacted structured logs;
- optional screenshots;
- optional Playwright trace;
- downloaded files with checksums;
- policy decision record;
- runtime and framework version metadata.

### 17.3 Review Artifacts

Recommended location:

```text
ACP/REVIEW/ACP-EPIC-BROWSER-PLAYWRIGHT/
├── review-package.yaml
├── child-issue-matrix.md
├── acceptance-evidence.yaml
├── ci-evidence.json
├── security-review.md
├── artifact-manifest.json
├── rollback.md
└── known-limitations.md
```

If the target repository already defines another canonical ACP review path, Slarti must use it and record the mapping.

---

## 18. Machine-Readable Definition of Done

```yaml
apiVersion: acp.homelab/v1alpha1
kind: DefinitionOfDone
metadata:
  epicId: ACP-EPIC-BROWSER-PLAYWRIGHT
spec:
  required:
    repository:
      targetResolved: true
      featureBranchOnly: true
      directDefaultBranchWrites: 0
      finalIntegrationPRCount: 1
      intermediatePRCount: 0
    subagents:
      model: deepseek-v4-flash-free
      oneChildPerInvocation: true
      freshContextPerChild: true
      allChildrenReviewedBySlarti: true
    architecture:
      playwright: true
      language: typescript
      browserBaseline: chromium
      cliFirst: true
      declarativeStepsOnly: true
      arbitraryCodeExecution: false
      denyByDefaultPolicy: true
      isolatedBrowserContext: true
      plaintextSecretsInWorkOrders: false
    contracts:
      workOrderSchemaVersioned: true
      resultSchemaVersioned: true
      policySchemaVersioned: true
      evidenceManifestSchemaVersioned: true
      stableExitCodesDocumented: true
    security:
      originAllowlistEnforced: true
      pathTraversalBlocked: true
      secretRedactionTested: true
      artifactLimitsEnforced: true
      runtimeSecretResolverAbstracted: true
    tests:
      publicInternetDependency: false
      schemaTestsPass: true
      unitTestsPass: true
      integrationTestsPass: true
      conformanceTestsPass: true
      cliContractTestsPass: true
      buildPass: true
    ci:
      formattingGreen: true
      lintGreen: true
      typecheckGreen: true
      schemaGateGreen: true
      unitGateGreen: true
      integrationGateGreen: true
      conformanceGateGreen: true
      buildGateGreen: true
      secretScanGreen: true
      reviewPackageGateGreen: true
    review:
      packagePresent: true
      acceptanceEvidenceMapped: true
      finalHeadShaRecorded: true
      chatgptApprovalCurrentSha: true
      unresolvedThreads: 0
    merge:
      actor: eddie
      allowedOnlyAfterAcpApproval: true
    documentation:
      architectureDocumented: true
      cliDocumented: true
      policyDocumented: true
      operatorRunbookPresent: true
      rollbackDocumented: true
      examplesValidated: true
```

---

## 19. Completion Criteria

The epic is complete only when:

1. all Child Issues below are completed in order;
2. each Child Issue has deterministic passing evidence and an accepted commit SHA;
3. the final integration suite passes locally and in CI;
4. the final ACP review package is complete and validates against its schema or documented contract;
5. ChatGPT reviews and approves the exact final PR head SHA;
6. Eddie merges the PR after confirming approval and CI state;
7. a post-merge verification confirms the default branch remains green;
8. no production browser workflow is activated without a separate approved work order.

---

## 20. Follow-Up Epics

1. **ACP Browser Workflow Registry** — signed/versioned catalog of approved production workflows.
2. **Lydia Browser Execution Adapter** — runtime integration, queueing, artifact upload, and operator notifications.
3. **Eddie Browser Scheduling and Concurrency Control** — schedules, locks, backoff, and idempotency.
4. **Browser Session Vault** — controlled persistent storage state with rotation, encryption, and provenance.
5. **Human Approval Gates for High-Impact Actions** — operator confirmation before submissions or irreversible actions.
6. **Browser Automation Service API** — authenticated service wrapper around the CLI.
7. **Multi-Browser Conformance** — Firefox and WebKit support.
8. **Visual Regression and Selector Resilience** — approved snapshots and maintainable locator contracts.
9. **Production Portal Workflow Epics** — one epic per external portal or business process.
10. **Browser Artifact Lifecycle Management** — retention, encryption, deletion, and privacy controls.

---

# Child Issue Plan

## Execution Rules for All Child Issues

- Execute in the listed order.
- Use one fresh DeepSeek V4 Flash Free subagent per issue.
- Target 30–60 minutes implementation effort per issue.
- Slarti supplies only the issue contract, relevant files, prior public contracts, and failing test evidence if applicable.
- Slarti reviews and tests before proceeding.
- Each issue ends in a commit on the single feature branch.
- No issue creates a PR.
- Any architectural deviation is recorded before implementation continues.

---

## Child 01 — Resolve Target Repository and Baseline

**ID:** `ACP-BA-001`

**Goal:** Determine the authoritative implementation repository and record its technical baseline.

**Inputs:**

- this epic;
- accessible Homelab repositories;
- existing ACP, agent runtime, tool registry, Lydia, and CI documentation;
- repository manifests and package files.

**Tasks:**

- identify the correct target repository;
- record default branch, language conventions, package manager, Node version, CI platform, test framework, deployment model, ACP artifact path, and relevant tool-contract conventions;
- document rejected repository candidates and rationale;
- define canonical local commands for format, lint, typecheck, unit, integration, build, and schema checks;
- create an epic implementation baseline document in the target repository.

**Outputs:**

- `docs/architecture/browser-automation-baseline.md` or repository-equivalent;
- explicit target repository decision;
- command matrix used by all later issues.

**Deterministic Tests:**

```bash
# Repository-specific equivalents are allowed.
test -f docs/architecture/browser-automation-baseline.md
# Verify every required command field is present.
grep -q "Package manager" docs/architecture/browser-automation-baseline.md
grep -q "Integration test" docs/architecture/browser-automation-baseline.md
```

**Definition of Done:**

- one target repository selected from evidence;
- baseline document committed;
- all required commands resolve or are explicitly marked for creation in Child 02;
- Slarti confirms no implementation code was introduced.

---

## Child 02 — Bootstrap TypeScript and Playwright Package

**ID:** `ACP-BA-002`

**Goal:** Create the minimal buildable package using repository-native conventions.

**Inputs:**

- Child 01 baseline;
- repository package and CI conventions.

**Tasks:**

- add package structure;
- configure strict TypeScript;
- install Playwright and required test tooling;
- add format, lint, typecheck, unit-test, integration-test, and build scripts;
- avoid downloading unused browser engines;
- add a minimal exported version constant.

**Outputs:**

- buildable package;
- lockfile changes;
- minimal test proving package import.

**Deterministic Tests:**

```bash
<package-manager> install --frozen-lockfile
<package-manager> typecheck
<package-manager> test:unit
<package-manager> build
```

**Definition of Done:**

- strict type checking passes;
- Chromium dependency is configured;
- no production behavior beyond package bootstrap;
- repository remains clean after build and tests.

---

## Child 03 — Define Versioned Browser Work Order Schema

**ID:** `ACP-BA-003`

**Goal:** Define the declarative input contract.

**Inputs:**

- epic architecture;
- ACP schema conventions;
- package baseline.

**Tasks:**

- define JSON Schema for metadata, target, timeout, artifact policy, credential references, and ordered steps;
- support initial primitives: `navigate`, `click`, `fill`, `select`, `check`, `uncheck`, `waitFor`, `assertText`, `assertVisible`, `download`, `screenshot`;
- prohibit unknown step types and arbitrary script fields;
- define schema versioning rules;
- add valid and invalid fixtures.

**Outputs:**

- work order schema;
- TypeScript types derived from or synchronized with schema;
- fixture corpus.

**Deterministic Tests:**

```bash
<package-manager> schema:check
<package-manager> test:unit -- work-order-schema
```

Must prove rejection of:

- unknown action;
- missing target;
- plaintext password field;
- arbitrary JavaScript field;
- invalid timeout;
- unexpected additional property in strict objects.

**Definition of Done:**

- schema is versioned;
- valid fixture accepted;
- every invalid fixture rejected for the intended reason;
- schema and TypeScript contract cannot silently diverge.

---

## Child 04 — Define Result, Error, and Exit-Code Contracts

**ID:** `ACP-BA-004`

**Goal:** Establish deterministic machine-readable outcomes.

**Inputs:**

- work order schema;
- CLI conventions.

**Tasks:**

- define execution result schema;
- define stable error categories and numeric CLI exit codes;
- include work order ID, framework version, timestamps, policy decision, step results, artifact references, and terminal state;
- distinguish validation, policy denial, browser launch, navigation, selector, timeout, assertion, artifact, and internal failures;
- document stdout/stderr rules.

**Outputs:**

- result schema;
- error taxonomy;
- exit-code documentation;
- unit tests.

**Deterministic Tests:**

```bash
<package-manager> schema:check
<package-manager> test:unit -- result-contract
```

**Definition of Done:**

- every defined failure category maps to one stable exit code and result state;
- output examples validate against schema;
- errors do not contain secret values in test probes.

---

## Child 05 — Implement Schema Validation Boundary

**ID:** `ACP-BA-005`

**Goal:** Reject malformed or unsupported work orders before any browser launch.

**Inputs:**

- work order and result schemas;
- valid/invalid fixtures.

**Tasks:**

- implement validator;
- normalize validation errors into stable result format;
- reject unsupported schema versions;
- prove browser adapter is not invoked on validation failure.

**Outputs:**

- validator module;
- unit tests with fake browser adapter invocation counter.

**Deterministic Tests:**

```bash
<package-manager> test:unit -- validation-boundary
```

**Definition of Done:**

- all invalid fixtures fail deterministically;
- valid fixture returns typed normalized input;
- browser invocation count remains zero on failure;
- error ordering is stable.

---

## Child 06 — Implement URL Normalization and Origin Policy

**ID:** `ACP-BA-006`

**Goal:** Enforce deny-by-default navigation policy.

**Inputs:**

- normalized work order;
- policy ADRs.

**Tasks:**

- define versioned policy schema;
- implement canonical origin parsing;
- support exact origins and narrowly defined subdomain patterns;
- reject non-HTTP(S) schemes, embedded credentials, malformed URLs, and origin bypass attempts;
- apply policy to initial target and subsequent navigation requests;
- produce structured allow/deny decisions.

**Outputs:**

- policy schema;
- origin policy module;
- bypass-oriented test corpus.

**Deterministic Tests:**

```bash
<package-manager> test:unit -- origin-policy
<package-manager> schema:check
```

Must include tests for:

- allowed exact origin;
- denied origin;
- deceptive suffix domain;
- uppercase and default-port normalization;
- URL username/password rejection;
- `file:`, `data:`, and `javascript:` rejection.

**Definition of Done:**

- policy denies by default;
- canonicalization occurs before matching;
- all bypass fixtures are rejected;
- decisions are machine-readable.

---

## Child 07 — Implement Action Policy and Safety Classification

**ID:** `ACP-BA-007`

**Goal:** Authorize declarative actions independently from URL authorization.

**Inputs:**

- work order step model;
- policy schema.

**Tasks:**

- classify actions as read, write, artifact, or sensitive;
- allow policy to enable or deny action classes and specific primitives;
- require explicit permission for form submissions, uploads, downloads, and persistent-state use;
- reserve unsupported destructive actions as denied;
- emit policy decision evidence per step.

**Outputs:**

- action policy module;
- policy fixtures;
- unit tests.

**Deterministic Tests:**

```bash
<package-manager> test:unit -- action-policy
```

**Definition of Done:**

- every primitive has one classification;
- undefined actions cannot be authorized;
- denied action prevents browser execution of that step;
- decision rationale is deterministic.

---

## Child 08 — Implement Secret Reference Contract and Resolver Interface

**ID:** `ACP-BA-008`

**Goal:** Support credentials without embedding secret values in work orders or logs.

**Inputs:**

- credential reference schema fields;
- Lydia/runtime secret conventions discovered in Child 01.

**Tasks:**

- define secret reference syntax;
- implement resolver interface and test-only in-memory resolver;
- reject plaintext secret fields;
- ensure secret values are wrapped or tagged for redaction;
- define missing-secret and access-denied failures;
- do not implement a production secret backend unless one already exists and only needs an adapter.

**Outputs:**

- resolver contract;
- test resolver;
- documentation for future runtime adapter.

**Deterministic Tests:**

```bash
<package-manager> test:unit -- secret-resolver
```

Must prove secret probes do not appear in serialized results or logs.

**Definition of Done:**

- no plaintext credential accepted in work order fixtures;
- resolver is injectable;
- secret values are unavailable to unrelated components;
- serialization leakage tests pass.

---

## Child 09 — Implement Browser Launcher and Isolated Context Lifecycle

**ID:** `ACP-BA-009`

**Goal:** Launch Chromium safely and guarantee context cleanup.

**Inputs:**

- Playwright package;
- execution contracts;
- policy-approved normalized work order.

**Tasks:**

- implement injectable browser launcher;
- create a new context per execution;
- configure deterministic viewport, locale, timezone, downloads, and timeout defaults;
- disable persistent profile use;
- close page, context, and browser on success and failure;
- expose lifecycle evidence without sensitive data.

**Outputs:**

- launcher/context module;
- lifecycle unit and integration tests.

**Deterministic Tests:**

```bash
<package-manager> test:unit -- browser-lifecycle
<package-manager> test:integration -- browser-lifecycle
```

**Definition of Done:**

- two executions cannot observe each other's cookies or local storage;
- cleanup occurs after injected failures;
- browser launch parameters are documented and testable.

---

## Child 10 — Implement Local Deterministic Fixture Server

**ID:** `ACP-BA-010`

**Goal:** Provide stable pages for all browser integration tests.

**Inputs:**

- supported step primitives;
- test framework conventions.

**Tasks:**

- create local fixture server with pages for navigation, forms, delayed content, assertions, cookies/storage, redirect tests, download, and error conditions;
- bind only to loopback;
- allocate or deterministically manage ports;
- implement reliable startup/readiness/shutdown helpers.

**Outputs:**

- fixture server;
- fixture pages;
- test helper API.

**Deterministic Tests:**

```bash
<package-manager> test:integration -- fixture-server
```

**Definition of Done:**

- no public network required;
- startup and shutdown leave no listener behind;
- fixture behavior is deterministic;
- server logs contain no volatile noise unless requested.

---

## Child 11 — Implement Core Read-Only Step Executor

**ID:** `ACP-BA-011`

**Goal:** Execute safe navigation and assertion primitives.

**Inputs:**

- browser lifecycle;
- fixture server;
- policy decisions;
- step contracts.

**Tasks:**

- implement `navigate`, `waitFor`, `assertText`, `assertVisible`, and `screenshot`;
- use Playwright locators, not brittle sleep-based timing;
- enforce per-step and overall timeouts;
- record structured step results;
- stop according to documented fail-fast behavior.

**Outputs:**

- read-only executor;
- integration tests.

**Deterministic Tests:**

```bash
<package-manager> test:integration -- readonly-steps
```

**Definition of Done:**

- success and failure paths produce schema-valid results;
- no fixed sleeps are used for synchronization;
- timeout failures map to stable error category;
- screenshot path is confined to execution artifact directory.

---

## Child 12 — Implement Controlled Form Interaction Steps

**ID:** `ACP-BA-012`

**Goal:** Execute approved non-arbitrary form interactions.

**Inputs:**

- action policy;
- secret resolver;
- fixture server.

**Tasks:**

- implement `click`, `fill`, `select`, `check`, and `uncheck`;
- permit values from literals or secret references according to field contract;
- prevent secret value echo in step results;
- distinguish interaction failure from assertion failure;
- require policy authorization for write-class actions.

**Outputs:**

- interaction executor;
- integration tests for literals and secret references.

**Deterministic Tests:**

```bash
<package-manager> test:integration -- form-steps
<package-manager> test:unit -- secret-redaction
```

**Definition of Done:**

- all supported form primitives operate against local fixtures;
- denied write action produces no page mutation;
- secret input is not serialized;
- locator failures are deterministic.

---

## Child 13 — Implement Download Handling and Filesystem Confinement

**ID:** `ACP-BA-013`

**Goal:** Safely capture approved downloads.

**Inputs:**

- download step schema;
- action policy;
- execution artifact directory.

**Tasks:**

- implement `download` primitive;
- constrain filenames and paths to the execution directory;
- prevent traversal, absolute paths, symlink escape where testable, and overwrite ambiguity;
- enforce count and size limits;
- calculate SHA-256 checksums;
- record MIME hint, size, and checksum in artifacts.

**Outputs:**

- download manager;
- security-focused tests.

**Deterministic Tests:**

```bash
<package-manager> test:integration -- downloads
<package-manager> test:conformance -- filesystem
```

**Definition of Done:**

- valid fixture download succeeds with correct checksum;
- traversal and oversize cases fail closed;
- no file is written outside the execution directory;
- partial files are cleaned up on failure.

---

## Child 14 — Implement Evidence Manifest and Artifact Hashing

**ID:** `ACP-BA-014`

**Goal:** Produce ACP-reviewable evidence for every execution.

**Inputs:**

- result contract;
- artifact outputs;
- ACP review conventions.

**Tasks:**

- define evidence manifest schema;
- include work order hash, framework version, policy hash, artifact hashes, step-to-acceptance mapping, and final state;
- ensure deterministic ordering;
- avoid absolute host paths in portable manifests;
- validate manifest after generation.

**Outputs:**

- evidence manifest schema and generator;
- unit and integration tests.

**Deterministic Tests:**

```bash
<package-manager> schema:check
<package-manager> test:unit -- evidence-manifest
<package-manager> test:integration -- evidence-manifest
```

**Definition of Done:**

- generated manifest validates;
- hashes match files;
- repeated execution with normalized volatile fields yields stable structural output;
- acceptance mappings cannot reference nonexistent steps or artifacts.

---

## Child 15 — Implement Redaction Pipeline

**ID:** `ACP-BA-015`

**Goal:** Prevent sensitive values from leaking into logs and review artifacts.

**Inputs:**

- secret wrapper/resolver;
- execution result;
- screenshots/traces/logs artifact model.

**Tasks:**

- implement structured text redaction using known secret values and configured patterns;
- redact request/result metadata before persistence;
- define screenshot/trace policy: disabled by default when secret fields are used unless explicit safe capture policy exists;
- add leakage probes across JSON, logs, errors, and artifact metadata;
- document residual limitations of image redaction.

**Outputs:**

- redaction module;
- security tests;
- operator documentation.

**Deterministic Tests:**

```bash
<package-manager> test:unit -- redaction
<package-manager> test:conformance -- secret-leakage
```

**Definition of Done:**

- all seeded secret probes absent from persisted textual artifacts;
- unsafe screenshot/trace capture is blocked by policy;
- redaction behavior is documented;
- false-negative limitations are explicitly stated.

---

## Child 16 — Implement CLI Entrypoint

**ID:** `ACP-BA-016`

**Goal:** Expose the framework through a stable machine-oriented CLI.

**Inputs:**

- validator;
- policy engine;
- orchestrator modules;
- result/exit-code contracts.

**Tasks:**

- accept work order and policy from files, with work order stdin support if repository conventions permit;
- accept an artifact output directory;
- emit one schema-valid result to stdout;
- route diagnostics to stderr without secrets;
- map terminal states to documented exit codes;
- add `--version` and `--help`;
- reject conflicting or unknown arguments.

**Outputs:**

- executable CLI;
- CLI contract tests.

**Deterministic Tests:**

```bash
<package-manager> build
<package-manager> test:integration -- cli
```

**Definition of Done:**

- success, validation failure, policy denial, timeout, and internal failure paths have tested exit codes;
- stdout remains machine-readable;
- CLI invokes no browser on validation/policy failure;
- help documents security boundaries.

---

## Child 17 — Add End-to-End Conformance Scenarios

**ID:** `ACP-BA-017`

**Goal:** Verify the complete execution path against local fixtures.

**Inputs:**

- finished CLI;
- fixture server;
- all schemas and policies.

**Tasks:**

- add success scenario with navigation, assertion, form interaction, and download;
- add denied-origin scenario;
- add denied-action scenario;
- add missing-secret scenario;
- add timeout scenario;
- add path traversal scenario;
- validate result and evidence artifacts for every scenario.

**Outputs:**

- conformance fixture suite;
- golden normalized expected outputs where appropriate.

**Deterministic Tests:**

```bash
<package-manager> test:conformance
```

**Definition of Done:**

- all scenarios execute without public network;
- expected exit codes and states match contracts;
- artifacts validate and hashes match;
- no secret probes leak.

---

## Child 18 — Add CI Workflow and Required Gates

**ID:** `ACP-BA-018`

**Goal:** Enforce all mandatory quality and security checks in CI.

**Inputs:**

- repository CI conventions;
- final command matrix;
- Playwright CI requirements.

**Tasks:**

- add or extend CI workflow;
- cache dependencies safely;
- install only required Chromium dependencies;
- run format, lint, typecheck, schema, unit, integration, conformance, build, secret scan, and clean-tree checks;
- retain failure artifacts only when redaction policy permits;
- document required check names for branch protection.

**Outputs:**

- CI workflow changes;
- gate documentation.

**Deterministic Tests:**

```bash
# Local equivalents
<package-manager> format:check
<package-manager> lint
<package-manager> typecheck
<package-manager> schema:check
<package-manager> test:unit
<package-manager> test:integration
<package-manager> test:conformance
<package-manager> build
git diff --exit-code
```

**Definition of Done:**

- workflow syntax validates;
- all local equivalents pass;
- mandatory gates are not marked optional;
- artifacts cannot expose seeded test secrets.

---

## Child 19 — Write Developer and Operator Documentation

**ID:** `ACP-BA-019`

**Goal:** Make the framework implementable, operable, and reviewable without hidden context.

**Inputs:**

- final contracts and commands;
- repository documentation conventions.

**Tasks:**

- document architecture and trust boundaries;
- document installation and Chromium dependencies;
- document work order and policy authoring;
- document CLI usage and exit codes;
- document secret integration contract;
- document artifact retention and redaction limitations;
- document troubleshooting and rollback;
- provide safe local examples only.

**Outputs:**

- architecture document;
- developer guide;
- operator runbook;
- validated examples.

**Deterministic Tests:**

```bash
<package-manager> docs:check  # create if repository supports documentation checks
# At minimum validate all JSON/YAML examples with project validators.
<package-manager> schema:check
```

**Definition of Done:**

- a new operator can run the local example without unstated steps;
- all examples validate;
- no real domains, accounts, tokens, or secrets are embedded;
- rollback and disable procedures are explicit.

---

## Child 20 — Assemble ACP Review Package and Final Integration Readiness

**ID:** `ACP-BA-020`

**Goal:** Produce the final review evidence and verify the entire feature branch.

**Inputs:**

- all accepted Child Issue commits;
- CI definitions;
- this epic's review artifact contract.

**Tasks:**

- generate Child Issue completion matrix with commit SHAs;
- map every epic acceptance criterion to tests and artifacts;
- record architecture deviations and rationale;
- produce security review, known limitations, rollback document, CI evidence placeholder/collector, and artifact manifest;
- run the complete local gate set from a clean checkout state;
- verify no untracked generated artifacts remain;
- prepare final PR title and body;
- record final branch head SHA after all changes.

**Outputs:**

- complete ACP review package;
- final test evidence;
- final PR-ready branch.

**Deterministic Tests:**

```bash
<package-manager> format:check
<package-manager> lint
<package-manager> typecheck
<package-manager> schema:check
<package-manager> test:unit
<package-manager> test:integration
<package-manager> test:conformance
<package-manager> build
<review-package-validator-command>
git status --porcelain
```

Expected final command output for `git status --porcelain`: empty.

**Definition of Done:**

- all 20 Child Issues are listed with accepted commit SHAs;
- all tests pass from the feature branch head;
- review package validates;
- final head SHA is recorded;
- Slarti opens exactly one final integration PR;
- PR requests ChatGPT ACP review and explicitly states that Eddie must not merge before current-SHA approval.

---

# Slarti Autonomous Continuation Contract

After each Child Issue, Slarti evaluates:

```yaml
childGate:
  prerequisitesSatisfied: true
  exactlyOneSubagentUsed: true
  modelWasDeepSeekV4FlashFree: true
  diffWithinScope: true
  deterministicTestsPassed: true
  noSecretsIntroduced: true
  slartiReviewPassed: true
  evidenceRecorded: true
  commitCreated: true
```

- If every field is `true`, Slarti starts the next Child Issue automatically.
- If any field is `false`, Slarti stops, records `BLOCKED`, and reports exact evidence.
- Slarti may repair integration defects directly only when the repair is small, deterministic, and documented; otherwise it invokes a fresh subagent for the same Child Issue.
- Slarti may not skip, merge, or reorder Child Issues without recording an ADR deviation and obtaining explicit operator authorization where the change alters scope or safety.

---

# Final PR Contract

Recommended title:

```text
feat(acp): add Playwright browser automation framework
```

Required PR body sections:

1. Epic and scope.
2. Architecture summary.
3. Child Issue completion matrix.
4. Security boundaries.
5. Test commands and results.
6. CI evidence.
7. Artifact and schema inventory.
8. Known limitations.
9. Rollback procedure.
10. Final head SHA.
11. Explicit review request to ChatGPT.
12. Explicit merge prohibition for Eddie until current-SHA ACP approval.

The final PR must not claim production activation. Deployment and first production workflow require separate approved work orders.
