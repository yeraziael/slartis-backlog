# ADR-002: Review Provenance and Self-Verification Semantics

**Status:** Proposed
**Date:** 2026-07-25

## Context

During the ACP v0.2 review cycle (PR #91 mirror in
`yeraziael/slartis-backlog`), a governance weakness was discovered:

1. A self-review verdict used the term "approved" and "authoritative ACP
   verdict", implying independent review authority that the author did not
   possess.
2. The verdict referenced an outdated commit SHA but was not re-issued after
   fixes.
3. The review history did not accurately reflect the progression: an initial
   self-review claimed "approved" before all external findings were resolved.
4. Later fixes were not represented by a final verification tied to the merged
   commit.

This weakens auditability because a future observer cannot determine from the
review record alone which commits were reviewed, by whom, and with what
authority.

Pilot 57 and the ACP v0.1 conventions did not formalize review types, commit
binding, or supersession. The existing `github-review` skill in
`yeraziael/ai-governance` defines a review procedure but does not distinguish
self-verification from independent review at the schema level.

## Decision

Add a normative Review Provenance specification (`SPEC/review-provenance.md`)
to ACP v0.3.0-draft with the following elements:

1. **Three disjoint review types**: `independent`, `self-verification`,
   `post-merge`. Each has distinct authority and valid verdict values.

2. **Commit binding**: Every verdict applies exclusively to the `reviewed_commit`.
   A changed HEAD invalidates all prior reviews for the new HEAD.

3. **Review supersession**: Each verdict may reference a prior verdict via
   `supersedes_review`, forming an auditable chain.

4. **Extended verdict schema** (`SCHEMAS/review-verdict.json`, v2):
   - `review_type` restricts valid `verdict` values per type
   - `review_basis` documents what was evaluated (PR, merge commit, release)
   - `supersedes_review` enables chain formation
   - `remaining_followups` documents deferred items

5. **Terminology rules**: Self-verification must not use "approved",
   "authoritative", or unqualified "ACP Verdict". The only valid verdict for
   self-verification is `consistency-verified`.

## Consequences

**Easier:**
- Review records are self-documenting: type, authority, and scope are explicit.
- Post-merge audits can reference the exact review that preceded them.
- Self-verification is formalized as a valid practice without conflating it
  with independent review.
- Automation can validate verdict schemas and reject type/verdict mismatches.

**Harder:**
- Existing review tooling (`github-review` skill) must be updated to use v2
  schema.
- Previous PRs that used "approved" in self-reviews are technically
  non-conformant retroactively (acceptable as they predate v0.3).
- Reviewers must explicitly track which commit SHA they reviewed.

## Relation to Existing Mechanisms

| Existing | ACP v0.3 | Mapping |
|----------|----------|---------|
| `github-review.md` (ai-governance) | Review types, commit binding | Formalized at ACP level |
| ACP v0.1 review conventions | Review Provenance spec | Superseded |
| Self-review "ACP Verdict" pattern | Self-verification with `consistency-verified` | Stricter terminology |

## References

- Issue: `yeraziael/slartis-backlog#88`
- PR: `yeraziael/slartis-backlog#91`
- PR: `Homelab/ACP#6`
- Existing review skill: `yeraziael/ai-governance/skills/github-review.md`
