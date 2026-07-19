# INSTRUCTIONS.md — GH-45 Media Upload Limits Review

This PR transports the exact source diff and evidence for GH-45 (Telegram
registration + homogeneous three-bridge stand) and the follow-up media-upload
limit fixes.

Review `docs/review/gh45-media-upload-limits/CHANGES.diff` against the
accompanying root-cause, risk, and testing evidence.

## Scope of this PR

Runtime configuration fixes on the Pi5 (192.168.2.30) that remove the
HTTP 413 media-upload barrier:

1. Synapse `max_upload_size: 100M` added to the versioned template
   `synapse.yaml.example` so it survives container recreation.
2. Frontproxy `client_max_body_size 100m` for `matrix.hl.maier.wtf`
   (fixes web-app / Element uploads) and `cwa.hl.maier.wtf` (Calibre-Web).
3. All three bridge `public_address` set to the internal Synapse URL
   `http://compose-synapse-1:8008`.

## Gate

Approval permits recording the configuration in the versioned
`Homelab/Architecture` repository. It does NOT itself authorize any
production recreation beyond what was already deployed and verified live.
If changes are requested, a corrective source PR is required before merge
into the Architecture repo.

GH-45 is already operationally complete and closed; this PR only captures
the versioned record of the config mutations.
