# Architecture — PW-I03 Result Semantics

## Current State (PW-I01/PW-I02)

The runner wrapper (`run.sh`) runs two Docker phases:
1. **Dependency phase:** Installs npm packages in a volume.
2. **Test phase:** Runs Playwright tests with the installed packages.

Both phases forwarded raw Docker exit codes. `set -euo pipefail` terminated the
script on the first failure without distinction. The entire container was
`--read-only`, which prevented Docker from creating volume mount points.

## New / Changed Components

### map-result.sh (new)

A standalone Bash script that maps a phase exit code to one of three result
codes:

| Input | Dependency Phase | Test Phase |
|-------|-----------------|------------|
| 0 | 0 (pass) | 0 (pass) |
| 1–124 | 2 (prerequisite_error) | 1 (fail) |
| 125+ | 1 (error) | 1 (error) |

Docker exit codes 125+ are infrastructure errors (daemon, OCI runtime, missing
command). Codes 1–124 are application errors (npm failure, test failure).

### run.sh (modified)

- Removed `set -e` to allow explicit error capture with `|| EXIT=$?`.
- Removed `--read-only` from both phases (blocks volume mount point creation).
- Dependency phase: captures exit code, calls `map-result.sh dependency`.
  Non-zero mapped result exits early with the mapped code.
- Test phase: captures exit code, calls `map-result.sh test`.
- Added forced-outcome subcommands: `prerequisite_error` (exit 2), `error`
  (exit 1), `pass`/`fail` (sets `--grep @pass`/`@fail` filter).
- Changed Playwright output dir from `/results` to `/results/out` to avoid
  `rmdir` on the bind mount point.
- Added `chmod 777` on results dir for container non-root user access.

### validate-lock.mjs (bugfix)

Fixed relative path resolution: `../../package-lock.json` → `../package-lock.json`.
The old path resolved to `tests/package-lock.json` (wrong directory); the fix
resolves to `tests/playwright/package-lock.json`.

### result-semantics.spec.ts (new)

Two Playwright tests tagged for grep-based selection:
- `passes @pass` — `expect(true).toBe(true)` (always passes).
- `fails @fail` — `expect(true).toBe(false)` (always fails).

## Interfaces and Data Flows

```
run.sh platform [pass|fail|custom-grep]
  │
  ├─ dependency phase (docker run … npm ci)
  │   └─ exit code → map-result.sh dependency → exit 0/1/2
  │
  └─ test phase (docker run … npx playwright test --grep …)
      └─ exit code → map-result.sh test → exit 0/1
```

```
run.sh prerequisite_error → exit 2 (immediate, no docker)
run.sh error → exit 1 (immediate, no docker)
```

## Architecture Decisions

- **Three result classes** (pass/fail+error/prerequisite_error) match
  PW-D02's evidence-provenance precedence semantics.
- **Standalone mapper script** (`map-result.sh`) keeps mapping logic testable
  without Docker.
- **Forced-outcome subcommands** enable shell-level verification of exit codes
  without real Playwright tests.
- **Tag-based test selection** (`--grep @pass`/`@fail`) avoids duplicating test
  suites for outcome verification.
