# E-003 Research Notes

## Validated Facts

- The GH-24 worker ran as `opencode/hy3-free` in dedicated session
  `ses_086bdc63cffeLD2XhNyr6qJvFz`.
- Provider/runtime initialization succeeded before every investigated silent
  state.
- The worker produced one flawed ADR PR (#36), which green CI did not protect
  from stale external facts and Eddie merged before reviewer acceptance.
- The same session respected the stale-PR stop rule after PR #36 merged.
- A resumed session retained its original directory; a replacement `--dir` did
  not rebind the session workspace.
- A pending `external_directory` request caused one apparent hang.
- Denied replacement-worktree access caused another run to exit cleanly without
  an error or deliverable.
- Explicit replacement-worktree permission allowed the same session to produce
  draft corrective PR #37. CI run 515 succeeded; the PR remains unmerged.
- Full process-table inspection can copy secrets from other processes' command
  lines into captured tool output. No credential value is stored in these
  artifacts.

## Rejected Hypotheses

- Hy3 was stalled inside model inference.
- The OpenCode provider was unavailable.
- The later no-output run was still waiting for permission.
- A clean `exiting loop` event implied successful task completion.
- Green documentation CI established external factual correctness.

## Hypotheses Requiring Focused Tests

- The resumed-session `--auto` permission behavior may be an OpenCode 1.17.20
  implementation defect or a resume-path propagation defect.
- Exact credential-file allow rules may not satisfy requests normalized to a
  parent wildcard.
- `--dir` on a resumed session may need a warning or hard error because its
  apparent workspace override is misleading.

## Recommendations

- Implement issue #32 before relying on timeout-only worker monitoring.
- Implement issue #33 before restoring CI-only auto-merge for research ADRs.
- Keep corrective research PRs draft until factual review accepts their current
  head SHA.
- End every validation sequence with a clean-worktree check.
- Update issue #17's redaction scope and rotate the exposed Paperless credential
  through its owner.
