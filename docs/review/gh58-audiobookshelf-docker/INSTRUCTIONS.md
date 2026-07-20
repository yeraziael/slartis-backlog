# INSTRUCTIONS.md — GH-58 Review Guidelines

## Review Target

This review package covers GitHub Issue **#58** — Audiobookshelf Docker-Service
auf dem Pi5 bereitstellen.

## What This Package Contains

| File | Content |
|------|---------|
| `README.md` | Overview |
| `manifest.json` | Machine-readable provenance |
| `CHANGES.diff` | Combined diff of all Gitea PRs |
| `NOTES.md` | Scope, risks, correction record |
| `TESTING.md` | CI evidence, compose validation, runtime evidence |
| `CI.json` | CI pipeline evidence |

## Review Prerequisites

The reviewer should:
1. Read the diff in `CHANGES.diff` to understand what was changed
2. Verify that each acceptance criterion is documented with evidence in `TESTING.md`
3. Check `manifest.json` for exact SHA bindings
4. Review `NOTES.md` for scope boundaries and risk assessment
5. Confirm no secrets are exposed in the review package

## Gate

After approval:
- The Architecture repo source PRs (#63, #65, #66, #69, #70, #72) are **merged**
- The compose is **deployed** on Pi5
- This GitHub review PR documents the complete evidence
- Merge this PR to close GH-58
- Update the Audiobookshelf epic checklist (GH-57) to mark the Docker-service item as done
