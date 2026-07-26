# Testing — PW-I03 Result Semantics

## Tests Executed

### Static Bootstrap Tests (75 total, Python)

```bash
python3 tests/test_playwright_bootstrap.py
```
All 75 pass. Covers file existence, content contracts, map-result.sh unit
tests (16), run.sh subcommand routing (5), and grep filter propagation (1).

Includes signal-level coverage: 125, 126, 127 (Docker infrastructure), 130
(SIGINT+128, maps to phase semantics), 139 (SIGSEGV+128, maps to phase
semantics).

### Docker Platform Tests (5 Playwright tests)

```bash
sudo -u michael bash tests/playwright/runner/run.sh platform
```
Result: 4 passed, 1 failed (intentional @fail fixture).
Exit code: 1 (mapped to fail).

### Forced Outcome Subcommands

| Command | Expected Exit | Actual Exit |
|---------|--------------|-------------|
| `run.sh prerequisite_error` | 2 | 2 |
| `run.sh error` | 1 | 1 |
| `run.sh platform pass` | 0 | 0 |
| `run.sh platform fail` | 1 | 1 |

All four forced outcomes produce correct exit codes.

### Grep Filter Propagation

The grep filter (`--grep @pass`, `--grep @fail`, custom pattern) reaches the
Docker test command. Verified via fake-Docker argument capture.

## CI Status

- 4 Gitea Actions runs triggered by the PW-I03 branch:
  - Run #736: success
  - Run #737: success
  - (latest pushes also green)
- CI runs `test-playwright-bootstrap` (static tests). `playwright-platform`
  is disabled in CI (requires non-root Docker).

## Known Test Gaps

- `playwright-platform` step cannot run in CI container (UID 0 issue).
  Only executable on rechenknecht host by user with Docker access.
- No cross-browser matrix tests.
- No test for Docker infrastructure failure simulation (requires real Docker
  daemon error).
