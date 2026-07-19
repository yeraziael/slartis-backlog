# Scope And Risks

## Delivered

- Adds only `/data/appservice/mautrix-whatsapp.yaml` to the versioned active list
- Preserves Signal and Telegram
- Keeps Facebook and Instagram inactive
- Updates the exact active-list contract test

## Not Performed

- No registration, database, state directory, container, or Synapse mutation
- No account linking or QR generation
- No secret or runtime data access

## Runtime Gate

Before Synapse recreation, GH-40 must create and validate the real WhatsApp
registration, complete a restricted backup, and preserve the previous
Signal/Telegram list for first-deployment rollback.
