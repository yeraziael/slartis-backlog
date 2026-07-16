---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#217
state: closed
updated_at: 2026-07-14T21:19:36+02:00
is_epic: false
labels:
  - "FLASH_FREE"
  - "sub-task"
publication: sanitized
---

# Synapse ARM64 Proof of Concept auf dem Pi 5

Parent: #212. Depends on: #215.

## FLASH_FREE packet
Repo: `architecture`; branch: `feat/synapse-arm64-poc`; create `pi/compose/synapse-poc.yml` and `docs/matrix/poc-plan.md`.
Implement: isolated Synapse + PostgreSQL Compose with immutable ARM64-capable image digests, named HDD paths, healthchecks, CPU/RAM limits and no frontproxy/network exposure. Define measurement commands for idle, load, restart and disk.
Tests first: Compose parse and static assertions in `pi/tests/test_synapse_poc.sh`.
Do not: run on Pi, use production domain/data/keys, enable federation or OIDC.
Done: reproducible PoC definition and pass/fail resource budget; operator blackbox procedure.

## Vekling-Ausfuehrung

Worktree: <local-path-redacted>

Vor dem Editieren: `git status --short --branch` im Worktree.

Lokaler Nachweis: Fuehre jeden im Paket genannten fokussierten Test aus dem Repository-Root aus. Anschliessend aus demselben Worktree zwingend:

    make ci
    git diff --check

Ein Test aus einem anderen Verzeichnis oder nur ein zusammengefasster Testbericht gilt nicht als Nachweis.

## Review-Nachschärfung (verbindlich vor Retry)

Der erste Implementierungsversuch (`feat/synapse-arm64-poc`, Commit `a447ca5`) darf nicht als PR eingereicht werden. Der Retry muss zusätzlich erfüllen:

1. **HDD-Bind-Mounts versionieren:** Die Compose-Datei definiert direkt `driver_opts` mit `type: none`, `o: bind` und den drei Geräten unter `<local-path-redacted>{data,media,db}`. Kein manueller Compose-Edit als Setup-Schritt. Der statische Test prüft alle drei Bind-Mounts.
2. **Federation in versionierter Konfiguration deaktivieren:** Eine versionierte PoC-`homeserver.yaml` wird eingebunden. Ihr HTTP-Listener enthält nur `client` (nie `federation`); die Konfiguration enthält keinen Federation-Port. Der statische Test prüft diese konkrete Konfiguration.
3. **Isolierten Lasttest ausführbar machen:** Bei weiterhin fehlenden Host-Ports führt die Blackbox-Anleitung den Test innerhalb des Synapse-Containers oder über einen explizit isolierten Test-Client im PoC-Netz aus. Kein Host-`localhost:8008` ohne Port-Mapping.
4. **Gepinnte Digests prüfen:** Die Architektur-Verifikationsbefehle fragen exakt die in Compose verwendeten `sha256`-Index-Digests ab, nicht mutable Tags (`latest`, `17-alpine`). Der Test hält die erwarteten Digests fest.

Die neue Implementierung aktualisiert die statischen Tests zuerst. Bestehende Isolation bleibt erhalten: keine publizierten Ports, kein `frontproxy_default`, kein OIDC, keine reale Ausführung auf Pi5 und keine Produktionsdaten oder -secrets.

## Retry 2: Laufzeit-Anforderungen (verbindlich)

Der zweite Retry korrigiert Commit `b15fbc75` ohne Rebase oder Force-Push und muss diese nachweisbaren Bedingungen erfüllen:

1. **Gerenderter Config-Mount ist real:** Der relative Bind-Source in `pi/compose/synapse-poc.yml` löst vom Compose-Verzeichnis auf die tatsächlich versionierte Datei `pi/synapse-poc/homeserver.yaml` auf. Der statische Test ermittelt den Pfad relativ zur Compose-Datei und prüft `-f`; er darf nicht nur den Mount-Namen suchen.
2. **Versionierte Konfiguration ist vollständig referenzierbar:** Entferne `log_config`, sofern Synapse ohne diese Option auf stdout loggt, oder liefere eine versionierte, gemountete, nicht geheime Log-Konfiguration mit. Es darf keine Referenz auf eine nicht bereitgestellte Datei geben.
3. **Keine eingecheckten Runtime-Secrets, aber bootbarer Start:** Die `homeserver.yaml` benennt klare Pfade für jedes erforderliche Synapse-Runtime-Material. Der PoC-Plan enthält einen exakten, lokalen und einmaligen Befehl, der Signing Key und sonstige erforderliche lokale Secrets in den HDD-Datenpfad generiert, ohne eine versionierte Datei zu überschreiben oder Secrets auszugeben. Die statischen Tests prüfen den Konfigurationspfad und die dokumentierte Generierungsprozedur.
4. **Dokumentierter Startpfad:** Die Blackbox-Prozedur führt Reihenfolge und Vorbedingungen vollständig auf: HDD-Verzeichnisse erzeugen, Runtime-Material erzeugen, Compose starten, dann Gesundheits- und Lasttest. Kein unerklärter manueller Config-Edit.
5. **Regression:** Alle bisherigen #217-Anforderungen bleiben verpflichtend; der statische Test muss den falschen bisherigen Pfad `pi/compose/synapse-poc/homeserver.yaml` explizit als nicht zulässig erkennen.

Vor dem Commit muss der Vekling anhand der primären Synapse-Dokumentation validieren, dass der gewählte Key-Generierungsbefehl und die referenzierten Konfigurationsoptionen für die gepinnte Synapse-Image-Linie unterstützt werden.

## Retry 3: Verbindlicher Bootstrap-Befehl

Der dritte Retry ersetzt die implizite Key-Autoerzeugung durch diese dokumentierte, vor dem Compose-Start auszufuehrende Bootstrap-Prozedur. Grundlage: Synapse-Installationsdokumentation, Abschnitt Configuration Generation.

1. Der Plan muss als eigenen Schritt vor `docker compose up` genau diesen Befehl mit dem gepinnten Synapse-Image dokumentieren (die Image-Referenz wird aus der Compose-Datei uebernommen):

```bash
docker run --rm \
  -v <local-path-redacted>:/data \
  --entrypoint python3 <synapse-image-pinned-by-digest> \
  -m synapse.app.homeserver \
  --server-name synapse-poc.local \
  --config-path /data/bootstrap.yaml \
  --generate-config \
  --report-stats=no
rm -f <local-path-redacted>
```

2. Dieser Befehl erzeugt notwendiges lokales Runtime-Material im HDD-Datenpfad, ohne die readonly gemountete versionierte `homeserver.yaml` zu ueberschreiben; die temporaere Bootstrap-Konfiguration wird danach entfernt. Der Plan darf die Key-Erzeugung nicht mehr als implizite Nebenwirkung von `docker compose up` darstellen.
3. Die statischen Tests lesen den Plan und pruefen: `--generate-config`, `--config-path /data/bootstrap.yaml`, `--server-name synapse-poc.local`, `--report-stats=no`, den gepinnten Image-Digest, und die anschliessende Entfernung von `bootstrap.yaml`.
4. Die Blackbox-Reihenfolge lautet zwingend: HDD-Verzeichnisse -> Bootstrap -> Compose-Start -> Health -> Messungen.
5. Vor Commit gegen die primaere Synapse-Installationsdokumentation pruefen, dass der Befehl genau deren CLI-Form entspricht.
