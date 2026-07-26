# Architecture

## Evidence Manifest (PW-I04)

The manifest generator accepts a trusted input envelope from the host
wrapper (`run.sh`) and produces a schema-valid `manifest.json` in the
results directory. The envelope includes:

- Git commit SHAs (source and architecture — currently identical as both
  live in `Homelab/Architecture`)
- Runner image reference with immutable digest
- Container IDs from PW-D01 `--cidfile` output
- Caller-selected service name, environment, and suite
- Duration and timestamp from the wrapper's clock
- Aggregate test counts from runner output

The schema (`manifest.schema.json`) enforces PW-D02 contract rules:
`additionalProperties: false`, strict field patterns, and an
`acceptance_criteria` array per ACP Pilot 57.

## Prerequisite Checks (PW-I05)

Four standalone shell scripts, each taking a target and returning 0/1:

- `check-dns.sh` — resolves hostname via `getent`/`dig`/`nslookup`/`host`
- `check-http.sh` — verifies HTTP status code via `curl`/`wget`/`node`
- `check-tls.sh` — validates certificate expiry via `openssl`/`node`
- `check-keycloak.sh` — validates OIDC discovery endpoint JSON

The orchestrator (`check-all.sh`) supports two modes:

| Mode | Purpose |
|------|---------|
| `fixture <dir>` | Deterministic test via `fixture.env` variables |
| `service <url>` | Real service check against a live endpoint |

`run.sh` detects `service:<url>` suite prefixes and runs `check-all.sh`
before the test phase. Any failure produces exit 2 (prerequisite_error).

## Failure-Only Artifacts (PW-I06)

`playwright.config.ts` sets `screenshot: 'only-on-failure'` and
`trace: 'retain-on-failure'`. Artifact self-tests verify that passing
tests produce no screenshot/trace files while failing tests capture them.
