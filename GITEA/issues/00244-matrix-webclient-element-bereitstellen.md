---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#244
state: closed
updated_at: 2026-07-15T01:38:31+02:00
is_epic: false
labels:
  - "FLASH_FREE"
  - "sub-task"
publication: sanitized
---

# Matrix-Webclient (Element) bereitstellen

Parent: #212. Depends on: #220, #221.

## FLASH_FREE packet
Repo: `architecture`; branch: `feat/element-web-client`; create `pi/compose/element.yml`, `pi/element/config.json.example`, `docs/matrix/element.md` and `pi/tests/test_element_compose.sh`.

Implement: an ARM64-capable, digest-pinned Element Web container behind `frontproxy_default` for `<internal-host>`. Supply a static, non-secret runtime configuration that points only to `<internal-gitea-reference> disables public registration and third-party integrations by default, and avoids host-port bindings. Persist only configuration required by the image; do not store credentials in the web client.

Tests first: Compose parse without real secrets; static assertions for the pinned image, frontproxy-only exposure, exact Matrix base URL, disabled guest/registration paths, no analytics defaults and no embedded secrets.

Operator prerequisites: CNAME `<internal-host>` is present; certificate issuance and external HTTPS smoke test occur only after merge and manual deployment.

Do not: deploy Element, change DNS, expose a host port, add Matrix accounts, enable public registration, or place tokens in Git.

Done: Element can be deployed through the existing proxy pattern and documented smoke steps cover HTTPS, discovery, login to the private Synapse instance and rollback.

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
- Repository: `architecture`. Exakte Worktree(s): `<local-path-redacted>`. Branch: `feat/element-web-client`. Vor jedem Editieren exakt `git status --short --branch` ausfuehren.
- Unrelated working-tree changes nicht zuruecksetzen oder ueberschreiben; melden und stoppen.
- Erlaubt sind nur die oben genannten Paketpfade sowie die folgenden fokussierten Testpfade: `pi/compose/element.yml; pi/element/config.json.example; docs/matrix/element.md; pi/tests/test_element_compose.sh`. Generierte Dateien duerfen nur ueber den vorhandenen Generator entstehen.
- Keine ungeplanten Refactorings, Adapter-Umbauten oder Aenderungen an anderen Issues.

### Verbindliche Nachweise
- Fokus-Test aus dem jeweiligen Repository-Root, exakt und in dieser Form: `bash pi/tests/test_element_compose.sh && docker-compose -f pi/compose/element.yml config`.
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
