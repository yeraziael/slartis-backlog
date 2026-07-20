# TESTING.md — GH-45 Media Upload Limits (revised, two-source-PR)

## Authenticated blackbox (passed live)

Action: As an authenticated Matrix user, upload files of increasing size to
`https://matrix.hl.maier.wtf/_matrix/media/v3/upload` via the public proxy.
Expected: HTTP 200 and an `mxc://` URI returned (body stored).

Evidence (redacted: no token, no file content, no identifiers):
- 2 MB upload  -> HTTP 200, mxc URI returned
- 50 MB upload -> HTTP 200, mxc URI returned
(Unauthenticated requests correctly return 401; that only proves auth, not
upload success — the above uses a valid user token.)

Action: In the Element web app (element.hl.maier.wtf), upload an image and a
file to a Matrix room.
Expected: Upload succeeds; media renders.
Evidence: Operator confirmed web-app upload works (no 413).

## Bridge-media observations (contextual, do NOT satisfy #46/#47)

Operator reported Telegram, Signal and WhatsApp media uploads working in live
operation. These are contextual observations for this package's upload-path
limit fix and are tracked separately in #46 and #47, which remain open for
their full acceptance criteria.

## Regression gates (all green)

- Synapse container healthy after recreate.
- `max_upload_size: 100M` present in active config after recreate (persistent).
- Telegram / Signal / WhatsApp bridge `live` and `ready` = HTTP 200 (also after
  the `public_address` revert to null).
- No new host port bindings; no frontproxy exposure change.
- Signal and WhatsApp remain healthy (unchanged).
