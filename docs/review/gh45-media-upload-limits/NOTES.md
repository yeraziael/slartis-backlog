# NOTES.md — GH-45 Media Upload Limits (revised)

## Root cause (version-corrected)

- Public frontproxy vhost `matrix.hl.maier.wtf` had no `client_max_body_size`
  directive. The nginx-proxy default is `1m` (1 MiB); requests above that were
  rejected with HTTP 413. The Element **web app** uploads media to
  `matrix.hl.maier.wtf` through this proxy, so every upload failed. The Element
  **iOS app** used a different path and was unaffected.
- Synapse `max_upload_size` default is `50M` (current Synapse documentation).
  The deployed version is **Synapse 1.156.0** (image
  `ghcr.io/element-hq/synapse@sha256:6882d265...`). With no explicit value,
  uploads above 50M would be capped. The proxy 100m and Synapse 100M are now
  aligned.
- nginx-proxy image is `jwilder/nginx-proxy:latest`.

## Correction vs. first package

- `appservice.public_address` was wrongly set to the Synapse URL. Per review,
  this field serves optional public-media for the bridge appservice and must
  stay `null` while `public_media.enabled=false`. Reverted to `null` on all
  three bridges. This is NOT part of the versioned change.
- Calibre-Web (cwa) vhost change removed from GH-45 scope (own work item).

## Verification performed (live, on Pi5)

- `nginx -t` passed; graceful `nginx -s reload` applied.
- Authenticated upload via `https://matrix.hl.maier.wtf/_matrix/media/v3/upload`
  with a real user token: 2 MB -> HTTP 200, 50 MB -> HTTP 200 (no 413; body
  stored, mxc URI returned).
- Synapse healthy after recreate; `max_upload_size: 100M` persisted from
  template (verified present post-recreate).
- All three bridges `live`/`ready` = HTTP 200 (no regression) after the
  `public_address` revert.
- Operator confirmed: Telegram, Signal, WhatsApp media upload all working.

## Security closure

- `tg_SECRET_HANDOVER.tmp` (held the Telegram api_id/api_hash) was deleted from
  `~/.creds/` after the credentials were written into the runtime bridge config
  (mode 0600). No plaintext copy remains outside the intended runtime config.
  Verified: `ls ~/.creds/ | grep -i SECRET_HANDOVER` returns nothing.

## Risk

- Low. Additive Synapse media key; frontproxy body-size increase to 100m on a
  private homelab. No new host ports, no frontproxy exposure change.
- No secrets in `synapse.yaml.example` were touched; only `max_upload_size` was
  added below the existing `media_store_path`.
