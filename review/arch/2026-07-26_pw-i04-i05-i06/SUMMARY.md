# PW-I04 / I05 / I06 — Evidence Manifest, Prerequisite Checks, Failure-Only Artifacts

## Problem

The Playwright Plan-as-Code test platform required three foundational
capabilities: (1) machine-readable evidence binding to source and runtime
state, (2) composable DNS/TLS/HTTP/Keycloak prerequisite checks with a
fail-closed gate, and (3) failure-only screenshot and trace capture for
deterministic artifact management.

## Goal

Deliver PW-I04, PW-I05, and PW-I06 as the next three implementation
tickets after PW-I03.

## Scope

- JSON Schema v1, typed generator (`manifest-generate.py`), and shell
  validator (`manifest-validate.sh`) for the PW-D02 evidence manifest
  contract
- Individual check scripts (DNS, HTTP, TLS, Keycloak) and an orchestrator
  (`check-all.sh`) with fixture/service modes
- Playwright config (`screenshot: only-on-failure`, `trace: retain-on-failure`)
  and artifact self-tests (`artifact-self-test.spec.ts`)
- Integration into `run.sh` for manifest generation and service-mode
  prerequisite checks
- Post-run artifact verification harness (`verify-artifacts.sh`) with
  screenshot and trace validation
- 117 static bootstrap tests (up from 90)

## Not in Scope

- No production FQDN checks in PR CI, no retries, no service identity login,
  no product assertions, no sanitisation, no CI upload, no videos, no retention
  deletion

## Canonical PRs

- Homelab/Architecture#86 (PW-I04, merged)
- Homelab/Architecture#87 (PW-I05, merged)
- Homelab/Architecture#88 (PW-I06, merged)
- Homelab/Architecture#89 (PW-I06 fix: artifact verification harness, merged)
- Homelab/Architecture#90 (PW-I06 fix: trace hard failure, merged)
- Homelab/Architecture#91 (PW-I06 fix: structural ZIP integrity, merged)
