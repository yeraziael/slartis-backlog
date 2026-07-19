# GH-34 Test Evidence

## Test First

Red command:

```bash
bash pi/tests/test_mautrix_facebook_compose.sh
```

Observed red result: failed because `pi/compose/mautrix-facebook.yml` did not
exist.

After implementation, the focused test passed all 42 contract assertions.

## Full Local Validation

All commands passed on implementation head
`8d5d556344c3d3891eb27da785f3a4f8e09b4b32`:

```bash
make lint
make test
docker-compose -f pi/compose/mautrix-facebook.yml config -q
git diff --check
```

The secret scan covered 118 tracked files and passed. The current v26.07 image
generated a registration with ID `facebook`, internal URL
`http://mautrix-facebook:29319`, exclusive bot and ghost namespaces, and
distinct runtime tokens. Token values were not printed or committed.

Manifest inspection on the Pi 5 confirmed Linux amd64 and arm64 entries for
`sha256:c65eb7f10a3880933490972bed574678874d780df70458a5ab0568157f9cc15c`.
