# GH-35 Test Evidence

## Test First

Initial red command:

```bash
bash pi/tests/test_mautrix_instagram_compose.sh
```

Observed red result: failed because `pi/compose/mautrix-instagram.yml` did not
exist.

A second RED/GREEN cycle required production logging to use level `info` and
stdout only. It failed against the generated upstream defaults (`debug` plus a
file writer), then passed after hardening the versioned config.

## Full Local Validation

All commands passed on implementation head
`957b7d23202a5946ab29ac92639f0d63c2fad869`:

```bash
make lint
make test
docker-compose -f pi/compose/mautrix-instagram.yml config -q
git diff --check
bash scripts/scan-secrets.sh --staged
```

The current `ig-v26.07` image generated a registration with ID `instagram`,
internal URL `http://mautrix-instagram:29330`, and exclusive bot and ghost
namespaces. Runtime tokens were distinct and were neither printed nor
committed.

Manifest inspection from the Pi 5 confirmed Linux amd64 and arm64 entries. The
versioned Compose file pins the multi-arch manifest
`sha256:3f9c260c05c8880e1d7d54677e311e530afdcbd4ec08e4f42f1273b47579e881`,
not the ARM64 architecture descriptor.
