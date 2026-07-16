---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#230
state: closed
updated_at: 2026-07-15T14:23:00+02:00
is_epic: false
labels:
  - "FLASH_FREE"
  - "sub-task"
publication: sanitized
---

# Matrix Attachment Pipeline absichern

Parent: #212. Depends on: #226.

## FLASH_FREE packet
Repo: `home-repo`; branch: `feat/matrix-attachments`; create `runtime/matrix/attachments.py`; extend `runtime/matrix/client.py`; extend Envelope attachment metadata in `runtime/messaging/envelope.schema.json` and `docs/messaging-envelope-v1.md`; register the focused test through `ci-manifest.yaml` and regenerate `Makefile` plus `.gitea/workflows/ci.yaml` with `ci-generate.py`.
Implement: `MatrixClient.download_media(mxc_uri, max_bytes)` accepts only strict `mxc://<server-name>/<media-id>` values, constructs the authenticated `/_matrix/client/v1/media/download/{serverName}/{mediaId}` URL on the configured homeserver, reads at most `max_bytes + 1`, and returns bytes plus response MIME. Public pipeline interface: `process_attachment(client, source, max_size_bytes, allowed_mime_types, audit) -> metadata`; `source` requires `content_uri`, `content_type`, `filename`, `sender_id`, `room_id`, and `event_id`; accepted metadata contains only `content_uri`, normalized `content_type`, `filename`, `size_bytes`, and literal lowercase SHA-256. Reject non-MXC input before network access, over-limit media, missing/disallowed/mismatched MIME and timeouts with typed errors plus a redacted quarantine audit record. Never place bytes/base64 in Envelope metadata.
Tests first: `runtime/tests/test_matrix_attachments.py` covers PDF/image/audio/text, strict MXC parsing and local-homeserver endpoint construction, Authorization header without query token, non-MXC rejection before network, Content-Length and streamed over-limit responses, MIME mismatch, timeout, redacted quarantine audit, metadata without payload and an independently calculated hash literal. Extend `runtime/tests/test_message_envelope.py` for the new `content_uri` and `sha256` fields and `runtime/tests/test_ci_generator.py` to prove the focused test is present in generated CI.
Do not: execute, parse or log attachment contents; no arbitrary URL fetch.
Done: rejected media has a redacted audit record and quarantine reason.

## Vekling-Ausfuehrung

Worktree: <local-path-redacted>

Vor dem Editieren: `git status --short --branch` im Worktree.

Lokaler Nachweis: Fuehre jeden im Paket genannten fokussierten Test aus dem Repository-Root aus. Anschliessend aus demselben Worktree zwingend:

    make test
    git diff --check

Falls ein Paket ein neues Python-Testmodul erstellt, muss dessen exakter Aufruf im Paket ergaenzt und vor `make test` ausgefuehrt werden. Ein Test aus einem anderen Verzeichnis oder nur ein zusammengefasster Testbericht gilt nicht als Nachweis.
## Flash-Free Execution Contract (Control-Plane Revision)

Dieser Abschnitt ergaenzt das fachliche Paket oben und ist fuer den naechsten Flash-Free-Arbeitsversuch verbindlich.

### Abhaengigkeits-Gate
- Vor dem Editieren jeden `Depends on`-Vorgaenger gegen den Remote-Status pruefen.
- Ist ein Vorgaenger nicht gemerged/geschlossen, mit `BLOCKED` stoppen und nichts erraten. Unabhaengige Vorbereitung ist nur zulaessig, wenn dieses Issue sie ausdruecklich erlaubt.

### Worktree, Branch und Scope
- Repository: `home-repo`. Exakte Worktree(s): `<local-path-redacted>`. Branch: `feat/matrix-attachments`. Vor jedem Editieren exakt `git status --short --branch` ausfuehren.
- Unrelated working-tree changes nicht zuruecksetzen oder ueberschreiben; melden und stoppen.
- Erlaubt sind nur die oben genannten Paketpfade sowie die folgenden fokussierten Testpfade: `runtime/matrix/attachments.py; runtime/matrix/client.py; runtime/messaging/envelope.schema.json; docs/messaging-envelope-v1.md; runtime/tests/test_matrix_attachments.py; runtime/tests/test_message_envelope.py; ci-manifest.yaml; Makefile; .gitea/workflows/ci.yaml; runtime/tests/test_ci_generator.py`. Generierte Dateien duerfen nur ueber den vorhandenen Generator entstehen.
- Keine ungeplanten Refactorings, Adapter-Umbauten oder Aenderungen an anderen Issues.

### Verbindliche Nachweise
- Fokus-Test aus dem jeweiligen Repository-Root, exakt und in dieser Form: `python3 runtime/tests/test_matrix_attachments.py && python3 runtime/tests/test_message_envelope.py && python3 runtime/tests/test_ci_generator.py`.
- Danach die vollstaendige Repository-Suite: `make test`.
- Danach aus demselben Worktree: `git diff --check main...HEAD` und `git diff --name-only main...HEAD`.
- Falls `main`/`origin/main` fehlt, den Base-Branch explizit unter `origin/main` laden; niemals nur auf `HEAD~1` zurueckfallen und keinen unvollstaendigen PR-Diff akzeptieren.
- Neue Python-Tests immer mit dem oben genannten exakten Modulaufruf vor der Full-Suite ausfuehren.
- Vor dem Push den tatsaechlichen Diff, alle geaenderten Pfade und den Remote-PR-Head pruefen; nach dem Push die echten CI-Jobs/Logs kontrollieren.

### Delivery-Grenze
- Erlaubt: editieren, testen, committen, pushen und nur den zugehoerigen PR erstellen/aktualisieren.
- Verboten: Merge, Force-Push, Deployment, Service-/DNS-/Firewall-Aenderungen, Produktionsgeheimnisse und weitere Subagents.
- Abschlussbericht muss Commit, geaenderte Dateien, jeden exakten Befehl mit Ergebnis, PR-Head, CI-Run/Jobstatus und offene Einschraenkungen enthalten. Ein Worker-Bericht allein ist kein Testnachweis.

### Retry-Regel
- Bei Review- oder CI-Fehlern vor einem neuen Versuch zuerst Logbefund, Root Cause und konkrete Loesung in diesem Issue dokumentieren und den Retry-Scope begrenzen. Keine spekulativen Wiederholungen.
