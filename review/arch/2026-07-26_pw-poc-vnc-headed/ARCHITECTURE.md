# Architecture Review

## Existing Headless Path

The existing `tests/playwright/runner/run.sh platform` path runs the pinned
Playwright image ephemerally for CI and platform self-tests. The shared config
defaults to `headless: true`, and the existing Docker invocation remains the
headless test authority.

## Added Headed Path

The headed path is deliberately separate:

```text
tools/playwright-headed/run.sh
    |
    +-- build pinned base + Xvfb + x11vnc image
    +-- start detached container
    +-- wait for host VNC TCP readiness
    +-- send address and password to Telegram
    |
    v
Xvfb :99 -> x11vnc :5900 -> Chromium headed mode
                              |
                              +-- public Homelab HTTPS endpoint loop
```

The repository is mounted read-only at `/workspace`. The container has no
Docker socket. Runtime output is mounted separately under the ignored
`test-results/playwright-headed` path.

## Endpoint Workflow

The default registry contains these public FQDNs:

- `auth.hl.maier.wtf`
- `audiobookshelf.hl.maier.wtf`
- `cwa.hl.maier.wtf`
- `element.hl.maier.wtf`
- `gitea.hl.maier.wtf`
- `gitea-mcp.hl.maier.wtf`
- `matrix.hl.maier.wtf`
- `pprls.hl.maier.wtf`
- `pprlsf.hl.maier.wtf`

Each endpoint receives one ten-second display slot. The default ten rounds are
bounded and the process exits after the final slot. A navigation or TLS error
is rendered in a fresh browser tab and does not abort later endpoints.

## Security Boundary

The VNC listener is password-protected and Docker binds it to the Homelab LAN
address by default. The VNC password is generated at runtime and the Telegram
token is read from `~/.creds/telegram_slarti.token`; neither is committed.

The headed POC is not a persistent service. The operator must explicitly start
it and can stop it with `docker stop playwright-headed-poc`.

## Decision Relationship

This change extends, but does not replace, the PW-D01 runner decision in
`docs/decisions/playwright/runner-bootstrap.md`. Headless CI remains the
standard contract; VNC-headed execution is an operator-observable POC.
