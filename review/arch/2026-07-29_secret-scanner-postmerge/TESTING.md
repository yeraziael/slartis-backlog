# Testing

Verified before merge at canonical head `530984e8db131bc6a4026a36d3b4875523481d92`:

- `bash scripts/scan-secrets.sh` passed.
- `python3 tests/test_safe_summary.py` passed: 98 tests.
- `bash tests/test_checks.sh` passed: 12 tests.
- `git diff --check` passed.

Gitea PR CI run `991` completed before merge. Main-branch run `992` completed
with failure: lint, unit tests, and reporting passed, while post-deployment
Audiobookshelf job `3704` and Jellyfin job `3705` failed in their smoke steps.
Those runtime failures are unrelated to the scanner test-only diff and require
separate diagnosis before Jellyfin integration can advance.
