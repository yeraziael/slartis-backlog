# TESTING.md — GH-45 Media Upload Limits

## Operator blackbox (already passed live)

Action: In the Element web app (element.hl.maier.wtf), upload an image and a
file to a Matrix room.
Expected: Upload succeeds; no error toast; media renders.
Evidence: Operator confirmed web-app upload works; 5/10/50 MB proxy uploads
returned no 413 (verified via curl with appservice token).

Action: In Calibre-Web (cwa.hl.maier.wtf), upload a book/file.
Expected: Upload succeeds.
Evidence: Large POST returned 405 (method-specific) instead of 413; body-size
barrier removed. Operator confirmed working.

Action: Send an image/file Matrix -> Telegram, Matrix -> Signal,
Matrix -> WhatsApp.
Expected: Media arrives on the remote platform.
Evidence: Operator confirmed all three bridge uploads work.

## Regression gates (all green)

- Synapse container healthy after recreate.
- `max_upload_size: 100M` present in active config after recreate (persistent).
- Telegram / Signal / WhatsApp bridge `live` and `ready` = HTTP 200.
- No new host port bindings; no frontproxy exposure change.
- Signal and WhatsApp remain healthy (unchanged).

## Reproduction for a reviewer

From a host with reachability to the proxy:
```
curl -s -o /dev/null -w "%{http_code}\n" -X POST \
  "https://matrix.hl.maier.wtf/_matrix/media/v3/upload?filename=t.bin&access_token=<token>" \
  --data-binary @<file> -H "Content-Type: application/octet-stream"
```
Expect any code other than 413 for bodies up to 100 MB.
