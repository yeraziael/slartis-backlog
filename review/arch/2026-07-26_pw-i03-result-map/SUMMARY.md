# PW-I03: Result Semantics and Exit-Code Mapping

## Problem Statement

The Playwright ephemeral runner (PW-I01/PW-I02) ran Playwright tests inside
Docker but produced no structured exit codes or result classification. Consumers
(Docker CI, Make targets, shell scripts) received raw Docker exit codes without
knowing whether a failure was a test failure, a prerequisite problem, or a
Docker infrastructure error.

## Goal

Map all exit codes of the runner wrapper (`run.sh`) into three stable result
classes: **pass** (0), **fail/error** (1), and **prerequisite_error** (2).
Provide forced-outcome subcommands for test fixtures, and tag-based Playwright
tests to exercise each outcome.

## Scope

- A standalone `map-result.sh` that phases exit codes through a mapping table.
- A modified `run.sh` that uses `map-result.sh` for both dependency and test
  phases.
- A `result-semantics.spec.ts` with `@pass` and `@fail`-tagged tests.
- Forced-outcome subcommands (`run.sh prerequisite_error`, `run.sh error`,
  `run.sh platform pass`, `run.sh platform fail`).
- Runtime fixes discovered during the real Docker run:
  - Removed `--read-only` from both phases (blocks volume mount point creation).
  - Fixed `validate-lock.mjs` lockfile path resolution (`../../` → `../`).
  - Added `package-lock.json` (npm-generated, previously missing).
  - Changed `PLAYWRIGHT_RESULTS_DIR` to `/results/out` (subdir avoids mount
    point rmdir conflict).
- 24 new static bootstrap tests for map-result.sh, forced outcomes, and grep
  filter verification.

## Not in Scope

- CI activation of `playwright-platform` step (requires non-root Docker in CI).
- Real browser-level matrix tests (multi-browser, multi-platform).
- Playwright test result rendering (HTML/JSON reporters).
- Coverage or performance benchmarks.

## Affected Components

- `tests/playwright/runner/run.sh` — runner wrapper
- `tests/playwright/runner/map-result.sh` — new exit-code mapper
- `tests/playwright/runner/validate-lock.mjs` — lockfile validator (bugfix)
- `tests/playwright/package-lock.json` — lockfile (new)
- `tests/playwright/platform/result-semantics.spec.ts` — outcome fixtures
- `tests/test_playwright_bootstrap.py` — static contract tests

## References

- **Canonical PR:** Homelab/Architecture#85
- **Issue:** slarti/backlog#258 (PW-I03)
- **Epic:** slarti/backlog#253 (Playwright)
- **Precedent:** PW-D02 Evidence Provenance ADR
