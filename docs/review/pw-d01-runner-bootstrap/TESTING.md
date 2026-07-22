# PW-D01 Test Evidence

## Source Identity

- Repository: `Homelab/Architecture`
- PR: `#79`
- Base: `3180722ba546dfd9d5434b4d3d71d32eb82ebd43`
- Effective review base: `ed54f1144f1df21af13c9a2a1fd5c685fa2a95ac`
- Head: `5e4e566ab143f3e1a3f9b6a7bbd8b5798dc1bacb`
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

Focused architecture self-audit assertions also passed for the exact package
script, bootstrap spec, lock validator, image tag, index and linux/amd64
manifest digests, Node/npm versions, package integrity, Chromium revision, Make
target, network modes, private shared memory, UID/GID rejection, tmpfs/cache,
deferred seams, testability, and upgrade/rollback sections.

Primary metadata was reverified without pulling or running the image:

- MCR index `sha256:5b8f294aff9041b7191c34a4bab3ac270157a28774d4b0660e9743297b697e48`.
- linux/amd64 manifest `sha256:cf0daee9b994042e011bc29f20cdff1a9f682a039b43fcd738f7d8a9d3bcd9d6`.
- `@playwright/test` `1.61.1` integrity `sha512-8nKv6+0RJSL9FE4jYOEGXnPeM/Hg12qZpmqzZjRh3qM0Y7c3z1mrOTfFLids72RDQYVh9WpLEfR5WdpNX4fkig==`.
- Chromium revision `1228`, browser version `149.0.7827.55`.

`make lint` included internal-link validation, Compose validation, whitespace
validation, and the repository secret scan. The complete repository unit suite
passed under `make test`.

## Gitea CI

| Event | Run | Linting & Validation | Unit Tests | Reporting |
|---|---:|---|---|---|
| push | [661](https://gitea.hl.maier.wtf/Homelab/Architecture/actions/runs/661) | success, job 2538 | success, job 2539 | success, job 2540 |
| pull request | [662](https://gitea.hl.maier.wtf/Homelab/Architecture/actions/runs/662) | success, job 2541 | success, job 2542 | success, job 2543 |

Aggregate source commit status: `success`, six of six contexts successful.

## Runtime And Blackbox Scope

No browser, image, container, service, account, credential, DNS record, or
deployment was executed or mutated. Runtime blackbox testing is intentionally
not applicable to this architecture-decision ticket; PW-I01 owns implementation
and the first controlled platform self-test after this decision is accepted.
