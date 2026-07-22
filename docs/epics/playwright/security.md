# Playwright — Security

## Threat Model

| Threat | Impact | Mitigation | Status |
|---|---|---|---|
| Credential exposure in test code | Attacker gains access to Homelab services | Synthetic identities only; credentials injected at runtime; never in source control | Planned |
| Credential exposure in evidence | Attacker sees passwords in screenshots/traces | Evidence sanitisation; failure-only artifact retention | Planned |
| Credential exposure in CI logs | Attacker reads secrets from CI output | Secrets as CI variables; never echoed or logged | Planned |
| Runner container compromise | Attacker accesses Homelab internal network | Ephemeral container; no persistent network access; discarded after run | Planned |
| Synthetic identity abuse | Attacker uses test accounts for unauthorised access | Minimum permissions per role; rotatable credentials | Planned |
| Browser-based data exfiltration | Malicious page exfiltrates test data | No personal data in test identities; runner has no outbound except to services under test | Planned |
| Test data privacy breach | Real user data visible in evidence | Controlled test data only; evidence sanitised before publication | Planned |

## Security Boundaries

```
External (CI / Operator)
         │
         │ Ephemeral container
         ▼
┌─────────────────────┐
│  Playwright Runner    │
│  - Synthetic creds   │
│  - No persistent     │
│  - Discarded after   │
└────────┬────────────┘
         │ HTTPS (TLS 1.2+)
         ▼
┌─────────────────────┐
│  Frontproxy           │  Trust Boundary 1: TLS termination
├─────────────────────┤
│  Service Under Test   │  Trust Boundary 2: Application
├─────────────────────┤
│  Keycloak             │  Trust Boundary 3: Identity
└─────────────────────┘
```

## Secret Handling

| Secret | Storage | Injection Method | Status |
|---|---|---|---|
| Test usernames | CI variables or `.env` (local) | Environment variable at container start | Planned |
| Test passwords | CI variables or `.env` (local) | Environment variable at container start | Planned |
| Keycloak client secret | CI secret or `.env` (local) | Environment variable at container start | Planned |
| Service API tokens (if needed) | CI secret | Environment variable at container start | Planned |

### Rules

- **No secrets in version control.** Zero exception.
- **No secrets in container images.** All secrets injected at runtime.
- **No secrets in test code.** Use `process.env` or Playwright project config.
- **No secrets in evidence.** Evidence sanitisation step **MUST** redact credentials, tokens, cookies.
- **No secrets in CI logs.** CI configuration **MUST NOT** echo variable values.
- **No personal data in synthetic identities.** Usernames, display names, emails are automation markers only.

## Synthetic Identities Only

- Automation **MUST** use synthetic Keycloak accounts. See `contracts.md` §Synthetic Test Identities Contract.
- Real family accounts **MUST NOT** be used in any automated test.
- Synthetic accounts **MUST** be visibly marked as automation (`pw-e2e-` prefix).
- Synthetic accounts **MUST** receive only minimum permissions for their test role.
- Synthetic account passwords **MUST** be rotatable without test code changes.

## Privacy of Retained Artifacts

| Artifact | Privacy Risk | Mitigation |
|---|---|---|
| Screenshots | May show personal content if controlled data contains real titles | Controlled test data MUST use generic, non-personal content |
| Traces | May contain network request bodies with tokens | Trace sanitisation step required before storage |
| Videos | May capture session activity with personal identifiers | Failure-only retention; controlled test data only |
| HTML snapshots | May contain rendered user-specific content | Failure-only retention |
| Console logs | May contain error messages with paths or identifiers | Failure-only retention |

## Evidence Sanitisation

Before evidence is published in a review package or stored persistently, the runner **MUST**:

1. Remove all credential headers from recorded network requests in traces.
2. Verify screenshots do not contain visible tokens, passwords or personal data.
3. Redact any personal identifiers from console error messages.
4. Strip cookies, authorization headers and session tokens from HAR files (if captured).

## Network Security

| Interface | Exposure | Protection |
|---|---|---|
| Runner → Service | Internal Homelab LAN | HTTPS, frontproxy, TLS |
| Runner → Keycloak | Internal Homelab LAN | HTTPS, OIDC |
| Runner → Internet | None (isolated container) | No outbound access except to service |
| CI system | `rechenknecht` | SSH key access, Pi5 internal network |

## Security Verification

| Test | Method | Automated |
|---|---|---|
| No secrets in repo | Secret scan CI check | Planned |
| Evidence sanitisation | Manual review of sample evidence | Planned |
| Credential injection test | Verify credentials only available as env vars | Planned |
| Synthetic identity isolation | Verify test accounts cannot access real user data | Planned |
