# Architecture Agent Instructions At Review Head

Source: `Homelab/Architecture/AGENTS.md` at
`8d5d556344c3d3891eb27da785f3a4f8e09b4b32`.

## Review Contract

- Pull requests are the review object. Issues are the work journal and control
  channel; issue evidence never substitutes for pull-request review.
- Before waiting, publish exactly `waiting_for_pr_review` or
  `waiting_for_issue_review`.
- Implementation evidence includes `instruction_file`, `instruction_commit`,
  `instruction_reloaded`, `pr_head_commit`, `changed_files`, `ci_run_ids`, and
  `review_target: pr`.
- Externally fact-based PRs remain draft until the current head is reviewed.
- Eddie or the operator merges after review; the implementation agent does not.
- Changed instructions must be fetched and reread before continuing.

## Change Rules

- One branch and PR per issue.
- `ci-manifest.yaml` is the source of truth; generated CI files are regenerated.
- New contract tests run in PR CI.
- Run `make lint`, `make test`, and `git diff --check` before review.
- Never commit credentials, cookies, registrations, or runtime data.
- Repository preparation and live deployment are separate scopes.
