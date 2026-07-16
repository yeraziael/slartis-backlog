---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#227
state: closed
updated_at: 2026-07-15T12:43:36+02:00
is_epic: false
labels:
  - "FLASH_FREE"
  - "sub-task"
publication: sanitized
---

# Sync-Cursor und Matrix Event-Deduplizierung

Parent: #212. Depends on: #226.

## FLASH_FREE packet
Repo: `home-repo`; branch: `feat/matrix-sync-idempotency`; create `runtime/matrix/state_store.py` and `runtime/matrix/state.schema.json`.
Implement: durable cursor and processed-event store with atomic claim/complete semantics. Public interface: `claim(event_id)`, `complete(event_id, cursor)`, `is_processed(event_id)`.
Tests first: `runtime/tests/test_matrix_state_store.py` proves restart-before-complete retries once, restart-after-complete never reexecutes, and duplicate event is rejected.
Do not: use in-memory-only state or modify processor dispatch.
Done: storage failures fail closed and expose retryable error type.

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
- Repository: `home-repo`. Exakte Worktree(s): `<local-path-redacted>`. Branch: `feat/matrix-sync-idempotency`. Vor jedem Editieren exakt `git status --short --branch` ausfuehren.
- Unrelated working-tree changes nicht zuruecksetzen oder ueberschreiben; melden und stoppen.
- Erlaubt sind nur die oben genannten Paketpfade sowie die folgenden fokussierten Testpfade: `runtime/matrix/state_store.py; runtime/matrix/state.schema.json; runtime/tests/test_matrix_state_store.py`. Generierte Dateien duerfen nur ueber den vorhandenen Generator entstehen.
- Keine ungeplanten Refactorings, Adapter-Umbauten oder Aenderungen an anderen Issues.

### Verbindliche Nachweise
- Fokus-Test aus dem jeweiligen Repository-Root, exakt und in dieser Form: `python3 runtime/tests/test_matrix_state_store.py`.
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
