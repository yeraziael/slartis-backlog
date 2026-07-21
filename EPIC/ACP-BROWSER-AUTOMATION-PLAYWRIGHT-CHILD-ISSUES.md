# ACP Browser Automation Framework (Playwright) — Executable Child Issues

> Parent epic: `ACP-EPIC-BROWSER-PLAYWRIGHT`
>
> Execution model: exactly one fresh DeepSeek V4 Flash Free subagent per Child Issue, executed consecutively by Slarti on one feature branch.

## Global Execution Contract

The following rules apply to every Child Issue and do not need to be rediscovered by a subagent.

- Work only on the active epic feature branch. Never modify the default branch directly.
- Implement only the files and behavior explicitly permitted by the current Child Issue.
- Do not create, merge, or close pull requests.
- Do not change branch protection, repository settings, secrets, deployment state, or production schedules.
- Do not introduce public-network-dependent tests.
- Do not weaken existing tests, lint rules, schemas, policy checks, or acceptance criteria.
- Do not add plaintext credentials, tokens, cookies, session data, or personal data to source, fixtures, logs, snapshots, or artifacts.
- Use repository-standard tooling established by Child 01.
- Return a completion report containing: changed files, commands executed, exit codes, assumptions, remaining risks, and suggested commit message.
- Slarti reviews the diff and independently executes the deterministic tests before accepting the result.
- Automatic progression is permitted only when every DoD item is true and the accepted commit SHA is recorded.

## Standard Subagent Response

```yaml
childIssue: ACP-BA-NNN
status: completed | blocked | failed
changedFiles: []
commands:
  - command: "..."
    exitCode: 0
    result: "..."
assumptions: []
residualRisks: []
suggestedCommitMessage: "..."
```

---

# Child 01 — Resolve Repository, Baseline, and Implementation Contract

**ID:** `ACP-BA-001`  
**Estimated effort:** 30–60 minutes  
**Depends on:** none  
**Allowed change type:** documentation and non-invasive discovery helpers only

## Objective

Determine the exact implementation repository, package location, runtime constraints, ACP artifact conventions, CI platform, package manager, Node.js version, and deployment boundary. Freeze these findings as the authoritative baseline for all later Child Issues.

## Inputs

- Parent epic.
- Current Homelab repository inventory available to Slarti.
- Existing repository documentation, manifests, CI files, ACP files, tool registries, and runtime contracts.
- Current feature-branch requirement.

## Required Work

1. Inspect candidate repositories and select one primary implementation repository using this order:
   1. an existing ACP repository that already contains executable capability implementations;
   2. an existing agent/tool runtime repository with compatible TypeScript/Node conventions;
   3. a new package within the most appropriate architecture/runtime repository.
2. Record why rejected candidates were not selected.
3. Determine:
   - default branch;
   - active feature branch name;
   - package manager and lockfile;
   - Node.js version source;
   - TypeScript configuration;
   - test framework;
   - lint/format tools;
   - CI implementation;
   - secret-scanning mechanism;
   - ACP review artifact path;
   - intended Lydia integration boundary;
   - whether container packaging is already standard.
4. Define canonical commands for install, format check, lint, typecheck, unit tests, integration tests, conformance tests, schema validation, build, and full verification.
5. Create `docs/acp-browser-automation/implementation-baseline.md` or the repository-equivalent canonical path.
6. Create a small machine-readable baseline file, preferably `acp-browser-baseline.yaml`, containing the selected values.
7. Do not bootstrap Playwright or modify production code.

## Explicit Non-Scope

- No dependency installation.
- No package creation.
- No workflow implementation.
- No CI behavior change.
- No deployment or secret configuration.

## Required Outputs

- Human-readable implementation baseline.
- Machine-readable baseline.
- Exact canonical command table.
- Selected implementation path and rationale.
- List of unresolved blockers, which must be empty for automatic continuation.

## Deterministic Tests

```bash
# Adapt paths, but do not replace these checks with narrative verification.
test -f docs/acp-browser-automation/implementation-baseline.md
<yaml-validator> acp-browser-baseline.yaml
<package-manager-existing-command> lint-or-doc-check

git diff --check
git status --short
```

The machine-readable baseline must contain at least:

