# Playwright — Testing

## Test Strategy

Testing is structured in six layers:

1. **Platform Self-Tests** — verify the runner, fixtures and evidence machinery work correctly.
2. **Smoke Tests** — rapid post-deployment verification (minutes).
3. **Regression Tests** — comprehensive coverage for releases and relevant changes.
4. **E2E Acceptance Tests** — complete user journeys with reviewable evidence.
5. **Service Acceptance Tests** — service-specific requirements from `requirements.md` verified through the browser.
6. **Evidence Validation Tests** — verify evidence integrity, manifest completeness and sanitisation.

## Platform Self-Tests

These tests verify that the shared platform works before any service suite is executed.

| Test | Scope | Expected |
|---|---|---|
| Runner starts | Container starts, browsers available | Exit 0 |
| Fixture: OIDC login | Login with synthetic credentials succeeds | Session cookie obtained |
| Fixture: user roles | Each role can be authenticated | Correct group/permission mapping |
| Fixture: service health | Health endpoint check | Correct pass/fail classification |
| Evidence manifest | `manifest.json` produced with all required fields | Valid JSON, all fields present |
| Evidence sanitisation | Credentials not present in output | No secrets in any artifact |
| Failure classification | Prerequisite error vs test failure | Correct exit code |
| Browser isolation | Two sequential tests have clean contexts | No state leakage |

## Smoke Tests

Runs after deployment and SHOULD complete within a few minutes.

Minimum checks per service:

- HTTPS endpoint reachable (HTTP 200).
- Expected page loads (title, key elements).
- OIDC login flow completes.
- One critical authenticated user action succeeds.
- Logout succeeds.
- No unexpected browser-console errors (filtered for known non-critical messages).

### Smoke Suite Structure

```typescript
// services/<service>/smoke.spec.ts
describe('<Service> Smoke', () => {
  test('HTTPS endpoint loads', ...);
  test('HTTP redirects to HTTPS', ...);
  test('OIDC login with valid user', ...);
  test('Key user action works', ...);
  test('Logout completes', ...);
  test('No console errors in covered flows', ...);
});
```

## Regression Tests

Runs for releases or relevant changes.

Covers:

- Navigation structure.
- Permission boundaries (user vs admin vs denied).
- Session behaviour (login, expiry, logout).
- Core workflows (full CRUD where applicable).
- Negative paths (invalid input, unauthorised access).
- Previously fixed defects (regression prevention).

### Regression Suite Structure

```typescript
// services/<service>/regression.spec.ts
describe('<Service> Regression', () => {
  // Navigation
  test('all menu items reachable by authorised user', ...);
  test('admin-only items not visible to user', ...);

  // Permissions
  test('denied user cannot access service', ...);
  test('user lacks admin functions', ...);

  // Session
  test('session expires after timeout', ...);
  test('re-login after logout creates new session', ...);

  // Workflows
  test('core user journey completes', ...);

  // Negative
  test('invalid input handled gracefully', ...);
});
```

## E2E Acceptance Tests

Uses deterministic test identities and controlled test data. Verifies a complete user journey and emits reviewable evidence.

### E2E Suite Structure

```typescript
// services/<service>/e2e.spec.ts
describe('<Service> E2E', () => {
  test('authenticated user completes primary workflow', ...);
  test('administrator completes admin workflow', ...);
  test('evidence manifest captures all fields', ...);
});
```

## Service Acceptance Tests

These tests verify requirements from each adopting service epic's `requirements.md`. Evidence levels:

| Level | Meaning |
|---|---|
| **Upstream native** | Feature exists in the service upstream. No Homelab-specific configuration verified. |
| **Configured** | Explicitly configured for Homelab deployment. Configuration source referenced. |
| **Verified** | Test executed with evidence reference (CI run, evidence bundle). |
| **Pending** | Not yet testable — blocking dependency identified. |

### Audiobookshelf Acceptance (Pilot)

| Test | Requirement | Evidence Level |
|---|---|---|
| HTTPS endpoint loads | PWR-090 | Planned |
| HTTP redirects to HTTPS | Service spec | Planned |
| OIDC login with valid user | Service spec (R-020) | Planned |
| OIDC login denied without group | Service spec (R-042) | Planned |
| Admin user has admin functions | Service spec (R-041) | Planned |
| Guest user has read-only access | Service spec (R-040) | Planned |
| Playback starts and pauses | Service spec (R-002) | Planned |
| Logout completes | Service spec | Planned |
| Break-glass login (separate suite) | Service spec (R-060) | Planned |
| No console errors in covered flows | PWR-090 | Planned |

### Jellyfin Acceptance (Second Service)

| Test | Requirement | Evidence Level |
|---|---|---|
| OIDC login with valid user | Service spec | Planned |
| Library visibility for permitted user | Service spec | Planned |
| Restricted library denied | Service spec | Planned |
| Admin user has admin functions | Service spec | Planned |
| Playback starts | Service spec | Planned |
| Logout completes | Service spec | Planned |

## Evidence Validation Tests

| Test | Expected |
|---|---|
| `manifest.json` exists | File present |
| All required manifest fields present | JSON schema validation |
| Source commit SHA matches tested commit | Verified |
| Service version matches deployed version | Verified |
| No credential patterns in artifacts | Secret scan on evidence bundle |
| JUnit XML valid | XML schema validation |
| Screenshots readable (on failure) | Image file valid |
| Traces readable (on failure) | Zip file valid |

## Prerequisite Classification

The runner MUST check prerequisites before executing any test suite.

```typescript
// Pseudocode
async function runSuite(service: string, suite: string) {
  const prereqs = [
    checkDns(service),
    checkTls(service),
    checkHealth(service),
    checkKeycloak(),
    checkTestIdentity(service),
  ];

  const results = await Promise.allSettled(prereqs);
  if (results.some(r => r.status === 'rejected')) {
    return { result: 'prerequisite_error', details: results };
  }

  return executeTests(service, suite);
}
```

## Test Execution Matrix

| Suite | Trigger | Max Duration | Evidence | Retry |
|---|---|---|---|---|
| Platform self-tests | Runner image change | 2 min | Full | No |
| Smoke | Post-deployment | 5 min | Screenshots on fail | Infrastructure only |
| Regression | Release / relevant change | 20 min | Full | Infrastructure only |
| E2E | Release / relevant change | 15 min | Full | No |
| Service acceptance | Per service epic trigger | Per service | Full | Infrastructure only |
| Evidence validation | After each suite | 1 min | Validation report | No |
