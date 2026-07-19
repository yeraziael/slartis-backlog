Execute exactly GitHub backlog issue GH-24 in one fresh Hy3 worker session.

Operator approval: the operator explicitly approved this single Hy3 Vekling start in the parent request. Do not start subagents.

issue:
- Authoritative task: https://github.com/yeraziael/slartis-backlog/issues/24, including all comments.
- Scope: research and one ADR deciding Facebook Messenger bridge feasibility only. Do not work on GH-25 or any other issue.

repositories:
- Backlog/research target: https://github.com/yeraziael/slartis-backlog
- Implementation: https://gitea.hl.maier.wtf/Homelab/Architecture
- Absolute implementation worktree: /tmp/opencode/architecture-gh24
- Base: origin/main at b58d5df61375d01fa93fa7258bb743eb790ddf93
- Assigned branch: docs/gh-24-facebook-bridge
- Permitted implementation file: docs/adr/002-facebook-messenger-bridge.md
- Credentials: select only by target hostname from ~/.creds; never guess, print, persist, or place credentials in URLs.

gate:
- Requires GitHub GH-23 closed with reviewer approval and its Gitea implementation PR #34 merged.
- The reviewer observed GH-23 closed, approval in its final reviewer comment, Gitea PR #34 merged by Eddie at merge commit f273d6a5e40aba2e110a336ab4417dec625f3b13, and successful PR CI run 506.
- Independently reverify all gate elements immediately before any mutation. Keep GitHub issue numbers and Gitea PR numbers as separate namespaces. If any element fails, report and stop without mutation.

required_skills:
- Load and use: adr, architecture, github-cli, gitea, vekling-delegation, communication.
- Use the GitHub issue body/comments as the task contract. Inspect the local implementation worktree before remote/API research.

task-specific overrides:
- Research current primary sources for mautrix-meta/Facebook Messenger maintenance status, official ARM64 image availability, authentication/user flow, known limitations, account-ban/ToS risk, E2EE behavior, Pi 5 resource implications, compatibility with the merged bridge_internal appservice pattern, and joint Facebook/Instagram operation.
- Record source URL, access date 2026-07-19, version/tag/commit when available, and the exact supported finding. Unknown is preferred over inference. Do not present unsupported resource estimates or platform-policy claims as facts.
- Decision must be exactly one of: implement, implement_with_instagram, do_not_implement. Include rationale, risks, limitations, and operational/resource consequences.
- Repository mutation is ADR-only. No runtime, Synapse, container, deployment, service, network, secret, token, DNS, firewall, or production changes.
- If and only if the reviewed research decision is positive, report the proposed follow-up issue title/body in the final result; do not create or execute that follow-up before reviewer acceptance.
- Before editing, confirm there is no existing open/merged PR or conflicting branch for GH-24. Use the assigned branch and existing worktree; do not create another branch or worktree.
- Allowed: edit the one permitted ADR, validate, commit, push the assigned branch, create exactly one Gitea PR targeting main, inspect CI, and comment structured evidence on GH-24.
- Forbidden: merge, close GH-24, force-push, modify unrelated files, start GH-25, or create a replacement PR if automation closes/merges the assigned PR.

validation:
- Working directory for every command: /tmp/opencode/architecture-gh24
- Run `git diff --check` before commit.
- Run `make lint` and `make test` locally; report exact exit status. Do not relabel structural inspection as command execution.
- After push, verify Gitea PR head SHA, changed-file list, and required Gitea Actions CI state. If CI is still running, report it as pending rather than green.

research measurement contract:
- In the final report, record clarification_count, unsupported_assumption_count, gate_compliance, unrelated_change_count, corrective_prompt_count (initially 0), measured elapsed_seconds if available, and usage scope only if isolated to this run. Never label aggregate ccusage data as session-specific.
- Measurement is protocol metadata for later versioned persistence by the reviewer; do not add it to the implementation PR and do not mutate the backlog repository for it.

output:
- Keep console output to phase lines, blockers, and final JSON only.
- Final JSON fields: state, issue, gate, loaded_skills, branch, commit, pr, adr_path, decision, changed_files, sources, commands, ci, limitations, proposed_followup, measurement.
- Stop after the existing GH-24 PR and evidence comment are ready for review.
