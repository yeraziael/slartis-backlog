# Implementation - ACP Release-State Audit

| File | Change |
|---|---|
| `.gitea/workflows/ci.yaml` | Installs `python3-jsonschema` through APT and removes the unpinned pip install; ignores documented `secret:<name>` placeholders only. |
| `CHANGELOG.md` | Adds an Unreleased entry stating that the current v0.3 line has not been published. |
| `README.md` | Distinguishes the draft `VERSION` line from an actual release and links the release contract and audit. |
| `RELEASE.md` | Defines blocking release, publication, verification, runtime, and automation gates. |
| `docs/release-audit-2026-07-25.md` | Records tags, releases, merge history, runtime and mirror observations, gaps, recommendation, and hardening requirements. |

## Compatibility

No protocol schema or runtime behavior changes. The CI change replaces a
nondeterministic package installation with the Debian package used by the
runner. The scanner exemption is restricted to angle- or bracket-delimited
documentation placeholders.

## Release Impact

No ACP release is produced. The documented recommendation is to prepare ACP
v0.3.0 as the first stable release after its gates and the policy dependency
are resolved.