```yaml
implementationRepository: owner/repository
implementationPath: path/to/package
packageManager: pnpm|npm|yarn
nodeVersionSource: path-or-policy
ciPlatform: github-actions|gitea-actions|other
featureBranch: feature/acp-browser-automation-playwright
acpReviewPath: path
canonicalCommands:
  install: "..."
  formatCheck: "..."
  lint: "..."
  typecheck: "..."
  unit: "..."
  integration: "..."
  conformance: "..."
  schema: "..."
  build: "..."
  verify: "..."
```

## Definition of Done

- Exactly one target repository and implementation path are selected.
- Every required tooling decision is supported by repository evidence.
- Canonical commands are executable or explicitly marked `to-be-created` for later issues.
- No production code or runtime configuration changed.
- No blocker remains that prevents Child 02.
- Slarti records the accepted commit SHA and automatically starts Child 02.

---

# Child 02 — Bootstrap the Playwright TypeScript Package

**ID:** `ACP-BA-002`  
**Estimated effort:** 30–60 minutes  
**Depends on:** `ACP-BA-001`

## Objective

Create the smallest repository-conformant TypeScript package that can build, typecheck, run unit tests, and resolve Playwright Chromium without implementing browser automation behavior.

## Inputs

- Child 01 baseline files.
- Repository package conventions.
- Existing workspace and CI configuration.

## Required Work

1. Create the package in the selected implementation path.
2. Add repository-compatible manifests, strict TypeScript configuration, source and test directories.
3. Add Playwright as a pinned dependency according to lockfile policy.
4. Configure Chromium as the only required browser engine.
5. Add minimal exported package metadata and a placeholder typed API that throws a documented `NOT_IMPLEMENTED` error only when invoked.
6. Add scripts for typecheck, unit test, build, and browser installation where the repository does not already centralize them.
7. Ensure generated files and browser binaries are excluded correctly.
8. Add one deterministic unit test proving the package loads and exposes its version.

## Explicit Non-Scope

- No work-order schema.
- No CLI.
- No browser launch.
- No policy engine.
- No container image.

## Required Outputs

- Package manifest and lockfile update.
- Strict TypeScript configuration.
- Minimal source entry point.
- Minimal unit test.
- Updated workspace configuration if required.

## Deterministic Tests

```bash
<install-command>
<typecheck-command>
<unit-command>
<build-command>
git diff --check
git diff --exit-code -- . ':!<expected-generated-files>'
```

## Definition of Done

- Fresh install from the lockfile succeeds.
- Strict typecheck succeeds.
- Unit test succeeds without launching a browser.
- Production build succeeds.
- Chromium dependency is pinned and installable.
- No unsupported browser engine is required.
- Slarti records the accepted commit SHA and starts Child 03.

---

# Child 03 — Define the Versioned Browser Work Order Contract

