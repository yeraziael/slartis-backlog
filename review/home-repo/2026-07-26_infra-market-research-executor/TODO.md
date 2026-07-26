# TODO: infra-market-research-executor

## Open Items

- [ ] Unit tests for `OPS_COMMANDS_USERS` logic
- [ ] Integration test for conditional sudo path
- [ ] Parameterize research prompt (currently hardcoded in script)
- [ ] Log rotation policy for `/tmp/infra-market-research-*.log`

## Follow-up Issues

- Eddie scheduling configuration (separate issue)
- Research output quality monitoring

## Known Limitations

- Script hardcodes the research prompt
- Log files are ephemeral (lost on reboot)
- No retry logic if opencode fails
