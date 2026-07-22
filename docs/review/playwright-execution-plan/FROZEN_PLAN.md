# Frozen Playwright Execution Plan

## Freeze Record

- Freeze identifier: `playwright-execution-plan-v1`.
- State: `FROZEN_AWAITING_FINAL_REVIEW_AND_OPERATOR_APPROVAL`.
- Independent review: PR #83 review `4756629751`, reviewed head
  `274ad202a8319728fc610870c92a3a79d19c22b9`.
- Gitea ticket snapshot SHA-256: `93e483fb33ae235c9c3e1b3400b3e9d3fbdb5a4eaf8ab78dcf7e8c6bceb9d62f`.
- Hash domain: canonical UTF-8 JSON serialization of `tickets.json` using
  sorted object keys and separators `(comma, colon)`.
- No implementation has begun. No ticket is ready before final SHA-bound review
  and explicit operator approval.
- After approval, PW-D01 is first executable; PW-I01 remains blocked by PW-D01
  and the canonical-plan default-branch merge gate.

Any ticket-body, dependency, model, checkpoint, evidence, or reviewer-workflow
change invalidates this freeze and requires a regenerated snapshot and new
SHA-bound review.

Reproduce the Gitea ticket snapshot SHA-256 from the repository root:

```bash
python3 -c 'import hashlib,json,pathlib; p=pathlib.Path("docs/review/playwright-execution-plan/tickets.json"); data=json.loads(p.read_text(encoding="utf-8")); canonical=json.dumps(data,sort_keys=True,separators=(",", ":")).encode("utf-8"); print(hashlib.sha256(canonical).hexdigest())'
```

## Final Dependency Graph

```text
PW-D01 -> PW-D02
PW-D01 -> PW-I01 -> PW-I02
PW-D02 + PW-I02 -> PW-I03 -> PW-I04 -> PW-I05
PW-I01..PW-I05 -> PW-ACP-CP1
PW-ACP-CP1 -> PW-D03 -> PW-I06 -> PW-I07 -> PW-I08
PW-I08 -> PW-D04 -> PW-I09 -> PW-I10 -> PW-I11
PW-I11 -> PW-D05 -> PW-I12 -> PW-I13 -> PW-I14 -> PW-I15
PW-I15 -> PW-I16 -> PW-I17 -> PW-I18
PW-I17 + PW-D06 -> PW-I19 -> PW-I20 -> PW-I21
```

The exact dependency fields in the ticket snapshots are authoritative. The
diagram is a review aid and does not relax any prerequisite.

## Final Execution Order

`operator approval -> PW-D01 -> PW-D02 -> PW-I01 -> PW-I02 -> PW-I03 -> PW-I04 -> PW-I05 -> PW-ACP-CP1 -> PW-D03 -> PW-I06 -> PW-I07 -> PW-I08 -> PW-D04 -> PW-I09 -> PW-I10 -> PW-I11 -> PW-D05 -> PW-I12 -> PW-I13 -> PW-I14 -> PW-I15 -> PW-I16 -> PW-I17 -> PW-I18 -> PW-D06 -> PW-I19 -> PW-I20 -> PW-I21`

Execution is serial by default. No parallel branch may start unless the parent
index is explicitly amended and independently re-reviewed.

## Final First Five Implementation Tickets

