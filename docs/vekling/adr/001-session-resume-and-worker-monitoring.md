# ADR-001: Monitor Vekling Lifecycle Events And Preserve Session Workspace Identity

**Status:** proposed
**Date:** 2026-07-19
**Evidence:** `../evidence/E-003/`

## Context

E-003 reproduced two silent-looking continuation states. One was a pending
`external_directory` permission request after provider and model selection. The
other selected Hy3 successfully, denied access to a replacement worktree,
advanced multiple loop steps, and exited cleanly without a final response,
commit, PR, or error event.

The same experiment showed that resuming a session by ID preserved the original
session directory. Passing another `--dir` bootstrapped that directory but did
not rebind the existing session; the replacement worktree remained external to
the session workspace.

## Decision

Vekling orchestration will treat the session's original workspace as immutable
identity for the lifetime of that session. Corrections should remain in that
workspace where possible. A replacement worktree requires an explicit,
least-privilege `external_directory` rule or a separately approved fresh
implementation session.

The Vekling monitor will derive state from runtime events, not elapsed silence.
It must distinguish at least:

- `starting`
- `provider_ready`
- `model_active`
- `waiting_permission`
- `tool_active`
- `tool_denied`
- `exited_without_delivery`
- `delivered`
- `failed`

A process exit or `exiting loop` event is not success. Delivery requires the
contract's independently verified artifacts.

## Facts

- OpenCode 1.17.20 selected provider `opencode` and model `hy3-free` before both
  silent-looking states.
- `external_directory` defaults to ASK for paths outside the bound workspace.
- A resumed session tracked the original directory despite a different CLI
  `--dir`.
- Explicitly allowing the replacement worktree let the same session produce
  commit `23e8f0a` and draft Gitea PR #37.

## Unknowns

- OpenCode documentation states that `--auto` approves ASK requests unless they
  are denied, but the resumed session still waited for the credential-directory
  request. The root cause is not established.
- It is not established whether exact credential-file rules can satisfy a
  permission request normalized to a parent wildcard in all tool paths.

## Consequences

- Monitoring needs permission and loop-exit event ingestion, redacted resource
  display, and deliverable verification.
- Worker prompts and launchers must declare the bound workspace separately from
  any requested replacement path.
- Credentials must not be exposed to resolve permission waits; operators choose
  constrained once/always approval, environment-based avoidance, or denial.
- Implementation is handed to GitHub issue #32. Reviewer-gated auto-merge is
  separately handed to issue #33.
