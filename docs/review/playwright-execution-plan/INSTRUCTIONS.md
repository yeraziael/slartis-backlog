# v2 Amendment Review Instructions

## Authoritative Inputs

- Playwright Plan-as-Code: `docs/epics/playwright/` on `main` after PR #82.
- Exact internal issue contracts: `tickets/` and `tickets.json` in this package.
- ACP: stable `v0.3.0`, including review-provenance v2 semantics.
- Architecture execution instructions: `Homelab/Architecture/AGENTS.md`.

## Review Checklist

- [ ] All Plan-as-Code backlog/requirement groups map to execution tickets.
- [ ] Every implementation ticket is one focused session and one pull request.
- [ ] Low-cost tickets require no architectural invention.
- [ ] Every unresolved architecture question has a Sol-only decision ticket.
- [ ] Dependencies prevent premature service, identity, CI and artifact work.
- [ ] PW-I01 through PW-I05 are the exact first implementation cohort.
- [ ] The checkpoint blocks PW-I06 until the first five exact-head
  self-verifications and aggregate checkpoint are complete.
- [ ] ACP evidence and ten-category findings records are complete per ticket.
- [ ] Generic ACP candidates are separated from domain-specific learning.
- [ ] Reviewer notification does not turn GitHub into the execution tracker.
- [ ] No `Homelab/Architecture` implementation or runtime mutation is present.

## Verdict

Review the exact v2-amendment PR head SHA. This one-time review remains native
independent review because it changes the frozen reviewer workflow. A later
push invalidates the verdict and requires re-review.
