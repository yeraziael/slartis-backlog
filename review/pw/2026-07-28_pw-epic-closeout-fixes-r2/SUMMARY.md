# SUMMARY - Playwright Epic Closeout Fixes Post-Merge Audit

## Problem

The previous Epic #253 closeout review established that the Playwright implementation was merged but not operationally complete. The generated CI did not execute every required suite, service evidence jobs were not separated, skipped credential-gated tests could be mistaken for success, result manifests did not contain actual Playwright totals, and the nested Docker runner did not work in the root-hosted Gitea job environment.

## Goal

Canonical Architecture PR #109 made the repository and CI contracts executable and fail-closed while preserving the operator boundary for deployment and credentials. It was squash-merged by `eddie-policy` as `11921fb0572222e5d3ccf7652ef1b466c704bc0f`.

## Included

- Root-hosted Gitea nested-Docker support with an explicit non-root browser identity.
- Read-only import of only the Gitea checkout mount, isolated dependency and results volumes, evidence copy-back, and deterministic cleanup.
- Correct dependency failure propagation and workspace-independent local fixture URLs.
- Manifest-generated registration of PW-I18 operations tests.
- Separate Audiobookshelf and Jellyfin post-deployment jobs with service-specific suites, credentials, evidence names, and artifact uploads.
- Actual Playwright pass, fail, prerequisite-error, and skip totals in evidence manifests.
- Fail-closed post-deployment validation requiring zero failed and zero skipped tests.
- Audiobookshelf page-object alignment with the production direct-Keycloak redirect.
- Deterministic git-diff test fixtures and updated operational documentation.

## Not In Scope

- Deploying Jellyfin or changing any production service.
- Creating, reading, rotating, or storing service credentials.
- Provisioning controlled media or synthetic service identities.
- Claiming successful production runtime verification.
- Removing or changing global Gitea Actions runner registrations.

## Affected Components

- `ci-manifest.yaml`, `ci-generate.py`, generated `Makefile`, and `.gitea/workflows/ci.yaml`.
- Playwright runner, evidence summary, post-deployment wrapper, service suites, and page objects.
- CI contract, bootstrap, operations, and git-diff regression tests.
- Playwright CI, operations, and Jellyfin onboarding documentation.

## References

- Canonical repository: `Homelab/Architecture`.
- Canonical PR: `Homelab/Architecture#109`, merged as `11921fb0572222e5d3ccf7652ef1b466c704bc0f`.
- Parent epic: `slarti/backlog#253`.
- Operator runtime gate: `slarti/backlog#283`.
- Duplicate runner gate: `slarti/backlog#284`.
- Prior partial closeout review: `yeraziael/slartis-backlog#108`.

## Disposition

The merged tree matches the reviewed PR-head tree and PR Run #906 was green. Main Run #908 is not green: Unit Tests repeatedly execute on duplicate runner ID 3 and fail before repository code with an OCI exec-format error, while both post-deployment jobs correctly fail without operator inputs. Closeout therefore remains incomplete until runner gate #284 and service gate #283 are both resolved at the merge SHA.

This post-merge audit records the state of the merged artifact and its remaining follow-ups. It does not change the historical review outcome or establish production readiness.