**ID:** `ACP-BA-003`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-002`

## Objective

Define a strict, versioned, declarative ACP Browser Work Order schema and synchronized TypeScript contract.

## Required Work

1. Create JSON Schema `v1alpha1` for:
   - metadata and work-order ID;
   - target URL;
   - policy reference;
   - overall and per-step timeout limits;
   - credential references;
   - artifact policy;
   - ordered steps;
   - acceptance-criterion identifiers.
2. Define exactly these initial step primitives:
   - `navigate`;
   - `click`;
   - `fill`;
   - `select`;
   - `check`;
   - `uncheck`;
   - `waitFor`;
   - `assertText`;
   - `assertVisible`;
   - `download`;
   - `screenshot`.
3. Forbid unknown properties in security-relevant objects.
4. Forbid arbitrary scripts, expressions, JavaScript, eval fields, inline cookies, plaintext passwords, raw tokens, and unrestricted headers.
5. Define selectors using one explicit locator contract; prefer role/test-id/text-safe locators over unrestricted script selectors.
6. Synchronize schema and TypeScript types using repository-standard generation or compile-time tests.
7. Add valid and invalid fixture corpus.
8. Document version compatibility and future schema evolution.

## Required Invalid Fixtures

- unknown step type;
- missing target;
- malformed work-order ID;
- plaintext password;
- raw bearer token;
- arbitrary JavaScript field;
- negative timeout;
- excessive timeout;
- unexpected additional property;
- empty steps;
- duplicate step IDs.

## Deterministic Tests

```bash
<schema-check-command>
<unit-command> -- work-order-schema
<typecheck-command>
git diff --check
```

## Definition of Done

- The schema has a stable `$id` and explicit version.
- One canonical valid fixture passes.
- Every invalid fixture fails for its intended reason.
- TypeScript and schema cannot silently diverge.
- No browser is launched by tests.
- Slarti starts Child 04.

---

# Child 04 — Define Result, Error, and CLI Exit Contracts

**ID:** `ACP-BA-004`  
**Estimated effort:** 30–60 minutes  
**Depends on:** `ACP-BA-003`

## Objective

Create deterministic machine-readable execution result, step result, error, terminal-state, and CLI exit-code contracts.

## Required Work

1. Create versioned result JSON Schema.
2. Define terminal states: `succeeded`, `rejected`, `failed`, `cancelled`.
3. Define stable error categories for:
   - input read;
   - schema validation;
   - unsupported version;
   - policy denial;
   - missing secret;
   - secret access denial;
   - browser launch;
   - navigation;
   - locator;
   - timeout;
   - assertion;
   - interaction;
   - download;
   - artifact;
   - internal failure.
4. Define non-overlapping numeric exit codes.
5. Define stdout as exactly one final JSON result for machine mode.
6. Define stderr as redacted diagnostic output only.
7. Include work-order hash, framework version, timestamps, policy decision, ordered step results, artifacts, and terminal state.
8. Normalize volatile fields in test fixtures.

## Deterministic Tests

```bash
<schema-check-command>
<unit-command> -- result-contract
<typecheck-command>
```

## Definition of Done

- Every failure category maps to one terminal state and one stable exit code.
- Examples validate against the result schema.
- Secret probe values never occur in serialized examples or errors.
- Contract documentation contains a complete exit-code table.
- Slarti starts Child 05.

---

# Child 05 — Implement the Validation Boundary

**ID:** `ACP-BA-005`  
**Estimated effort:** 30–60 minutes  
**Depends on:** `ACP-BA-004`

## Objective

Reject malformed and unsupported work orders before policy evaluation, secret resolution, filesystem creation, or browser launch.

## Required Work

1. Implement strict schema validation using the selected validator.
2. Normalize validation messages into the Child 04 result contract.
3. Sort or otherwise stabilize error ordering.
4. Reject unsupported `apiVersion` values.
5. Return a typed normalized work order on success.
6. Inject counters/fakes proving downstream boundaries are not invoked after validation failure.
7. Ensure raw rejected input is not echoed wholesale into logs.

## Deterministic Tests

```bash
<unit-command> -- validation-boundary
<typecheck-command>
```

Required assertions:

- browser invocations: `0` on invalid input;
- policy invocations: `0` on invalid input;
- secret resolver invocations: `0` on invalid input;
- artifact directory creations: `0` on invalid input.

## Definition of Done

- All invalid fixtures fail deterministically.
- Valid fixtures return typed normalized values.
- Downstream invocation counts remain zero on rejection.
- Error ordering is stable across repeated runs.
- Slarti starts Child 06.

---

# Child 06 — Implement URL Canonicalization and Origin Policy

**ID:** `ACP-BA-006`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-005`

## Objective

Implement deny-by-default target authorization for initial and subsequent navigations.

## Required Work

1. Define a versioned policy schema for allowed origins and optional narrow subdomain patterns.
2. Canonicalize scheme, host, IDNA form, default ports, and trailing origin syntax before comparison.
3. Reject:
   - non-HTTP(S) schemes;
   - embedded username/password;
   - malformed URLs;
   - deceptive suffix domains;
   - wildcard rules that match public suffixes;
   - loopback/private destinations unless explicitly allowed by policy;
   - redirect destinations outside policy.
4. Produce structured allow/deny decisions with stable reason codes.
5. Provide a browser-route guard interface for later integration.

## Deterministic Tests

```bash
<unit-command> -- origin-policy
<schema-check-command>
```

Required cases include exact allow, default deny, uppercase normalization, default-port normalization, deceptive suffix, IDNA, embedded credentials, `file:`, `data:`, `javascript:`, redirect escape, and malformed URL.

## Definition of Done

- Canonicalization always precedes matching.
- Default decision is deny.
- All bypass fixtures fail closed.
- Policy decisions are schema-valid and deterministic.
- Slarti starts Child 07.

---

# Child 07 — Implement Action Policy and Safety Classification

**ID:** `ACP-BA-007`  
**Estimated effort:** 30–60 minutes  
**Depends on:** `ACP-BA-006`

## Objective

Authorize each step independently of target authorization using explicit action classes and deny-by-default rules.

## Required Work

