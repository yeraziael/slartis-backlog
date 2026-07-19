# NOTES.md — GH-45 Media Upload Limits

## Root cause

- Public frontproxy vhost `matrix.hl.maier.wtf` had no `client_max_body_size`
  directive. nginx default blocked any request body above ~64 KB with
  HTTP 413. The Element **web app** (element.hl.maier.wtf) uploads media to
  `matrix.hl.maier.wtf` through this proxy, so every upload failed. The
  Element **iOS app** used a different path and was unaffected.
- `cwa.hl.maier.wtf` (Calibre-Web) had no vhost.d override at all, so it
  inherited the same default body-size limit → 413 on uploads.
- Synapse had no explicit `max_upload_size`, defaulting to 10 MB. Even after
  the proxy fix, Synapse would have capped uploads below the new 100 MB proxy
  limit.
- All three mautrix bridges had `public_address` pointing at a placeholder
  (`bridge.example.com`) or `null`, which broke mxc:// media resolution for
  outbound transfers.

## Verification performed (live, on Pi5)

- `nginx -t` passed; graceful `nginx -s reload` applied.
- 5 MB and 10 MB uploads via `https://matrix.hl.maier.wtf/_matrix/media/v3/upload`
  returned no 413 (only 401 due to test token).
- 50 MB upload via proxy returned no 413 after Synapse `max_upload_size` applied.
- `cwa.hl.maier.wtf` large POST returned 405 (method-specific) instead of 413.
- Synapse healthy after recreate; `max_upload_size: 100M` persisted from template.
- All three bridges `live`/`ready` = HTTP 200 (no regression).
- Operator confirmed: Telegram, Signal, WhatsApp media upload all working.

## Risk

- Low. Changes are additive (body-size limits, one new Synapse media key).
- `client_max_body_size 100m` raises the max request body; acceptable for a
  private homelab. No new exposure (no host ports, no frontproxy change beyond
  body size).
- Secrets in `synapse.yaml.example` were NOT touched or reproduced; only the
  `max_upload_size` line was added below the existing `media_store_path`.
