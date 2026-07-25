# Risks - ACP Release-State Audit

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Stable release is published before policy evidence is satisfiable | Medium | High | `RELEASE.md` blocks publication pending ai-governance #42. |
| CI falsely accepts a real secret | Low | High | The exemption only matches documented placeholder forms after a secret-like key. |
| CI fails because pip availability differs by runner | Removed | Medium | Use the Debian `python3-jsonschema` package installed during setup. |
| Runtime content is mistaken for a release pin | Medium | Medium | Release gate requires explicit tag and commit pinning. |
| Gitea release differs from tag target after publication | Medium | High | ACP #11 specifies a credentialed post-publication audit. |

## Rollback

This documentation and CI change can be reverted through a normal corrective
PR. No tag, release, runtime deployment, or external artifact was created by
the canonical change.
