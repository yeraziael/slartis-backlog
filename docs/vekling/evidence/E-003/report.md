# E-003: Capability-Informed GH-24 Hy3 Invocation

Date: 2026-07-19

GH-24 was executed by one fresh `opencode/hy3-free` worker using the versioned
skills discovered in E-001. The worker satisfied the lifecycle gate, loaded all
six requested skills, changed one permitted file, ran the requested local
checks, created one Gitea PR, and did not start GH-25 or another subagent.

The delivery was not review-acceptable. Primary-source review found that the
ADR named v26.06 as the latest release even though v26.07 had been released on
2026-07-16. More importantly, v26.07 split Instagram into the separate
`mautrix-instagram` bridge, invalidating the ADR's current same-binary model.
Several resource, policy-risk, database, and namespace statements also exceeded
the cited evidence.

Eddie merged PR #36 automatically after CI passed and before reviewer
acceptance. The same worker session initially stopped because the assigned PR
had already merged. After explicit operator authorization, it later created
draft corrective PR #37 at commit `23e8f0a`; both PR CI runs are green. GH-24
remains open and PR #37 remains draft and unmerged for a future implementation
review.

## Measured Results

- Prompt: 599 words, 4,592 bytes, SHA-256 recorded in `measurement.json`.
- Model/session: dedicated Hy3 Free session, independently confirmed in the
  OpenCode session database.
- Initial execution wall span: 99.657 seconds.
- Clarifications: 0.
- Gate violations: 0.
- Committed unrelated files: 0.
- Transient unrelated tracked mutations: 1, cleaned.
- Initial unsupported-assumption claim: 0; reviewer correction items: 9.
- Worker user turns: 8 total, including 7 continuation/review/runtime turns.
- PR CI: success; merge occurred before review acceptance.
- Console contract: failed; captured output was 4,714 words / 55,701 bytes.
- Observed credential-value pattern matches in captured worker output: 0.
- A broad orchestrator process listing exposed one credential from another
  process's command-line arguments. The value is not copied into research
  artifacts; redaction and rotation were handed to issue #17.
- Replacement: Gitea PR #37, draft, CI run 515 successful, not merged.

## Protocol Findings

1. Skill references and a shorter task payload preserved gate, scope, and
   credential-host separation behavior.
2. `current primary sources` was not sufficient to ensure release freshness.
   Prompts should require an explicit latest-release endpoint or tag check for
   time-sensitive vendor claims.
3. Green documentation CI did not validate external factual currency.
4. Auto-merge must be held until reviewer acceptance, not merely CI success.
5. Validation must end with a clean-worktree check because the repository test
   suite modifies a tracked Python bytecode file.
6. Console suppression remained ineffective despite an explicit output
   contract.
7. The same-worker stop rule worked correctly after the PR became stale.
8. With this CLI version, positional text must precede the array-valued
   `--file` option or the text is parsed as another file path.
9. A resumed OpenCode session retained its original directory even when the
   continuation command supplied a different `--dir`; the replacement worktree
   remained an external directory.
10. The apparent worker hang was first a `waiting_permission` state for
    `external_directory`, not blocked model inference.
11. A later no-output run selected Hy3 successfully, denied the replacement
    worktree, advanced its loop, and emitted `exiting loop` without an error or
    deliverable. Clean loop exit is therefore not delivery success.
12. OpenCode 1.17.20 documentation says `--auto` approves ASK requests unless
    explicitly denied, but the resumed session still waited for the credential
    directory. The cause is unknown and requires a focused reproduction.
13. Lifecycle monitoring must consume provider, permission, tool, loop-exit,
    and deliverable events rather than infer state from elapsed silence.

## Handoff

- GH-24 and draft Gitea PR #37: future documentation review and merge decision.
- GitHub issue #32: implement a permission-aware Vekling lifecycle monitor.
- GitHub issue #33: gate Eddie auto-merge on reviewer acceptance for research
  and other externally sourced documentation.
- GitHub issue #17 comment: add process-command-line credential exposure to the
  redaction scope and rotate the affected credential through its owner.

The exact initial and corrective prompts, sanitized runtime events, and
machine-readable measurements are stored beside this report. Architectural
consequences are captured in
`docs/vekling/adr/001-session-resume-and-worker-monitoring.md`.
