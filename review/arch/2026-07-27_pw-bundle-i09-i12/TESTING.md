# Testing: PW-I09/I10/I11/D05/I12 Bundle

## Tests Executed

### Local Validation

| Step | Command | Result |
|------|---------|--------|
| Lint | `make lint` (shellcheck, shfmt, yamllint, ci-generate check, pytest, scan-secrets) | PASS |
| Unit tests | `make test` (139 bootstrap + 7 headed contract) | PASS |
| Diff check | `git diff --check` | PASS |

### Playwright Fixture Self-Tests

| Suite | Tests | Result |
|-------|-------|--------|
| `shared-fixtures.spec.ts` (PW-I10) | 10 | **10/10 PASS** |
| `oidc-fixture.spec.ts` (PW-I11) | 7 | **7/7 PASS** |
| **Platform total** | **17** | **17/17 PASS** |

### Service Smoke Tests (live against audiobookshelf.hl.maier.wtf)

| Suite | Tests | Result |
|-------|-------|--------|
| `smoke-unauthenticated.spec.ts` (PW-I12) | 5 | **5/5 PASS** |

### Provisioning Script Tests

| Suite | Tests | Result |
|-------|-------|--------|
| `test_playwright_identities.sh` (PW-I09) | 31 | **31/31 PASS** |

### CI Status

No CI integration yet. All tests run locally on rechenknecht.

## Total Evidence

**53/53 tests passing** across all 4 suites.

## Schema Validations

| Schema | Result |
|--------|--------|
| `governance/schemas/review-manifest-schema.yaml` | pending |

## Known Gaps

- No CI registration (deferred to PW-I16)
- No Playwright config `projects` entry for audiobookshelf
- No shared OIDC fixture integration with service specs yet (PW-I13)
