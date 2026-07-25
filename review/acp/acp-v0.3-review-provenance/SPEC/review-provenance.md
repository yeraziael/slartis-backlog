# Review Provenance (ACP v0.3)

**Version:** 0.3.0-draft
**Status:** Draft
**Supersedes:** Implicit review conventions in `yeraziael/ai-governance`

## Purpose

Review Provenance defines the normative requirements for review artifacts
within the ACP framework. It ensures that every review verdict is
cryptographically and procedurally traceable: who reviewed what, when, on
which basis, and with what authority.

## Normative Principles

1. **Every review is SHA-bound.** A review verdict applies exclusively to the
   exact commit it references. If the target commit changes, all prior reviews
   become historical evidence only. A new verification or independent review is
   required.

2. **Review types are disjoint.** Self-verification, independent review, and
   post-merge verification are separate classes with separate authority. No
   review type may be presented as another.

3. **Self-verification is not independent review.** An author who validates
   their own work may assert internal consistency. They may not issue an
   authoritative merge recommendation. Self-verification never replaces an
   independent review.

4. **Verdicts form an auditable chain.** Each review may reference a prior
   review via `supersedes_review`, forming a chronological chain that
   documents every re-evaluation.

## Review Types

### Independent Review

An **Independent Review** is conducted by a reviewer with no direct
involvement in the implementation. It carries merge recommendation authority.

| Field | Requirement |
|-------|-------------|
| Reviewer | Not the PR author or committer |
| Authority | May approve or request changes |
| Merge recommendation | Authoritative |
| SHALL appear as | GitHub/Gitea `APPROVED` or `CHANGES_REQUESTED` |
| SHALL NOT appear as | `COMMENTED` with ACP-verdict substitute |

### Self-Verification

**Self-Verification** is conducted by the implementation author to demonstrate
internal consistency. It carries no merge authority.

| Field | Requirement |
|-------|-------------|
| Reviewer | The PR author or committer |
| Authority | May assert consistency only |
| Merge recommendation | None. Self-verification is not a substitute for independent review |
| SHALL appear as | `COMMENTED` with explicit `"review_type": "self-verification"` |
| SHALL NOT appear as | `APPROVED`, `CHANGES_REQUESTED`, or verdict claiming authoritative approval |

When GitHub/Gitea does not allow self-approval, the self-verification SHALL
use `COMMENTED` with the structured verdict. The word "approved" or
"approval" SHALL NOT appear in a self-verification verdict body.

### Post-Merge Verification

**Post-Merge Verification** validates a merged artifact. It documents
remaining follow-up work. It never changes the historical review outcome.

| Field | Requirement |
|-------|-------------|
| Reviewer | Any |
| Authority | Documents state of merged artifact |
| Merge recommendation | N/A — already merged |
| SHALL reference | The merge commit SHA |
| SHALL document | Any remaining follow-up items |

## Commit Binding

A review verdict applies ONLY to the reviewed commit. If the target HEAD
changes (amended, rebased, new commits), the verdict becomes historical
evidence for that specific commit. It MUST NOT be treated as applying to the
new HEAD.

The `reviewed_commit` field SHALL contain the full SHA-1 hash of the reviewed
commit. Short SHAs, branch names, or tag references are not sufficient.

## Review Supersession

Reviews SHALL form an auditable chain via `supersedes_review`. Each review
may reference the review it replaces, updates, or responds to.

Example chain:

```
Review A (self-verification, commit X)
  ↓ supersedes: none
Fixes
Review B (self-verification, commit Y)
  ↓ supersedes: A
Independent Review C (commit Y)
  ↓ supersedes: B
Merge
Post-Merge Verification D (merge commit Z)
  ↓ supersedes: C
```

The `supersedes_review` field SHALL contain a reference that uniquely
identifies the prior review (e.g., URL, review ID, or `(reviewer, timestamp,
commit)` tuple).

## Verdict Schema

Every review verdict MUST conform to the ACP Review Verdict schema
(`SCHEMAS/review-verdict.json`).

### Core fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema` | `string` | yes | Schema identifier, e.g. `acp.review-verdict.v2` |
| `reviewed_commit` | `string` | yes | Full SHA-1 hash of the reviewed commit |
| `review_type` | `string` | yes | One of: `independent`, `self-verification`, `post-merge` |
| `review_basis` | `string` | yes | What the review evaluated: `pull-request`, `merge-commit`, `release`, `working-copy` |
| `reviewer` | `string` | yes | Identity of the reviewer |
| `verdict` | `string` | yes | One of: `approved`, `request_changes`, `consistency-verified`, `post-merge-audit` |
| `blocking_findings` | `array` | no | Items that must be resolved before approval |
| `remaining_followups` | `array` | no | Items deferred beyond this review |
| `supersedes_review` | `string` | no | Reference to the prior review this replaces |
| `review_timestamp` | `string` | yes | ISO 8601 timestamp of the review |

### Verdict values by review type

| `review_type` | Valid `verdict` values |
|---------------|------------------------|
| `independent` | `approved`, `request_changes` |
| `self-verification` | `consistency-verified` |
| `post-merge` | `post-merge-audit` |

Combining `review_type: self-verification` with `verdict: approved` or
`verdict: request_changes` is a schema violation.

## Terminology

Self-verification verdicts SHALL use the following disclaimer:

> "This is a self-verification by the implementation author. It demonstrates
> internal consistency but is not an independent review. Only an independent
> review represents an external quality assessment."

The word "authoritative" SHALL NOT appear in self-verification verdicts.
"ACP Verdict" as a heading in self-verification is permitted only when
qualified by the review type.

## Return Value

The rendered verdict SHALL be machine-readable and human-readable. When
posted as a comment on a pull request or commit, the verdict SHOULD include
the structured JSON block and a prose summary.

## Alignment With Existing Governance

| ACP Term | `yeraziael/ai-governance` mapping |
|----------|-----------------------------------|
| Independent Review | `github-review.md` formal review |
| Self-Verification | Not previously formalized |
| Post-Merge Verification | Post-merge audit |
| Commit Binding | SHA-bound review semantics |
| Review Supersession | Review cycle iteration |

