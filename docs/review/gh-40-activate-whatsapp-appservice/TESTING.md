# Test Evidence

The active-appservice contract test was changed first and failed because the
template still contained only Signal and Telegram. Adding the WhatsApp path made
the focused test green.

All validations passed at source head
`17cedfdd9010c502e1137952a0f97813a9726da9`:

```bash
make lint
make test
git diff --check
bash scripts/scan-secrets.sh --staged
```

Gitea CI runs `554` and `555` both completed successfully.
