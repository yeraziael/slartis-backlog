---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#242
state: closed
updated_at: 2026-07-16T22:00:38+02:00
is_epic: false
labels:
  - "FLASH_FREE"
  - "in-progress"
  - "sub-task"
publication: sanitized
---

# CI: Architecture PR-Gates fuer Matrix-Dokumentation und Compose

Parent: #212. Unblocks CI-gated merge of Architecture PRs including #7.

## FLASH_FREE packet
Repo: `architecture`; branch: `ci/architecture-baseline`.
Read: current `README.md`, `docs/`, `pi/`, existing Homelab CI conventions in `lydia/home-repo`; do not copy credentials or deployment logic.
Implement: manifest-first minimal Gitea Actions CI for this documentation/infrastructure repository: Markdown internal-link validation, `docker compose config` for tracked Compose inputs, `git diff --check`, and a secret-pattern scan. Add a Makefile or equivalent local entry point only if generated from the manifest.
Tests first: generator/manifest test plus a fixture that fails for a broken link and a floating/invalid Compose input.
Do not: deploy, add production secrets, alter Pi files, change branch protection, merge PR #7.
Done: CI posts required PR contexts for #7; local and CI commands use the same checks; all generated files derive from one source of truth.

## Review-Korrektur 2026-07-14

Der erste Fix fuer den Shallow-Checkout darf nicht nur auf `HEAD~1...HEAD` zurueckfallen: Das prueft bei Pull Requests nur den letzten Commit und kann Whitespace-Fehler in frueheren PR-Commits uebersehen.

Korrigiere den Pull-Request-Pfad so, dass der Base-Branch mit explizitem Ref-Mapping nach `refs/remotes/origin/<base>` geladen wird und ein echter Merge-Base-Diff gegen diesen Ref erfolgt. Ein Fallback ist nur fuer den belegten Initial-Commit-Fall zulaessig und muss den vollstaendigen vorhandenen Diff pruefen, nicht nur den Parent-Diff.

Tests: Ein mehrcommitiger PR-Fall muss einen Whitespace-Fehler im ersten, aber nicht letzten Feature-Commit erkennen. Der Test muss beweisen, dass der Base-Ref nach dem Fetch unter `origin/<base>` vorliegt.

## Runner-Befund und verbindliche dritte Korrektur 2026-07-14

Die echten Gitea-Logs fuer PR-Run 278 belegen zwei Ursachen:

1. `actions/checkout@v4` holt den PR-Head weiterhin mit `--depth=1`. Der Base-Ref-Fetch findet deshalb keinen Merge-Base; der Script-Pfad behandelt den Checkout als Initial-Commit und prueft den vollen Baum. Dabei schlagen historische Whitespace-Fehler ausserhalb des PR-Diffs fehl.
2. Der Testjob erbt in einem Pull-Request-Run `GITHUB_BASE_REF=main`. Die Tests fuer simulierten Push- und fehlenden-Base-Ref-Modus muessen diese Variable explizit entfernen, statt die Runner-Umgebung zu erben.

Verbindliche Umsetzung:

* In `.gitea/workflows/ci.yaml` bei allen `actions/checkout@v4`-Schritten `with: fetch-depth: 0` setzen, damit der PR-Head und der Base-Branch einen echten Merge-Base haben. Das ist fuer diese kleine Dokumentations-/Infrastrukturhistorie akzeptabel und der direkte Fix fuer den realen Runner-Kontext.
* `check-git-diff.sh` behaelt den vollstaendigen Merge-Base-Diff bei; kein Initial-Commit-Pfad fuer normale Pull Requests.
* Teste die CI-Szenarien mit explizit gesetzten bzw. via `env -u GITHUB_BASE_REF` entfernten GitHub-Eventvariablen.
* Keine Bereinigung historischer Whitespace-Fehler, weil sie ausserhalb des PR-Diffs liegen.

Akzeptanz: Der echte Gitea-PR-Run prueft `origin/main...HEAD`, Lint und Unit Tests sind gruen, und ein mehrcommitiger PR mit Whitespace im ersten Commit wird weiterhin abgewiesen.

## Vekling-Ausfuehrung

Worktree: <local-path-redacted>

Vor dem Editieren: `git status --short --branch` im Worktree.

Lokaler Nachweis: Fuehre jeden im Paket genannten fokussierten Test aus dem Repository-Root aus. Anschliessend aus demselben Worktree zwingend:

    make ci
    git diff --check

Ein Test aus einem anderen Verzeichnis oder nur ein zusammengefasster Testbericht gilt nicht als Nachweis.
## Flash-Free Execution Contract (Control-Plane Revision)

Dieser Abschnitt ergaenzt das fachliche Paket oben und ist fuer den naechsten Flash-Free-Arbeitsversuch verbindlich.

### Abhaengigkeits-Gate
- Vor dem Editieren jeden `Depends on`-Vorgaenger gegen den Remote-Status pruefen.
- Ist ein Vorgaenger nicht gemerged/geschlossen, mit `BLOCKED` stoppen und nichts erraten. Unabhaengige Vorbereitung ist nur zulaessig, wenn dieses Issue sie ausdruecklich erlaubt.

### Worktree, Branch und Scope
- Repository: `architecture`. Exakte Worktree(s): `<local-path-redacted>`. Branch: `ci/architecture-baseline`. Vor jedem Editieren exakt `git status --short --branch` ausfuehren.
- Unrelated working-tree changes nicht zuruecksetzen oder ueberschreiben; melden und stoppen.
- Erlaubt sind nur die oben genannten Paketpfade sowie die folgenden fokussierten Testpfade: `the manifest, generator inputs, generated Makefile/workflow and named fixtures only`. Generierte Dateien duerfen nur ueber den vorhandenen Generator entstehen.
- Keine ungeplanten Refactorings, Adapter-Umbauten oder Aenderungen an anderen Issues.

### Verbindliche Nachweise
- Fokus-Test aus dem jeweiligen Repository-Root, exakt und in dieser Form: `bash tests/test_checks.sh && python3 tests/test_ci_generator.py`.
- Danach die vollstaendige Repository-Suite: `make ci`.
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
