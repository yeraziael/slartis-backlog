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
acceptance. The same worker session received one corrective prompt, verified
that the PR had already merged, cleaned its transient tracked `__pycache__`
change, and stopped without creating an unauthorized replacement PR. GH-24
remains open with a `changes_required` reviewer result.

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
- Corrective prompts: 1, to the same session.
- PR CI: success; merge occurred before review acceptance.
- Console contract: failed; captured output was 4,714 words / 55,701 bytes.
- Observed credential-value pattern matches in captured worker output: 0.

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

The exact initial and corrective prompts are stored beside this report.
