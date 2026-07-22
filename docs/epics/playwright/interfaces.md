# Playwright — Interfaces

## 1. Runner ↔ Service Under Test

| Aspect | Specification |
|---|---|
| Protocol | HTTPS (TLS 1.2+) |
| Entry point | Public FQDN via frontproxy (e.g., `https://audiobookshelf.hl.maier.wtf`) |
| Authentication | OIDC Authorization Code Flow through Keycloak |
| Health check | `GET /` or service-specific health endpoint → HTTP 200 before test suite starts |
| Service version | Retrieved from container image digest or service API; included in evidence manifest |
| Failure mode | Service unreachable or unhealthy → suite reports `prerequisite_error`, not test failure |

### Contract

```
Runner ── HTTPS ──→ Frontproxy ── HTTP ──→ Service
         OIDC login via Keycloak redirect
         Evidence: response status, page content, console logs, traces
```

## 2. Runner ↔ Keycloak

| Aspect | Specification |
|---|---|
| Protocol | HTTPS (OIDC Authorization Code Flow) |
| Keycloak endpoint | `https://keycloak.hl.maier.wtf` or internal Keycloak URL reachable from runner |
| Authentication | Synthetic test usernames + passwords injected at runtime |
| Identity source | Keycloak realm with dedicated test users (see `contracts.md` §Synthetic Test Identities) |
| Token validation | Runner verifies token by successful login — full token validation is the service's responsibility |
| Failure mode | Keycloak unreachable or login fails → suite reports `prerequisite_error` |

### Contract

```
Runner ── OIDC Auth Code Flow ──→ Keycloak
         Synthetic credentials from environment variables
         On success: session cookie / storage state for subsequent requests
         On failure: prerequisite_error, no further tests executed
```

## 3. Runner ↔ CI (Gitea Actions)

| Aspect | Specification |
|---|---|
| Invocation | Gitea Actions workflow step |
| Container image | Pinned Playwright image from registry |
| Test selection | Environment variable or CLI argument (suite name, service target) |
| Output (exit code) | 0 = all tests pass, 1 = test failure, 2 = prerequisite error |
| Output (artifacts) | Evidence bundle uploaded as CI artifact |
| Output (report) | JUnit XML for CI test reporting |
| Failure mode | Non-zero exit → CI step fails, artifact retained for review |
| Retry | Configurable retry for prerequisite errors (transient infrastructure) |

### Contract

```
CI Workflow ── docker run ──→ Playwright Container
         Environment variables:
           - SERVICE_URL
           - KEYCLOAK_URL
           - TEST_USERNAME / TEST_PASSWORD
           - SUITE (smoke|regression|e2e)
         Output:
           - Exit code
           - /results/ directory with manifest + artifacts
         CI uploads /results/ as run artifact
```

## 4. Runner ↔ Evidence Store

| Aspect | Specification |
|---|---|
| Storage | CI run artifacts (Gitea Actions) or local filesystem (operator mode) |
| Format | Directory with `manifest.json`, `results.json`, `junit.xml`, `screenshots/`, `traces/`, `videos/` |
| Retention | Configurable per run type (see `ci.md` §Artifact Retention) |
| Access | Reviewer downloads from CI or retrieves from ACP review package |
| Sanitisation | Runner MUST sanitise secrets, tokens, cookies and personal data before writing to evidence store |

### Contract

```
Evidence Bundle:
  manifest.json     ← machine-readable metadata (commit, version, result)
  results.json      ← per-test results
  junit.xml         ← CI-compatible report
  screenshots/      ← captured on failure (or always if configured)
  traces/           ← Playwright trace files (failure only)
  videos/           ← Playwright video recordings (optional)
```

## 5. Service Epic ↔ Shared Platform

| Aspect | Specification |
|---|---|
| Service responsibility | Define user journeys, acceptance criteria, controlled test data |
| Platform responsibility | Provide fixtures, evidence format, execution conventions, runner infrastructure |
| Handoff | Service epic documents coverage requirements; platform team implements test code |
| Version coupling | Service version changes MAY require test updates; evidence manifest captures service version |
| Boundary | Service-specific page objects and journeys live in service suite; shared fixtures in platform core |

### Contract

```
Service Epic ── defines ──→ User journeys, acceptance criteria
                 │
                 v
         Platform implements test code
                 │
                 v
         Service verifies coverage adequacy
                 │
                 v
         Evidence bundle → Reviewer
```

## 6. Platform ↔ Homelab/Architecture Repository

| Aspect | Specification |
|---|---|
| Platform code location | `Homelab/Architecture/tests/playwright/` |
| Configuration location | `Homelab/Architecture/tests/playwright/playwright.config.ts` |
| Fixtures location | `Homelab/Architecture/tests/playwright/fixtures/` |
| Service suite location | `Homelab/Architecture/tests/playwright/services/<service-name>/` |
| Runner definition | `Homelab/Architecture/` (Compose or Dockerfile for runner, if needed) |

The `Homelab/Architecture` repo is authoritative for implementation. This document and the epic documents in `yeraziael/slartis-backlog` are authoritative for scope and requirements.

## Interface Summary

| Interface | Type | Protocol | Security |
|---|---|---|---|
| Runner → Service | Test execution | HTTPS | TLS, OIDC session |
| Runner → Keycloak | Authentication | OIDC (HTTPS) | TLS, credentials at runtime |
| Runner → CI | Orchestration | Exit codes + files | CI context |
| Runner → Evidence Store | Artifact output | Filesystem | Sanitised before write |
| Service Epic → Platform | Requirements | Documentation | N/A |
