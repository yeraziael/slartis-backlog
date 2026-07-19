# TESTING.md — GH-45 Media Upload Limits (revised)

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

Action: Send an image/file Matrix -> Telegram / Signal / WhatsApp.
Expected: Media arrives on the remote platform.
Evidence: Operator confirmed all three bridge uploads work.

## Regression gates (all green)

- Synapse container healthy after recreate.
- `max_upload_size: 100M` present in active config after recreate (persistent).
- Telegram / Signal / WhatsApp bridge `live` and `ready` = HTTP 200 (also after
  the `public_address` revert to null).
- No new host port bindings; no frontproxy exposure change.
- Signal and WhatsApp remain healthy (unchanged).
