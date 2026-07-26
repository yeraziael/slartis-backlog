# Risk Review

| Area | Risk | Likelihood | Impact | Mitigation |
|---|---|---:|---:|---|
| Security | VNC exposes a live browser display if the LAN bind is broadened. | Medium | High | Password authentication, LAN-only default bind, explicit operator start, no public bind by default. |
| Security | VNC password is delivered through Telegram and local output. | Medium | Medium | Runtime-only random password, no repository persistence, operator-controlled chat. |
| Operations | The endpoint loop can encounter unavailable or TLS-misconfigured services. | High | Low | Navigation errors become visible error tabs and do not abort later rounds. |
| Operations | A detached container can consume resources until stopped or ten rounds finish. | Medium | Medium | Bounded ten-round default, explicit container name, documented stop command. |
| Compatibility | Chromium/Playwright version drift can break the image. | Low | Medium | Immutable base digest, exact existing package lock, build-time `npm ci`. |
| Maintainability | Public endpoint registry can become stale as services change. | Medium | Low | Registry is documented and overridable with `PUBLIC_ENDPOINTS`; smoke output exposes failures. |
| Review | Canonical PRs were auto-merged before independent GitHub review. | Certain | Medium | This package is SHA-bound self-verification of the cumulative post-merge state only; independent review remains required. |