1. Classify every supported primitive as `read`, `write`, `artifact`, or `sensitive`.
2. Extend policy schema with allowed classes and allowed/denied primitives.
3. Require explicit permission for write interactions, downloads, uploads if later added, screenshots on sensitive pages, and persistent-state use.
4. Prevent undefined primitives from becoming authorized through broad class rules.
5. Emit per-step decision records with stable reason codes.
6. Add a preflight function that can reject the complete work order before browser launch when any step is statically unauthorized.

## Deterministic Tests

```bash
<unit-command> -- action-policy
<schema-check-command>
```

## Definition of Done

- Every primitive has exactly one safety class.
- Undefined primitives are never authorized.
- Denied steps do not reach executor fakes.
- Decision order and rationale are deterministic.
- Slarti starts Child 08.

---

# Child 08 — Implement Secret Reference and Resolver Boundary

**ID:** `ACP-BA-008`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-007`

## Objective

Support runtime credentials through references while preventing plaintext secret persistence and serialization.

## Required Work

1. Define strict secret reference syntax, including namespace/provider/key fields only where supported by Child 01 evidence.
2. Implement an injectable resolver interface.
3. Implement an in-memory test resolver.
4. Represent resolved values with a type that discourages accidental stringification.
5. Define missing-secret and access-denied errors.
6. Implement secret-value registration for redaction.
7. Reject plaintext credential-like fields at schema and runtime boundaries.
8. Do not implement a new production secret store.

## Deterministic Tests

```bash
<unit-command> -- secret-resolver
<unit-command> -- secret-leakage
```

Use distinctive probe secrets and recursively scan serialized results, errors, logs, snapshots, and artifact metadata.

## Definition of Done

- Resolver is injectable.
- Test resolver supports success, missing, and denied outcomes.
- Probe secrets never appear in any serialized output.
- Unrelated components cannot retrieve secret values.
- Slarti starts Child 09.

---

# Child 09 — Implement Chromium Launcher and Ephemeral Context Lifecycle

**ID:** `ACP-BA-009`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-008`

## Objective

Launch Chromium through an injectable adapter and guarantee isolated context lifecycle and cleanup.

## Required Work

1. Implement browser launcher abstraction.
2. Create a new context per execution.
3. Configure deterministic viewport, locale, timezone, color scheme, downloads, and timeout defaults.
4. Prohibit persistent profile directories.
5. Ensure page, context, and browser close in reverse order on success and every failure path.
6. Emit non-sensitive lifecycle evidence.
7. Add test hooks for forced launch, page, and cleanup failures.

## Deterministic Tests

```bash
<unit-command> -- browser-lifecycle
<integration-command> -- browser-lifecycle
```

Required proof:

- cookies and local storage from execution A are absent in B;
- cleanup runs after an injected step failure;
- no Chromium process remains after test completion;
- launch parameters match documented defaults.

## Definition of Done

- Context isolation is demonstrated.
- Cleanup is idempotent and failure-safe.
- Persistent profiles are impossible through the public contract.
- Slarti starts Child 10.

---

# Child 10 — Implement the Local Deterministic Fixture Server

**ID:** `ACP-BA-010`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-009`

## Objective

Provide loopback-only deterministic pages supporting every current integration-test scenario.

## Required Work

1. Implement fixture server startup, readiness, base URL discovery, and shutdown helpers.
2. Bind only to loopback.
3. Add pages/endpoints for:
   - basic navigation;
   - text and visibility assertions;
   - delayed content;
   - form controls;
   - cookies/local storage;
   - same-origin redirect;
   - blocked redirect target representation;
   - deterministic download;
   - not-found and server-error responses.
4. Avoid external assets, timestamps, random content, analytics, and CDN dependencies.
5. Ensure teardown releases ports and temporary files.

## Deterministic Tests

```bash
<integration-command> -- fixture-server
```

## Definition of Done

- Server requires no public network.
- Repeated startup/shutdown succeeds.
- No listener remains after teardown.
- Fixture responses are byte-stable where expected.
- Slarti starts Child 11.

---

# Child 11 — Implement Core Read-Only Step Execution

**ID:** `ACP-BA-011`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-010`

## Objective

Execute approved read-only primitives using Playwright locators and deterministic timeout/error behavior.

## Required Work

1. Implement `navigate`, `waitFor`, `assertText`, `assertVisible`, and `screenshot`.
2. Enforce precomputed origin and action decisions.
3. Use locators and web-first assertions; do not add fixed sleeps.
4. Enforce per-step and overall timeouts.
5. Produce ordered schema-valid step results.
6. Implement documented fail-fast semantics.
7. Confine screenshot paths to the execution artifact directory.

