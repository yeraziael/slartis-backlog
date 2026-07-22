# PW-D01 Test Evidence

## Source Identity

- Repository: `Homelab/Architecture`
- PR: `#78`
- Base: `ed54f1144f1df21af13c9a2a1fd5c685fa2a95ac`
- Head: `2683d9542b21eaa2d70907f4306a023460774ee1`
- Changed file: `docs/decisions/playwright/runner-bootstrap.md`

## Local Validation

The following commands passed against the exact source head:

```bash
test -f AGENTS.md \
  && test -f ci-manifest.yaml \
  && test -f ci-generate.py \
  && test -f Makefile \
  && test -f docs/decisions/playwright/runner-bootstrap.md

make lint
make test
git diff --check origin/main...HEAD
```

Focused contract assertions also passed for the selected image tag, index and
linux/amd64 manifest digests, Node/npm versions, exact package version,
Chromium version, Make target, network modes, UID/GID execution, and registry
contract.

`make lint` included internal-link validation, Compose validation, whitespace
validation, and the repository secret scan. The complete repository unit suite
passed under `make test`.

## Gitea CI

| Event | Run | Linting & Validation | Unit Tests | Reporting |
|---|---:|---|---|---|
| push | [658](https://gitea.hl.maier.wtf/Homelab/Architecture/actions/runs/658) | success, job 2529 | success, job 2530 | success, job 2531 |
| pull request | [659](https://gitea.hl.maier.wtf/Homelab/Architecture/actions/runs/659) | success, job 2532 | success, job 2533 | success, job 2534 |

Aggregate source commit status: `success`, six of six contexts successful.

## Runtime And Blackbox Scope

No browser, image, container, service, account, credential, DNS record, or
deployment was executed or mutated. Runtime blackbox testing is intentionally
not applicable to this architecture-decision ticket; PW-I01 owns implementation
and the first controlled platform self-test after this decision is accepted.
