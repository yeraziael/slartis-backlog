# PW-I07 / PW-I08 Re-review - Fail-Closed Evidence Publication

This revision supersedes the package at `2026-07-26_pw-i07-i08/` after the
GitHub review findings on PR #100. It binds the review to canonical Gitea PR
#95 head `7f9c7252572a53cd6367d1d17f5a25b3683a4879`.

## Corrected Scope

- Image evidence without an available scanner is rejected.
- ZIPs are structurally validated and unreadable/extraction-failed archives
  are rejected.
- The scanner and assembler reject symlinks, special files, and root escapes.
- Tests capture rejected process status and diagnostics using `spawnSync`.

No upload, deletion scheduler, real credentials, or live service behavior is
included.
