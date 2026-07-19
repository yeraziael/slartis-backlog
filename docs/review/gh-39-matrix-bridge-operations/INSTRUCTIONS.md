# Architecture Agent Instructions At Review Head

Source: `Homelab/Architecture/AGENTS.md` at
`cca3131d262ad0a48be11b3238c699e507af47f6`; the instruction file was last
changed in commit `bf820d06bd1f95f4fa112805c67cfb6dfc5f9023`.

## Review Contract

- Pull requests are the review object; issue evidence does not substitute for
  pull-request review.
- Implementation evidence includes instruction provenance, exact PR head,
  changed files, CI run IDs, and `review_target: pr`.
- Externally fact-based PRs remain draft until the current head is reviewed.
- Eddie or the operator merges after review.
- New contract tests must run in manifest-generated PR CI.
- Repository preparation and live deployment are separate scopes.
- Credentials, registrations, cookies, runtime data, and raw logs remain outside
  Git and review evidence.