## Deterministic Tests

```bash
<integration-command> -- readonly-steps
<unit-command> -- timeout-mapping
```

## Definition of Done

- Every primitive succeeds against positive fixtures.
- Negative fixtures map to correct stable errors.
- No fixed sleep is used.
- Screenshot output cannot escape the artifact directory.
- Slarti starts Child 12.

---

# Child 12 — Implement Controlled Form Interaction

**ID:** `ACP-BA-012`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-011`

## Objective

Execute approved form interactions without arbitrary page scripting or secret leakage.

## Required Work

1. Implement `click`, `fill`, `select`, `check`, and `uncheck`.
2. Accept literals and approved secret references according to schema.
3. Never serialize resolved secret values in step results.
4. Require write-class authorization before mutation.
5. Distinguish locator, interaction, and assertion failures.
6. Add fixture assertions proving denied actions cause no page mutation.
7. Do not add a generic `evaluate`, script, keyboard macro, or raw DOM function.

## Deterministic Tests

```bash
<integration-command> -- form-steps
<unit-command> -- secret-redaction
```

## Definition of Done

- All supported controls work against local fixtures.
- Denied actions cause zero mutation.
- Secret probe values do not appear in outputs.
- Unsupported interactions remain impossible.
- Slarti starts Child 13.

---

# Child 13 — Implement Download Handling and Filesystem Confinement

**ID:** `ACP-BA-013`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-012`

## Objective

Capture explicitly authorized downloads within a bounded execution directory.

## Required Work

1. Implement `download` execution.
2. Normalize and sanitize server-suggested filenames.
3. Prevent absolute paths, traversal, separator tricks, reserved names, symlink escape, and overwrite ambiguity.
4. Enforce configurable file count and byte limits.
5. Stream or stage files safely and remove partial files on failure.
6. Calculate SHA-256 checksum, byte size, and MIME hint.
7. Record artifacts without embedding file content.

## Deterministic Tests

```bash
<integration-command> -- downloads
<conformance-command> -- filesystem
```

Required adversarial cases: `../`, encoded traversal, absolute path, duplicate name, oversized response, interrupted response, symlink target, and zero-byte file.

## Definition of Done

- Valid fixture download has expected checksum.
- No tested bypass writes outside the execution directory.
- Limit violations fail closed.
- Partial files are removed.
- Slarti starts Child 14.

---

# Child 14 — Implement Evidence Manifest and Artifact Hashing

**ID:** `ACP-BA-014`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-013`

## Objective

Produce an ACP-reviewable evidence manifest for every execution.

## Required Work

1. Define versioned evidence-manifest JSON Schema.
2. Include:
   - work-order ID and SHA-256 hash;
   - framework version;
   - policy reference and hash;
   - ordered step IDs and outcomes;
   - acceptance-criterion mappings;
   - artifact paths, types, sizes, and hashes;
   - redaction status;
   - terminal state.
3. Normalize timestamps/volatile fields for deterministic test mode.
4. Hash files using streamed reads.
5. Reject missing or changed artifacts during manifest verification.
6. Add a verifier function used by CI and final review packaging.

## Deterministic Tests

```bash
<unit-command> -- evidence-manifest
<integration-command> -- evidence-manifest
<schema-check-command>
```

## Definition of Done

- Manifest validates against schema.
- Every artifact hash is reproducible.
- Tampered and missing artifacts are detected.
- Acceptance-criterion IDs map to concrete evidence.
- Slarti starts Child 15.

---

# Child 15 — Implement Central Redaction and Sensitive Artifact Controls

**ID:** `ACP-BA-015`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-014`

## Objective

Apply one central redaction policy to structured logs, results, errors, artifact metadata, screenshots, traces, and retained HTML snippets.

## Required Work

1. Create a redaction service accepting registered secret values and configured field-name patterns.
2. Redact recursively in structured values.
3. Redact diagnostics before serialization.
4. Define screenshot and trace policy states: `disabled`, `allowed`, `sensitive-denied`.
5. Default traces and screenshots to disabled unless the work order and policy both allow them.
6. Ensure artifacts marked sensitive cannot be retained accidentally.
7. Add probe tests covering direct, nested, repeated, and URL-encoded secret appearances where technically feasible.