| Ticket | Objective | Dependencies | Expected deliverable | Recommended model | Model rationale | Implementation complexity | Review complexity |
|---|---|---|---|---|---|---|---|
| PW-I01 | Create the minimal pinned Playwright project and ephemeral runner bootstrap. | PW-D01; canonical plan merged to the default branch | Pinned package/lock/config/runner/README, bootstrap contract test, and generated CI registration. | DeepSeek V4 Flash Free | The image, package, path, and invocation decisions are externalised to PW-D01; remaining work is deterministic repository scaffolding. | Medium | Medium |
| PW-I02 | Prove Chromium startup and clean browser context isolation. | PW-I01 | Controlled local-page self-test, exact fixture, and pass/fail cleanup evidence. | DeepSeek V4 Flash Free | The test surface is isolated, local, and fully specified; no service or architecture choice remains. | Low-Medium | Low-Medium |
| PW-I03 | Implement deterministic result and exit-code semantics. | PW-I02; PW-D02 | Runner result types/wrapper plus fixtures for pass, assertion failure, prerequisite error, runner error, and mixed precedence. | DeepSeek V4 Flash Free | PW-D02 fixes the only semantic choice; implementation is a bounded state/exit mapping with deterministic fixtures. | Medium | Medium-High |
| PW-I04 | Generate and validate a versioned evidence manifest bound to trusted provenance. | PW-I03; PW-D02 | JSON schema, generator, validator, positive/negative fixtures, and acceptance-criterion evidence mapping. | DeepSeek V4 Flash Free | Trusted sources and result precedence are fixed by PW-D02; the remaining schema implementation is explicit and testable. | Medium | High |
| PW-I05 | Implement generic prerequisite classification and a fail-closed suite gate. | PW-I04 | Composable DNS/TLS/HTTPS/Keycloak checks, orchestrator, deterministic local fixtures, and manifest integration. | DeepSeek V4 Flash Free | All checks, result semantics, and failure behavior are enumerated; no live service or policy invention is permitted. | Medium | High |

## Final Sol-Only Decision Tickets

| Ticket | Gitea | Rationale |
|---|---:|---|
| PW-D01 | #254 | Selects immutable image, package manager, versions and invocation contract before bootstrap code. |
| PW-D02 | #255 | Defines trusted provenance sources and mixed-result precedence before evidence implementation. |
| PW-D03 | #262 | Resolves trace sanitisation feasibility and Gitea retention mechanics before artifact publication. |
| PW-D04 | #266 | Fixes realm, role membership and password handoff boundaries before provisioning code. |
| PW-D05 | #270 | Pins Audiobookshelf journeys, selectors and controlled data so service executors do not explore live UI architecture. |
| PW-D06 | #278 | Confirms Jellyfin readiness, identities, selectors and controlled media before second-service adoption. |

Sol decisions produce bounded decision documents only. They do not implement
the platform or perform runtime changes.

## Final Low-Cost Model Tickets

| Ticket | Gitea | Objective | Recommended model |
|---|---:|---|---|
| PW-I01 | #256 | Bootstrap pinned ephemeral runner project | DeepSeek V4 Flash Free |
| PW-I02 | #257 | Add platform self-test and browser isolation | DeepSeek V4 Flash Free |
| PW-I03 | #258 | Implement deterministic execution and result semantics | DeepSeek V4 Flash Free |
| PW-I04 | #259 | Implement evidence manifest schema and generator | DeepSeek V4 Flash Free |
| PW-I05 | #260 | Implement prerequisite classification and fail-closed gate | DeepSeek V4 Flash Free |
| PW-I06 | #263 | Implement failure-only screenshot and trace capture | DeepSeek V4 Flash Free |
| PW-I07 | #264 | Implement evidence sanitisation publication gate | DeepSeek V4 Flash Free |
| PW-I08 | #265 | Implement evidence bundle and retention metadata | DeepSeek V4 Flash Free |
| PW-I09 | #267 | Add synthetic Audiobookshelf identity provisioning contract | DeepSeek V4 Flash Free |
| PW-I10 | #268 | Add shared service, role and console fixtures | DeepSeek V4 Flash Free |
| PW-I11 | #269 | Implement shared Keycloak OIDC authentication fixture | DeepSeek V4 Flash Free |
| PW-I12 | #271 | Add Audiobookshelf unauthenticated smoke flow | DeepSeek V4 Flash Free |
| PW-I13 | #272 | Add Audiobookshelf authenticated login and logout smoke | DeepSeek V4 Flash Free |
| PW-I14 | #273 | Add Audiobookshelf controlled library and playback flow | DeepSeek V4 Flash Free |
| PW-I15 | #274 | Add Audiobookshelf role and negative authorization tests | DeepSeek V4 Flash Free |
| PW-I16 | #275 | Integrate Playwright pre-merge CI gates | DeepSeek V4 Flash Free |
| PW-I17 | #276 | Integrate post-deployment smoke, retry and ACP handoff | DeepSeek V4 Flash Free |
| PW-I18 | #277 | Codify Playwright maintenance and flake operations | DeepSeek V4 Flash Free |
| PW-I19 | #279 | Add Jellyfin unauthenticated smoke flow | DeepSeek V4 Flash Free |
| PW-I20 | #280 | Add Jellyfin authentication and role coverage | DeepSeek V4 Flash Free |
| PW-I21 | #281 | Add Jellyfin controlled media and playback flow | DeepSeek V4 Flash Free |

