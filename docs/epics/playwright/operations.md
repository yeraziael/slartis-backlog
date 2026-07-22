# Playwright — Operations

## Runner Upgrades

### Updating the Playwright Container Image

1. Identify the new desired Playwright release version.
2. Pull the new image by digest: `docker pull mcr.microsoft.com/playwright:v<version>@sha256:<new-digest>`.
3. Update the pinned digest in the runner configuration (`Homelab/Architecture`).
4. Run platform self-tests against a known service to verify compatibility.
5. Commit and merge the change.
6. If browser version changed, verify selectors still match in all service suites.

### Compatibility Check

| Check | Command | Expected |
|---|---|---|
| New image pulls | `docker pull <new-image>` | Exit 0 |
| Self-test passes | `docker run <new-image> npx playwright test --project=chromium` | Exit 0 |
| Smoke suite passes | Run smoke suite against service | Exit 0 |

### Rollback

If a runner upgrade breaks service suites:

1. Revert the pinned digest to the previous known-good value.
2. Commit and merge the revert.
3. Investigate the failure and create a fix issue.

## Browser Updates

Browser versions are tied to the Playwright container image. Updating the container image updates all browsers atomically.

| Browser | Update Mechanism | Risk |
|---|---|---|
| Chromium | Via Playwright image update | Medium — CSS/JS rendering may change |
| Firefox | Via Playwright image update | Medium |
| WebKit | Via Playwright image update | Low (if not used as primary target) |

## Fixture Maintenance

### Shared Fixtures

| Fixture | Maintenance Trigger | Owner |
|---|---|---|
| Keycloak OIDC login | Keycloak version update, protocol change | Platform |
| Synthetic user-role fixture | Account rotation, new roles per service | Platform + Service |
| Service health fixture | New service onboarding, endpoint changes | Platform |
| Console-error capture | Playwright API changes | Platform |
| Evidence manifest generator | Evidence format version change | Platform |

### Maintenance Procedure

1. Change is proposed in `Homelab/Architecture` with a PR.
2. Change is tested against all active service suites.
3. If a service suite breaks due to fixture change, the break is fixed before merge.
4. Fixture changes that require service suite updates are documented in the PR.

## Flaky-Test Handling

### Definition

A flaky test is a test that passes and fails on the same code without code changes.

### Procedure

| Step | Action |
|---|---|
| 1 | Identify flaky test from CI history or operator report |
| 2 | Investigate root cause (timing, selector fragility, shared state, infrastructure) |
| 3 | If fix is trivial (timeout, selector), implement and verify |
| 4 | If fix is non-trivial, create an issue and quarantine the test |
| 5 | Quarantined tests are skipped in CI but remain in the suite for local debugging |
| 6 | Flaky tests must be fixed or permanently removed within 14 days of quarantine |

### Flaky Test Metrics

| Metric | Target |
|---|---|
| Maximum flaky rate per suite | < 5% |
| Maximum quarantine duration | 14 days |
| CI retries for flaky tests | 0 (flaky tests are quarantined, not retried) |

## Selector Maintenance

- Prefer `data-testid` attributes: most stable across UI changes.
- When `data-testid` is not available, prefer ARIA roles and accessible names.
- CSS class-based selectors are fragile and SHOULD be avoided.
- Selector changes due to UI updates are maintained by the service suite owner.
- A selector change in a shared fixture requires platform team review.

### Selector Convention

| Priority | Strategy | Example |
|---|---|---|
| 1 (best) | `data-testid` | `page.getByTestId('login-submit')` |
| 2 | ARIA role | `page.getByRole('button', { name: 'Log in' })` |
| 3 | Text content | `page.getByText('Library')` |
| 4 | CSS selector | `page.locator('.btn-primary')` — avoid if possible |

## Test-Data Lifecycle

### Creation

- Controlled test data is defined by the service epic.
- Test data MUST be versioned (directory per test data version, or scripted setup).
- Test data MUST be reproducible (deterministic content).

### Refresh

- Test data MAY be refreshed on each test run (scripted setup).
- Test data SHOULD be reset to a known state between runs.
- Ephemeral data (created during a test) MUST be cleaned up after the test.

### Cleanup

- Tests MUST clean up created resources where possible.
- If cleanup fails, the evidence bundle MUST note the orphaned resource.
- Periodic cleanup scripts SHOULD exist for orphaned resources.

### Break-Glass Test Data

Break-glass recovery tests require a separate, controlled test procedure that:

1. Creates a known test data state.
2. Executes the break-glass login and verification.
3. Resets the break-glass password after the test.
4. Runs in isolation from routine smoke and regression suites.

## Upgrade Procedures

### Playwright Version Upgrade

| Step | Action |
|---|---|
| 1 | Review Playwright changelog for breaking changes |
| 2 | Update pinned image digest |
| 3 | Run platform self-tests |
| 4 | Run all service smoke suites |
| 5 | Run all service regression suites |
| 6 | Commit and merge |

### Service Version Upgrade (by Adopting Service)

1. Service deployment is updated (new image, new config).
2. Controlled test data is verified to still be valid.
3. Smoke suite is executed against new deployment.
4. If smoke passes, regression suite is executed.
5. Evidence bundle is reviewed.
6. Service upgrade is approved.

## Periodic Tasks

| Task | Frequency | Actor | Status |
|---|---|---|---|
| Verify synthetic identities exist | Weekly | Operator | Planned |
| Rotate synthetic account passwords | Quarterly | Operator | Planned |
| Review flaky test report | Weekly | Slarti | Planned |
| Update Playwright container image | Per release | Slarti | Planned |
| Verify evidence manifest format | Per evidence format change | Slarti | Planned |
| Audit evidence sanitisation | Quarterly | Reviewer | Planned |
| Clean up orphaned test data | Monthly | Operator | Planned |
