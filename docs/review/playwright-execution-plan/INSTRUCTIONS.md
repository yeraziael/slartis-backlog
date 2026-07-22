# Independent Review Instructions

## Authoritative Inputs

- Playwright Plan-as-Code: `docs/epics/playwright/` at PR #82 head.
- Exact internal issue contracts: `tickets/` and `tickets.json` in this package.
- ACP: `Homelab/ACP` version `0.1.0-draft`; `SPEC/` is empty.
- Accepted ACP Pilot 57 findings: deterministic review package, evidence-to-AC
  mapping, transport validation, explicit missing-artifact handling, SHA-bound
  review.
- Architecture execution instructions: `Homelab/Architecture/AGENTS.md`.

## Review Checklist

- [ ] All Plan-as-Code backlog/requirement groups map to execution tickets.
- [ ] Every implementation ticket is one focused session and one pull request.
- [ ] Low-cost tickets require no architectural invention.
- [ ] Every unresolved architecture question has a Sol-only decision ticket.
- [ ] Dependencies prevent premature service, identity, CI and artifact work.
- [ ] PW-I01 through PW-I05 are the exact first implementation cohort.
- [ ] The checkpoint blocks PW-I06 until independent review is complete.
- [ ] ACP evidence and ten-category findings records are complete per ticket.
- [ ] Generic ACP candidates are separated from domain-specific learning.
- [ ] Reviewer notification does not turn GitHub into the execution tracker.
- [ ] No `Homelab/Architecture` implementation or runtime mutation is present.

## Verdict

Review the exact GitHub PR head SHA. Use `APPROVED` or `CHANGES_REQUESTED` when
available. A later push invalidates the verdict and requires re-review.