## Final ACP Checkpoint Definition

`PW-ACP-CP1` activates only after PW-I01 through PW-I05 are merged and
independently reviewed at exact PR head SHAs. Decision tickets do not count.
The checkpoint blocks every PW-I06-or-later branch, edit, delegation, or retry.

It evaluates task self-containment, model selection, acceptance evidence,
failure classification, retries, escalation, model limitations, and process
friction. It records one disposition: `no change`, `clarification`,
`backward-compatible refinement`, or `breaking revision`, followed by `release`
or `hold`. Playwright-specific findings remain domain records. Generic ACP
candidates require a separate versioned `Homelab/ACP` work item.

## Final Reviewer Workflow

1. Gitea remains authoritative for execution state, retries, findings, and
   operational history.
2. Each implementation PR posts one final Gitea evidence comment containing the
   instruction commit, PR head, exact files, commands/results, CI run IDs,
   acceptance-evidence mapping, mutation declaration, rollback, and all ten
   finding categories.
3. Transport validation confirms PR URL, exact head SHA, changed files, CI, and
   evidence are accessible before `WAITING_FOR_PR_REVIEW`.
4. GitHub receives one concise review notification with internal ticket, Gitea
   PR/head SHA, scope, tests/CI, ACP evidence location, and findings summary. It
   does not receive a duplicate execution backlog.
5. Independent review is SHA-bound. Any push invalidates the verdict.
6. Review prioritises ticket-contract compliance, model routing, ACP checkpoint
   quality, and evidence generation. Playwright-specific detail is examined only
   where it affects an authoritative requirement or security boundary.
7. Approval authorizes that ticket's merge gate only. Deployment, secrets,
   accounts, DNS, and runtime mutation require separate operator authority.

## Final Self-Containment Validation

- Hidden architectural decisions in low-cost tickets: none. Image/provenance,
  artifact security, identity, Audiobookshelf onboarding, and Jellyfin onboarding
  are isolated in PW-D01 through PW-D06.
- Contract-alone execution: PASS. Every low-cost ticket names its prerequisite
  decision outputs, exact scope, paths, commands, acceptance evidence, rollback,
  and escalation behavior.
- ACP evidence sufficiency: PASS. Every child ticket contains phase transitions,
  mandatory evidence, ten finding categories, blocker rules, and SHA binding.
- Repository-wide exploration: forbidden. Every low-cost ticket is constrained
  to enumerated files or a narrow service/platform subtree.
- One-session scope: PASS. Each low-cost ticket has one primary concern and one
  PR deliverable; cross-cutting architecture is resolved before execution.

## Remaining Open Questions

- PR #82 must merge before PW-I01.
- PW-D01 resolves exact runner image/package/invocation.
- PW-D02 resolves provenance and mixed-result precedence.
- PW-D03 resolves trace sanitisation and retention enforcement.
- PW-D04 resolves synthetic identity and secret handoff.
- PW-D05 resolves Audiobookshelf selectors and controlled data.
- PW-D06 resolves Jellyfin readiness, selectors, identities, and controlled media.

These are explicit decision-ticket questions, not hidden low-cost work.
