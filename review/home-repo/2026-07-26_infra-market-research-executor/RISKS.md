# Risks: infra-market-research-executor

## Architecture

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Per-command user dict could grow unbounded | Low | Low | Keep dict small; document adding new users |
| Conditional sudo logic could miss edge cases | Low | Medium | Test with non-lydia users; default to michael |

## Security

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| lydia runs opencode with full Pi5 access | Medium | Medium | opencode runs in its own env; limited to infra repo |
| Script path hardcoded | Low | Low | Path is in lydia's home directory |

## Operations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Log files accumulate in /tmp | Low | Low | Unique timestamps; Eddie manages rotation |
| opencode headless could hang | Medium | Medium | Script exits with opencode's exit code |

## Migration

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Deployed executor might not pick up new dict | Low | Low | Restart processor after deploy |

## Rollback

Revert the two commits. The executor defaults to `michael` for all commands.
