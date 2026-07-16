---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#214
state: closed
updated_at: 2026-07-14T16:35:08+02:00
is_epic: false
labels:
  []
publication: sanitized
---

# Install jq in the Eddie runtime image

## Context

The production blackbox test for PR #348 showed that the Eddie runtime image is based on minimal Alpine and does not contain `jq`. Operational inspection currently has to stream JSON out of the container and parse it on the host.

## Scope

- Install `jq` in the Eddie runtime image through its Dockerfile.
- Keep the image minimal and use Alpine `apk --no-cache`.
- Do not add credentials, mutable runtime state, or host dependencies to the image.
- Update operator documentation where in-container report/queue inspection is described.

## Tests

1. Extend Eddie CI/smoke coverage to run `docker run --rm eddie:ci jq --version`.
2. Parse a representative JSON document inside the built ARM64 image and assert the expected value.
3. Keep the existing Eddie Go tests, vet, staticcheck, ARM64 build, Docker build, and health smoke test green.

## Definition of Done

- `jq` is available in the production Eddie container.
- The package is installed only in the runtime stage.
- ARM64 CI proves executable compatibility.
- Existing image health and policy-reconciler behavior remain unchanged.
- Deployment and rollback instructions are documented.

---

Moved from `lydia/home-repo#354` because Lydia cannot implement this task yet.
