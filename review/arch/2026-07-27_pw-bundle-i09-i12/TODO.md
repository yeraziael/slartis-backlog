# TODO: PW-I09/I10/I11/D05/I12 Bundle

## Open Items

- [ ] Close backlog issues #267, #268, #269, #270, #271 after merge
- [ ] Run live provisioned test suite with real Keycloak credentials
- [ ] Register `test-playwright-platform` target in Makefile for fixture self-tests

## Follow-up Issues

- PW-I13: Authenticated login/logout smoke (uses OIDC fixture)
- PW-I14: Controlled library and playback
- PW-I15: Role and negative authorization tests
- PW-I16: Pre-merge CI gates
- PW-I17: Post-deployment smoke/retry/ACP handoff

## Technical Debt

- `login.ts` hardcodes ABS base URL as default; could accept config object
- `fake-oidc.ts` password validation is hardcoded; could accept user list
- No `.gitignore` for `__pycache__` in project root
