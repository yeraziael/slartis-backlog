# Implementation - ACP Post-Publication Release Audit

## Production Adapter

`CONFORMANCE/release_audit.py` enumerates stable tags from a full Git checkout,
loads each matching Gitea release, downloads the attestation and payload assets,
and emits coded blocking findings for every failed binding.

The Gitea client uses only GET requests. The CLI reads the token from a named
environment variable and never accepts or prints the raw credential.

## Deterministic Fixtures

`CONFORMANCE/fixtures/release-audit/` contains valid Gitea release and
attestation templates. `CONFORMANCE/test_release_audit.py` builds a temporary
Git repository with deterministic commit and annotated-tag timestamps, then
mutates the fixtures for negative scenarios.

## CI Integration

- `.gitea/workflows/ci.yaml` executes all fixtures without network or secrets.
- `.gitea/workflows/release-audit.yaml` uses a full checkout and the read-only
  repository secret for scheduled/manual post-publication verification.

## Corrective Commit

Initial source PR #13 used secret name `GITEA_RELEASE_AUDIT_TOKEN`. Gitea
returned HTTP 400 `invalid variable or secret name` because the prefix is
reserved. PR #14 changed workflow, CLI default and runbook to
`ACP_RELEASE_AUDIT_TOKEN`; the final manual workflow run passed.

PR #15 removed a credential-shaped placeholder assignment from the local
runbook after the canonical review-bundle validator correctly rejected that
line in the generated source diff. The final source retains only the variable
name and requires its value to be pre-set in the process environment.
