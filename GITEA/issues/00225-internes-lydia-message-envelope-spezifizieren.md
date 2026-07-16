---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#225
state: closed
updated_at: 2026-07-15T00:02:50+02:00
is_epic: false
labels:
  - "FLASH_FREE"
  - "sub-task"
publication: sanitized
---

# Internes Lydia Message Envelope spezifizieren

Parent: #212. Depends on: #215.

## FLASH_FREE packet
Repo: `home-repo`; branch: `feat/message-envelope-v1`; create `runtime/messaging/envelope.schema.json`, `runtime/messaging/validate_envelope.py`, `docs/messaging-envelope-v1.md`.
Implement: versioned channel-neutral envelope with message/trace/origin IDs, sender, room/chat target, reply, text and attachment metadata. Require origin and hop fields for bridges.
Tests first: `runtime/tests/test_message_envelope.py` accepts canonical Telegram/Signal/Matrix fixtures and rejects missing IDs, invalid MIME, and malformed hops.
Do not: change existing adapters yet.
Done: JSON Schema is the sole compatibility contract and has examples.

## Vekling-Ausfuehrung

Worktree: <local-path-redacted>

Vor dem Editieren: `git status --short --branch` im Worktree.

Lokaler Nachweis: Fuehre jeden im Paket genannten fokussierten Test aus dem Repository-Root aus. Anschliessend aus demselben Worktree zwingend:

    make test
    git diff --check

Falls ein Paket ein neues Python-Testmodul erstellt, muss dessen exakter Aufruf im Paket ergaenzt und vor `make test` ausgefuehrt werden. Ein Test aus einem anderen Verzeichnis oder nur ein zusammengefasster Testbericht gilt nicht als Nachweis.

## Test-Ergaenzung

Der vor `make test` zwingende fokussierte Nachweis fuer das neue Python-Testmodul lautet aus dem Repository-Root:

    python3 runtime/tests/test_message_envelope.py

## Retry-Contract nach Review #3229

Der Retry auf `feat/message-envelope-v1` behebt ausschließlich die vier Review-Funde aus Kommentar #3229. Zusätzlich zu den ursprünglichen vier Dateien darf er nur diese CI-Quellen und daraus generierten Artefakte ändern:

- `ci-manifest.yaml`
- `Makefile`
- `.gitea/workflows/ci.yaml`

Vorgaben:
1. Entferne jeden Trailing Whitespace; `git diff --check main...HEAD` muss grün sein.
2. `envelope_version` ist für v1 exakt `1`; Tests verwerfen 0 und 2.
3. `message_id`, `origin_id`, `sender.id` und `target.id` haben `minLength: 1`; Tests verwerfen Leerstrings.
4. Registriere `python3 runtime/tests/test_message_envelope.py` in `ci-manifest.yaml` als Unit-Test-Schritt und regeneriere Makefile und Workflow mit dem vorhandenen Generator. `make test` sowie die Gitea Unit-Test-Jobliste müssen den Test ausführen.
5. Führe vor Push fokussierten Test, `make test`, `git diff --check main...HEAD` und den Generator-Nachweis aus.

Keine Adapter-, Deployment- oder Secret-Änderungen. Kein PR, kein Merge, kein Force-Push.
## Retry Contract after Control-Plane Review #3242

The existing PR is `lydia/home-repo#358` on branch `feat/message-envelope-v1`, currently at `e64226f`. PR CI run `304` is green. Update this PR; do not create a second PR. The earlier `No PR` instruction above is superseded.

The control-plane review found one additional blocking defect:

1. Hop objects require `from_channel` and `to_channel`, but both fields accept empty strings. The payload `{"from_channel":"","to_channel":"","timestamp":0}` currently validates. For an auditable bridge history, both channel fields must be non-empty.

Retry scope for this attempt is strictly limited to:

- `runtime/messaging/envelope.schema.json`
- `runtime/tests/test_message_envelope.py`

Requirements:

1. Add `minLength: 1` to both hop channel fields.
2. Add regression tests that reject an empty `from_channel` and an empty `to_channel`.
3. Preserve all previous review fixes and do not change adapters, documentation, CI configuration, deployment, or secrets.
4. Use the exact worktree `<local-path-redacted>` and branch `feat/message-envelope-v1`.
5. Before push, run from the repository root: `python3 runtime/tests/test_message_envelope.py`, `make test`, `python3 runtime/tests/test_ci_generator.py`, and `git diff --check main...HEAD`.

Execution authorization: one retry using `openai/gpt-5.6-luna` (LUNA), explicitly approved by the operator as the temporary session replacement for TERRA.

Allowed actions: edit the two permitted files, run tests, commit, push, and update PR #358. Forbidden: merge, force-push, deployment, service/DNS/firewall changes, production secrets, and subagents.
## Dependency clarification

Although dependency #215 remains in progress, this is a correction-only retry of the already-open PR #358. It is explicitly permitted as independent preparation: it does not modify or integrate the Synapse/Keycloak ADR, and it must remain limited to the two files and commands above.
