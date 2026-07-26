# PW-POC: Headless And VNC-Headed Playwright Modes

## Problem

The Architecture repository already provides a headless Playwright runner for
CI and platform tests. Operators also need an observable browser session for
interactive workflows and diagnosis without changing the headless CI contract.

## Goal

Add a separate headed Playwright POC with Xvfb and password-protected VNC,
document both execution modes, and provide a bounded public-endpoint workflow.

## Scope

- Extend the pinned Playwright image with Xvfb and x11vnc.
- Start Chromium in headed mode inside the isolated container.
- Expose VNC readiness through local output and Telegram.
- Cycle through nine public Homelab HTTPS FQDNs for ten seconds each and ten
  complete rounds by default.
- Handle unavailable endpoints without aborting the remaining rounds.
- Register static headed-runner contract tests in generated CI.
- Document headless CI and headed operator execution separately.

## Not In Scope

- No persistent browser service or systemd unit.
- No deployment to the Pi5 or production service mutation.
- No login, cookie persistence, credential injection, or ChatGPT automation.
- No public-WAN VNC exposure; the default bind address is the Homelab LAN IP.
- No merge authority: the canonical PR was auto-merged by `eddie-policy` before
  this GitHub review package was opened.

## Affected Components

- `tests/playwright/runner/run.sh` remains the headless CI entry point.
- `tools/playwright-headed/` contains the headed image, entrypoint, runner, and
  operator documentation.
- `tests/playwright/automation/repeat-endpoints.mjs` contains the bounded
  browser workflow.
- Root, Playwright, and runner decision documentation describe both modes.

## Canonical Source

- Repository: `Homelab/Architecture`
- Canonical PR: `http://192.168.2.30:3000/Homelab/Architecture/pulls/96`
- Follow-up PR: `http://192.168.2.30:3000/Homelab/Architecture/pulls/99` (merged)
- Review-fix PR: `http://192.168.2.30:3000/Homelab/Architecture/pulls/100` (open)
- Base commit: `b9f1c7df832b1be1e75019ba4881d1a524a4aa5d`
- Feature merge commit: `511e6964421532083d98669b070f971f2254c137`
- Reviewed head: `a5ddefc`
- Change request: `Homelab/Architecture#96; follow-ups #99 and #100`

The canonical feature PR was merged before the external review package was
created. The reviewed head is the current branch state after the follow-up
corrections. The changeset is a deterministic composite of the feature PR and
the follow-up PRs, excluding unrelated commits that landed on `main` between
them. PR #100 resolves the blocking external-review finding by forwarding the
host-side `PUBLIC_ENDPOINTS` override into the container.
