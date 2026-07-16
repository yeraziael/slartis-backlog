---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#240
state: open
updated_at: 2026-07-15T00:16:01+02:00
is_epic: false
labels:
  - "FLASH_FREE"
  - "sub-task"
publication: sanitized
---

# Matrix als primaeren internen Kanal freigeben

Parent: #212. Depends on: #238, #239 and explicit operator acceptance.

## FLASH_FREE packet
Repo: `architecture` and `home-repo`; branch: `release/matrix-primary-channel`.
Implement: only after acceptance, update architecture wording and gateway routing defaults so Matrix is primary internally while Telegram/Signal remain external fallback adapters.
Tests first: end-to-end contract verifies `/status`, task creation, approval, attachment, fallback alert and no bridge loop.
Do not: disable Telegram/Signal, enable federation, or merge/deploy without explicit approval.
Done: signed acceptance evidence, release manifest, rollback rehearsal and seven-day report attached.

## Vekling-Ausfuehrung

Dieses Paket hat zwei Worktrees und darf erst nach seinen Abhaengigkeiten delegiert werden:

* Architecture: <local-path-redacted>
* home-repo: <local-path-redacted>

Vor dem Editieren in beiden Worktrees: `git status --short --branch`.

Lokaler Nachweis:

    cd <local-path-redacted> && make ci && git diff --check
    cd <local-path-redacted> && make test && git diff --check

Die produktive Freigabe, Deployment und Kanalumschaltung bleiben Operator-Aktionen und sind kein Vekling-Output.
## Flash-Free Execution Contract (Control-Plane Revision)

Dieser Abschnitt ergaenzt das fachliche Paket oben und ist fuer den naechsten Flash-Free-Arbeitsversuch verbindlich.

### Abhaengigkeits-Gate
- Vor dem Editieren jeden `Depends on`-Vorgaenger gegen den Remote-Status pruefen.
- Ist ein Vorgaenger nicht gemerged/geschlossen, mit `BLOCKED` stoppen und nichts erraten. Unabhaengige Vorbereitung ist nur zulaessig, wenn dieses Issue sie ausdruecklich erlaubt.

### Worktree, Branch und Scope
- Repository: `architecture and home-repo`. Exakte Worktree(s): `<local-path-redacted> and <local-path-redacted>`. Branch: `release/matrix-primary-channel`. Vor jedem Editieren exakt `git status --short --branch` ausfuehren.
- Unrelated working-tree changes nicht zuruecksetzen oder ueberschreiben; melden und stoppen.
- Erlaubt sind nur die oben genannten Paketpfade sowie die folgenden fokussierten Testpfade: `the explicitly named release/routing/config paths in both worktrees; pi/tests/test_matrix_primary_channel.sh; runtime/tests/test_matrix_primary_channel.py; acceptance evidence and release manifest`. Generierte Dateien duerfen nur ueber den vorhandenen Generator entstehen.
- Keine ungeplanten Refactorings, Adapter-Umbauten oder Aenderungen an anderen Issues.

### Verbindliche Nachweise
- Fokus-Test aus dem jeweiligen Repository-Root, exakt und in dieser Form: `architecture: bash pi/tests/test_matrix_primary_channel.sh; home-repo: python3 runtime/tests/test_matrix_primary_channel.py`.
- Danach die vollstaendige Repository-Suite: `architecture: make ci; home-repo: make test`.
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
