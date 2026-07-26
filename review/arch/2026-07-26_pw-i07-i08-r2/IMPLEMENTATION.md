# Implementation

| File | Corrective change |
|---|---|
| `sanitise.sh` | Rejects unavailable image scanner, validates ZIP fallback, rejects symlinks/non-regular entries |
| `sanitise_zip.py` | Uses `testzip()` and errors rather than skipping unreadable archive entries |
| `bundle-assemble.py` | Rejects input symlinks, special files, and resolved paths outside the root |
| `sanitisation-spec.spec.ts` | Uses `spawnSync`; tests leak rejection, missing image scanner, corrupt ZIP, and symlink escape |
| `bundle-self-test.py` | Adds a symlinked-input rejection case |
| `test_playwright_bootstrap.py` | Adds runnable fail-closed regressions, including the no-Python unzip fallback |
