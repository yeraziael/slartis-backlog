# Testing Review

## Local Gates

All commands below were run from the Architecture worktree at the reviewed
head `6eb1a8117a0ecd7453a73de90d267e8547d4a782`.

| Command | Result |
|---|---|
| `make test` | PASS; 139 Playwright bootstrap tests and 6 headed contract tests, plus all existing suites. |
| `make lint` | PASS; internal links, Compose structure, diff whitespace, and secret scan. |
| `bash -n tools/playwright-headed/run.sh tools/playwright-headed/entrypoint.sh` | PASS. |
| `node --check tests/playwright/automation/repeat-endpoints.mjs` | PASS. |
| `git diff --check` | PASS. |
| `docker build -t homelab/playwright-headed:v1.61.1-noble-poc -f tools/playwright-headed/Dockerfile .` | PASS. |

## Runtime Smoke Tests

The headed container was run with one reachable endpoint and one unavailable
endpoint, with one-second slots and one round. The reachable Gitea page loaded;
the unavailable `gitea-mcp.hl.maier.wtf` produced a TLS error, rendered a fresh
error tab, and the process completed the round with exit code zero.

The full ten-round workflow was also exercised at runtime before the final
fresh-tab correction. The final correction was revalidated with the bounded
reachable/unavailable smoke run above. The generated password initialization
follow-up was validated by the final secret scan.

## CI

The new contract test is registered through `ci-manifest.yaml` and generated
into both `Makefile` and `.gitea/workflows/ci.yaml`. The real platform Docker CI
step remains separately controlled by its existing manifest flag.

## Known Gaps

- No CI job opens a VNC listener or performs ten external endpoint rounds.
- The public endpoint list is a versioned registry; endpoint availability is a
  runtime observation, not a CI prerequisite.
- `gitea-mcp.hl.maier.wtf` was not reachable during smoke testing and is
  intentionally retained as a nonfatal endpoint case.