## Deterministic Tests

```bash
<unit-command> -- redaction
<conformance-command> -- secret-leakage
```

## Definition of Done

- Probe secrets are absent from all searchable test outputs.
- Screenshot/trace capture fails closed under sensitive policy.
- Redaction behavior is deterministic and documented.
- No component implements its own conflicting redaction path.
- Slarti starts Child 16.

---

# Child 16 — Implement the Execution Orchestrator

**ID:** `ACP-BA-016`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-015`

## Objective

Compose validation, policy, secrets, lifecycle, step execution, artifacts, redaction, result production, and cleanup into one deterministic execution pipeline.

## Required Work

1. Implement ordered phases:
   1. read input;
   2. validate schema/version;
   3. normalize;
   4. policy preflight;
   5. create confined execution directory;
   6. resolve required secrets;
   7. launch browser/context;
   8. execute steps;
   9. collect/redact artifacts;
   10. write result/evidence;
   11. cleanup.
2. Ensure failures in each phase map to Child 04 contracts.
3. Ensure no later phase runs after a terminal earlier failure.
4. Ensure cleanup runs after every phase that allocates resources.
5. Inject clock, ID generator, filesystem root, launcher, policy, resolver, and logger.
6. Add orchestration tests using fakes plus one local-browser path.

## Deterministic Tests

```bash
<unit-command> -- orchestrator
<integration-command> -- orchestrator
```

## Definition of Done

- Phase order is explicit and tested.
- Short-circuit behavior is proven.
- Cleanup occurs on every injected failure.
- Final result and evidence remain schema-valid.
- Slarti starts Child 17.

---

# Child 17 — Implement the Stable CLI Surface

**ID:** `ACP-BA-017`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-016`

## Objective

Expose the orchestrator through a machine-oriented CLI suitable for Slarti, Lydia, CI, and future Eddie scheduling.

## Required Work

1. Support work-order input from a file and stdin.
2. Support explicit policy file/reference input.
3. Support execution-root configuration through approved CLI/config mechanisms.
4. Emit exactly one final JSON result to stdout in machine mode.
5. Send redacted diagnostics to stderr.
6. Return Child 04 exit codes.
7. Add `--version`, `--help`, and `validate` modes.
8. Reject conflicting input modes and unknown options.
9. Avoid interactive prompts.

## Deterministic Tests

```bash
<unit-command> -- cli-contract
<integration-command> -- cli
```

Required cases: valid file, valid stdin, malformed JSON, unsupported version, denied policy, missing secret, browser failure fake, successful local fixture execution, unknown option, and broken pipe/error handling if repository tooling supports it.

## Definition of Done

- Stdout is parseable as exactly one JSON result.
- Exit codes match documentation.
- CLI is non-interactive.
- Help/version do not launch Chromium.
- Slarti starts Child 18.

---

# Child 18 — Add Security and Conformance Test Suite

**ID:** `ACP-BA-018`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-017`

## Objective

Create a named conformance suite proving critical ACP Browser Automation invariants.

## Required Work

1. Create test groups for:
   - schema strictness;
   - unsupported action rejection;
   - origin bypass rejection;
   - redirect escape blocking;
   - action-policy denial;
   - validation-before-launch;
   - secret non-leakage;
   - artifact path confinement;
   - download limits;
   - ephemeral context isolation;
   - deterministic exit/result mapping;
   - evidence tamper detection;
   - no public-network dependency.
2. Add a machine-readable conformance result artifact.
3. Ensure each test maps to an epic security or architecture requirement.
4. Add a network guard in tests where feasible to fail unexpected non-loopback connections.

## Deterministic Tests

```bash
<conformance-command>
<verify-command>
```

## Definition of Done

- Every named invariant has at least one positive or negative proof as appropriate.
- Conformance output is machine-readable.
- Public network access is unnecessary and blocked/detected in the suite.
- Full suite passes twice consecutively.
- Slarti starts Child 19.

---

# Child 19 — Add CI Gates, Packaging, and Documentation

**ID:** `ACP-BA-019`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-018`

## Objective

Make the framework reproducibly verifiable by CI and operable by developers and the Operator without deploying it.

## Required Work

1. Add or extend CI with mandatory gates for:
   - format check;
   - lint;
   - strict typecheck;
   - schema validation;
   - unit tests;
   - integration tests with Chromium;
   - conformance tests;
   - production build;
   - dependency audit according to repository policy;
   - secret scan;
   - generated-tree cleanliness.
