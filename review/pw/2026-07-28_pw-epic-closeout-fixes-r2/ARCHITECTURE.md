# ARCHITECTURE - Playwright Epic Closeout Fixes

## Current State

Gitea Actions executes each job inside a container while nested Playwright containers use the host Docker daemon. A path visible inside the Gitea job container is not necessarily a valid host bind source. The repository previously assumed `/workspace`, combined service runtime checks, and did not guarantee that credential-gated skips failed the production gate.

The corrected tree is now merged at `11921fb0572222e5d3ccf7652ef1b466c704bc0f`. Gitea has two global runners with the same name and label. Runner ID 4 executed green PR Unit Tests; runner ID 3 repeatedly fails in the results initializer before repository code runs. Runner administration is external to the Architecture repository and tracked by `slarti/backlog#284`.

## Changed CI Topology

`ci-manifest.yaml` remains the source of truth. `ci-generate.py` produces the workflow and Makefile contracts. PR CI runs platform and operations coverage without service credentials. Main-branch runtime verification is split into `Post-Deployment Audiobookshelf` and `Post-Deployment Jellyfin`, each with its own URL, credential contract, suite, artifact name, and evidence directory.

## Nested Docker Data Flow

1. The runner identifies the Gitea job container from its hostname and inspects its mounts through the Docker socket.
2. It selects only the mount containing the repository checkout and imports that mount read-only at its existing destination.
3. A disposable named volume holds `node_modules`; an empty mount target is prepared before applying the read-only checkout.
4. A separate disposable named volume holds Playwright results. A one-volume initializer creates `/results/out` with permissions usable by the explicit non-root browser UID/GID.
5. The dependency container installs the lockfile-defined packages into the dependency volume.
6. The browser container runs as the configured non-root identity with the checkout and dependency volumes read-only and the results volume writable.
7. A stopped copy container exposes only the results volume to `docker cp`, returning evidence to the Gitea workspace without making the checkout writable to the browser container.
8. The runner generates and validates the manifest in the job container and removes all disposable containers and volumes.

## Evidence Flow

Playwright writes its JSON report and artifacts to `/results/out`. `result-summary.py` derives final test totals from the JSON report. `manifest-generate.py` combines those counts with trusted runner metadata. Post-deployment validation rejects missing evidence, invalid schemas, failed tests, or skipped tests before the artifact upload step can represent the run as successful.

## Service Boundaries

Audiobookshelf and Jellyfin use separate npm scripts and service-specific test directories. Environment variables are explicitly forwarded by service. The post-deployment wrapper validates the complete required credential set before invoking Docker, so absent identities are prerequisite failures rather than successful skipped suites.

## Security Properties

- Browser execution remains non-root even when the Gitea job itself is root.
- The canonical checkout is read-only inside dependency and browser containers.
- Gitea auxiliary runtime volumes are not inherited by nested containers.
- Credentials remain Gitea Actions secrets and are not copied into evidence or review material.
- Service evidence is uploaded only after schema, result, failure-count, and skip-count checks.
- Disposable volume names are randomized and removed by an exit trap.

## Compatibility

Local execution retains the existing host bind-mount flow and host-side results permissions. CI supports either a Docker named volume or bind mount as the Gitea checkout source. No production service interface or stored data format changes.
