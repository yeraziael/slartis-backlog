## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|---------|--------|
| Manifest generation fails for forced outcomes | Low | High | Tested with fake docker; empty runner_containers allowed |
| Prerequisite check false-positive in unusual network | Low | Medium | All checks return non-zero on failure; orchestrator exits 2 |
| Trace/ZIP corruption in capture | Low | Low | Basic integrity check in artifact self-tests |
| Schema drift from PW-D02 contract | Low | High | Schema is versioned; new version requires new integer |
| Keycloak check depends on curl+python3 | Medium | Low | Both available in the pinned playwright image |
