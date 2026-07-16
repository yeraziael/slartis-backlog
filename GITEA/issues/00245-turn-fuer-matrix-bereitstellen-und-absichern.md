---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#245
state: closed
updated_at: 2026-07-16T23:07:15+02:00
is_epic: false
labels:
  - "FLASH_FREE"
  - "sub-task"
publication: sanitized
---

# TURN fuer Matrix bereitstellen und absichern

Parent: #212. Depends on: #219, #220, #236.

## FLASH_FREE packet
Repo: `architecture`; branch: `feat/matrix-turn`; create `pi/compose/coturn.yml`, `pi/coturn/turnserver.conf.example`, `pi/coturn/turn.env.example`, `docs/matrix/turn.md` and `pi/tests/test_coturn_compose.sh`.

Implement: an ARM64-capable, digest-pinned Coturn service for the private Matrix deployment. Use external secret-file references for the shared TURN secret and TLS key material, explicit relay-port range, rate/abuse limits, healthcheck, CPU/RAM limits and restrictive container settings. Add the required Synapse TURN configuration contract without writing real credentials.

Network boundary: TURN media cannot traverse nginx-proxy. Bind only the documented TURN listener and relay TCP/UDP ports required for `<internal-host>`; do not publish unrelated ports or join `frontproxy_default`. TLS certificate acquisition, host firewall changes and DNS propagation remain operator-run production actions.

Tests first: Compose parse without real secrets; static assertions reject floating images, missing secret-file references, Docker socket mounts, broad host port ranges, missing UDP listener/relay contract and insecure TLS paths.

Operator prerequisites: CNAME `<internal-host>`; firewall approval for the documented minimal port range; a certificate/key provisioned outside Git before deployment.

Do not: deploy Coturn, alter firewall/DNS, expose unauthenticated relay service, embed shared secrets or certificates, or enable federation.

Done: the versioned configuration and runbook define a private, credentialed TURN path that can be deployed and rolled back independently of Synapse.

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
- Repository: `architecture`. Exakte Worktree(s): `<local-path-redacted>`. Branch: `feat/matrix-turn`. Vor jedem Editieren exakt `git status --short --branch` ausfuehren.
- Unrelated working-tree changes nicht zuruecksetzen oder ueberschreiben; melden und stoppen.
- Erlaubt sind nur die oben genannten Paketpfade sowie die folgenden fokussierten Testpfade: `pi/compose/coturn.yml; pi/coturn/turnserver.conf.example; pi/coturn/turn.env.example; docs/matrix/turn.md; pi/tests/test_coturn_compose.sh`. Generierte Dateien duerfen nur ueber den vorhandenen Generator entstehen.
- Keine ungeplanten Refactorings, Adapter-Umbauten oder Aenderungen an anderen Issues.

### Verbindliche Nachweise
- Fokus-Test aus dem jeweiligen Repository-Root, exakt und in dieser Form: `bash pi/tests/test_coturn_compose.sh && docker-compose -f pi/compose/coturn.yml config`.
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
