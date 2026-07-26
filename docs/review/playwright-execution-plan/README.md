# Review Package: Playwright Execution Plan

## Review Decision Requested

Review the control-plane decomposition of the Playwright Plan-as-Code epic and
record approval or requested changes on the v2-amendment pull request. The
historical exact Gitea snapshot remains unchanged; `FREEZE_V2_AMENDMENT.md`
supersedes only its reviewer/merge clauses and stale authority facts.

## Source

- Planning repository: `yeraziael/slartis-backlog`
- Planning path: `docs/epics/playwright/`
- Planning merge: `#82` / `7ae8e1cd468f4f9543f5c3e2ccdd0df05ba68b2b`
- Internal execution parent: `slarti/backlog#253`
- Snapshot range: `#253-#281`
- Gitea ticket snapshot SHA-256: `93e483fb33ae235c9c3e1b3400b3e9d3fbdb5a4eaf8ab78dcf7e8c6bceb9d62f`
- Implementation repository inspected: `Homelab/Architecture@a3b926bc16c6835eb0ae1ca8a9ca087ee5b4583d`
- ACP authority: stable `Homelab/ACP v0.3.0`, peeled commit `7768e129b3fdc48ebf69ebd888225d2c37af0c71`

## Package Files

- `EXECUTION_PLAN.md`: decomposition, dependencies, ordering, model allocation,
  checkpoint, mapping, assumptions and open questions.
- `tickets/`: one exact Markdown snapshot per internal Gitea issue.
- `tickets.json`: machine-readable exact issue snapshot.
- `FROZEN_PLAN.md`: final graph, ordering, model allocation, checkpoint,
  first-five complexity assessment, and reviewer workflow.
- `FREEZE_V2_AMENDMENT.md`: operator authority and exact self-verification /
  self-merge supersession contract.
- `REVIEW_DISPOSITION.md`: classification of every independent review point.
- `manifest.json`: provenance, inventory and mutation declaration.
- `INSTRUCTIONS.md`: review boundary and checklist.
- `TESTING.md`: package validation evidence.
- `CI.json`: CI/check evidence for this review surface.
- `NOTES.md`: scope, risks and exclusions.

## Authorization Boundary

Approval activates only the v2 amendment. The Operator's separately recorded
standing authorization permits ticket execution and exact-head merges. It does
not authorize deployment, account/secret changes, DNS, or runtime mutation.
