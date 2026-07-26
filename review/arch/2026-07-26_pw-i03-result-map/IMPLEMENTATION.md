# Implementation — PW-I03 Result Semantics

## Files Changed

| File | Status | Lines | Description |
|------|--------|-------|-------------|
| `tests/playwright/runner/map-result.sh` | **new** | 49 | Exit-code mapper (0/1/2) |
| `tests/playwright/platform/result-semantics.spec.ts` | **new** | 9 | @pass/@fail outcome fixtures |
| `tests/playwright/package-lock.json` | **new** | 75 | npm-generated lockfile |
| `tests/playwright/runner/run.sh` | modified | +72/−8 | Mapping, grep filter, forced outcomes, --read-only removed |
| `tests/playwright/runner/validate-lock.mjs` | modified | +1/−1 | Lockfile path fix |
| `tests/test_playwright_bootstrap.py` | modified | +298/−3 | 24 new static tests |

## Semantic Summary

1. **Exit-code mapping:** `map-result.sh` implements a two-phase mapping table
   and is callable standalone for unit testing.
2. **Runner integration:** `run.sh` delegates both phases to `map-result.sh`,
   exiting early on dependency failure with the mapped code.
3. **Runtime fixes:** Three Docker-specific issues discovered during real
   execution were fixed:
   - `--read-only` blocks volume mount point creation → removed from both phases.
   - `validate-lock.mjs` lockfile path was wrong (went up two levels instead of
     one) → fixed.
   - `package-lock.json` was missing from repo → generated and committed.
   - Playwright `rmdir` on bind mount point (`/results`) failed →
     changed output dir to `/results/out`.
4. **Test fixtures:** `result-semantics.spec.ts` provides grep-accessible
   pass/fail outcomes without browser dependencies.
5. **Forced outcomes:** `run.sh` supports `prerequisite_error` (exit 2) and
   `error` (exit 1) subcommands that skip Docker entirely.
6. **Static test coverage:** 24 new Python tests cover map-result.sh unit
   behavior, run.sh subcommand routing, and grep filter propagation.

## Breaking Changes

None. The runner interface (`run.sh platform`) remains backward compatible.
New subcommands extend the interface.
