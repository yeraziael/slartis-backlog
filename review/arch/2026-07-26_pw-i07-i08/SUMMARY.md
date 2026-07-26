# PW-I07 / PW-I08 - Evidence Sanitisation and Deterministic Bundles

## Problem

Playwright evidence could contain credentials or personal data and previously
had no deterministic, retention-classified publication bundle.

## Scope

- PW-I07: fail-closed sanitisation for text, ZIP trace content, and image
  metadata, with synthetic clean and leak fixtures.
- PW-I08: deterministic assembly of scanner-approved evidence, SHA-256
  inventory, retention metadata, and bundle validation.

## Excluded

- No Gitea upload, deletion scheduler, live service suite, real credentials,
  or unsanitised artifact publication.

## Canonical Changes

- Homelab/Architecture#93 - PW-I07, merged as `8c744dd`.
- Homelab/Architecture#94 - PW-I08, merged as `3362689`.

## Result

Evidence publication is fail-closed. Pass bundles retain no artifacts and use
a 7-day class; fail, prerequisite-error, and error bundles use a 30-day class.
