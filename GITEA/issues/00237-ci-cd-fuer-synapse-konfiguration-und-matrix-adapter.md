---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#237
state: open
updated_at: 2026-07-15T00:16:01+02:00
is_epic: false
labels:
  - "FLASH_FREE"
  - "sub-task"
publication: sanitized
---

# CI/CD fuer Synapse-Konfiguration und Matrix-Adapter

Parent: #212. Depends on: #219, #226, #241.

## FLASH_FREE packet
Repo: `home-repo`; branch: `ci/matrix-release-gates`; update `ci-manifest.yaml` and generated CI inputs only through the project generator.
Implement: gates for Envelope/adapter tests, Compose parse, secret scan, release-manifest validation and isolated Synapse integration test. Gate release on immutable artifacts and backup/restore evidence supplied by #241.
Tests first: extend CI generator tests with a matrix fixture and assert required jobs/commands.
Do not: add production secrets, deploy from CI, hand-edit generated workflow.
Done: `ci-generate.py` output is reproducible and CI runs without production access.

## Eddie Merge Gate

Nach erfolgreicher CI plant Eddie den Merge mit `merge_when_checks_succeed=true`; der FLASH_FREE-Agent erstellt nur Commit, Push und PR. Merge ist erst zulaessig, wenn die exakten erforderlichen Gitea-Status-Kontexte am aktuellen PR-Head grün sind und die repository-spezifischen Approval-/Protection-Regeln erfüllt sind. Kein Force-Merge, kein Admin-Bypass und kein Deployment durch den Merge.

Depends on: #242 Architecture CI baseline and #243 Eddie merge readiness before Architecture-owned Matrix configuration can enter the Eddie merge path.

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
- Repository: `home-repo`. Exakte Worktree(s): `<local-path-redacted>`. Branch: `ci/matrix-release-gates`. Vor jedem Editieren exakt `git status --short --branch` ausfuehren.
- Unrelated working-tree changes nicht zuruecksetzen oder ueberschreiben; melden und stoppen.
- Erlaubt sind nur die oben genannten Paketpfade sowie die folgenden fokussierten Testpfade: `ci-manifest.yaml; generated Makefile/workflow outputs; runtime/tests/test_ci_generator.py`. Generierte Dateien duerfen nur ueber den vorhandenen Generator entstehen.
- Keine ungeplanten Refactorings, Adapter-Umbauten oder Aenderungen an anderen Issues.

### Verbindliche Nachweise
- Fokus-Test aus dem jeweiligen Repository-Root, exakt und in dieser Form: `python3 runtime/tests/test_ci_generator.py`.
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