2. Pin CI actions/images according to repository policy.
3. Cache dependencies without caching secrets or runtime artifacts.
4. Add developer documentation.
5. Add CLI reference, policy guide, work-order examples, security model, artifact-retention guidance, and troubleshooting.
6. Add Operator runbook for validation-only local execution.
7. Add packaging/container configuration only if Child 01 selected it as repository standard.
8. Do not deploy or schedule the framework.

## Deterministic Tests

```bash
<verify-command>
<documentation-check-command>
git diff --exit-code
```

Where local CI emulation is available, run the relevant workflow validation tool.

## Definition of Done

- Every mandatory gate exists and fails closed.
- Documentation examples validate against schemas.
- Fresh-clone verification instructions are complete.
- No production deployment is performed.
- Slarti starts Child 20.

---

# Child 20 — Assemble Final ACP Review Package and Integration PR

**ID:** `ACP-BA-020`  
**Estimated effort:** 45–60 minutes  
**Depends on:** `ACP-BA-019`

## Objective

Run final verification, assemble deterministic ACP evidence, and open exactly one final integration PR for ChatGPT review.

## Required Work

1. Rebase or update the feature branch according to repository policy without rewriting accepted evidence incorrectly.
2. Run the complete verification suite from a clean checkout or equivalent clean working tree.
3. Record:
   - final head SHA;
   - all Child Issue accepted commit SHAs;
   - command list and exit codes;
   - CI run identifiers when available;
   - acceptance criteria to evidence mapping;
   - architecture decisions and deviations;
   - security analysis;
   - artifact inventory and checksums;
   - known limitations;
   - rollback instructions;
   - Operator validation procedure.
4. Create the review package at the canonical ACP path from Child 01.
5. Validate the package with the evidence verifier.
6. Confirm zero plaintext secrets and zero unexpected generated changes.
7. Open exactly one final integration PR targeting the protected default branch.
8. Mark the PR ready for ChatGPT ACP review only after CI is green.
9. Do not enable merge or merge the PR.

## Required Review Package

```text
review-package.yaml
child-issue-matrix.md
acceptance-evidence.yaml
ci-evidence.json
security-review.md
artifact-manifest.json
rollback.md
known-limitations.md
operator-validation.md
```

## Deterministic Tests

```bash
<install-command>
<verify-command>
<review-package-validation-command>
git diff --exit-code
git status --porcelain
```

## Definition of Done

- All 20 Child Issues are recorded complete in order.
- Full verification passes from a clean state.
- Review package validates and is bound to the final head SHA.
- Exactly one final integration PR exists.
- The PR is not merged.
- ChatGPT is identified as final ACP reviewer.
- Eddie is identified as merge authority after current-SHA approval.
- Any commit after ChatGPT approval invalidates that approval.

---

## Consecutive Automation State Machine

```yaml
apiVersion: acp.homelab/v1alpha1
kind: ConsecutiveChildExecution
metadata:
  epicId: ACP-EPIC-BROWSER-PLAYWRIGHT
spec:
  branchMode: single-feature-branch
  subagent:
    model: deepseek-v4-flash-free
    freshContext: true
    maxChildrenPerInvocation: 1
  progression:
    order:
      - ACP-BA-001
      - ACP-BA-002
      - ACP-BA-003
      - ACP-BA-004
      - ACP-BA-005
      - ACP-BA-006
      - ACP-BA-007
      - ACP-BA-008
      - ACP-BA-009
      - ACP-BA-010
      - ACP-BA-011
      - ACP-BA-012
      - ACP-BA-013
      - ACP-BA-014
      - ACP-BA-015
      - ACP-BA-016
      - ACP-BA-017
      - ACP-BA-018
      - ACP-BA-019
      - ACP-BA-020
    continueWhen:
      deterministicTestsExitCode: 0
      slartiReview: accepted
      outOfScopeChanges: 0
      secretsDetected: 0
      definitionOfDone: true
    stopWhen:
      deterministicTestsExitCode: nonzero
      slartiReview: rejected
      outOfScopeChanges: greater-than-zero
      secretsDetected: greater-than-zero
      definitionOfDone: false
  pullRequests:
    childIssuePRs: 0
    finalIntegrationPRs: 1
  finalReview:
    reviewer: chatgpt
    shaBound: true
  merge:
    actor: eddie
    requiresCurrentShaApproval: true
```
