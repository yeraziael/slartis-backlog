---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#231
state: closed
updated_at: 2026-07-16T23:31:26+02:00
is_epic: false
labels:
  - "FLASH_FREE"
  - "sub-task"
publication: sanitized
---

# Matrix Approvals an Lydia Execution Gate anbinden

Parent: #212. Depends on: #226, #227.

## FLASH_FREE packet
Repo: `home-repo`; branch: `feat/matrix-approvals`; create `runtime/matrix/approvals.py` and adapt only the existing approval boundary.
Implement: map `/approve <id>` and `/reject <id>` to existing Execution Gate with Matrix sender identity. Enforce principal binding, expiry and single use.
Tests first: `runtime/tests/test_matrix_approvals.py` proves valid approval, wrong user, expired, replay and unknown ID outcomes.
Do not: implement privileged command execution or bypass existing gate.
Done: audit entry has trace/event/approval IDs and no sensitive payload.

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
- Repository: `home-repo`. Exakte Worktree(s): `<local-path-redacted>`. Branch: `feat/matrix-approvals`. Vor jedem Editieren exakt `git status --short --branch` ausfuehren.
- Unrelated working-tree changes nicht zuruecksetzen oder ueberschreiben; melden und stoppen.
- Erlaubt sind nur die oben genannten Paketpfade sowie die folgenden fokussierten Testpfade: `runtime/matrix/approvals.py; the existing approval-boundary files strictly required by the packet; runtime/tests/test_matrix_approvals.py`. Generierte Dateien duerfen nur ueber den vorhandenen Generator entstehen.
- Keine ungeplanten Refactorings, Adapter-Umbauten oder Aenderungen an anderen Issues.

### Verbindliche Nachweise
- Fokus-Test aus dem jeweiligen Repository-Root, exakt und in dieser Form: `python3 runtime/tests/test_matrix_approvals.py`.
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
