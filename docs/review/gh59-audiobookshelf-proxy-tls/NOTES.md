# NOTES.md — GH-59 Audiobookshelf Reverse Proxy und TLS

## Scope

- **VIRTUAL_HOST**: `audiobookshelf.hl.maier.wtf` (aus GH-57 Architektur)
- **VIRTUAL_PORT**: `80` (audiobookshelf-Container lauscht intern auf Port 80)
- **ACME**: Let's Encrypt via acme-companion, E-Mail `webmaster@maier.wtf`
- **Netzwerk**: `frontproxy_default` (external) + `audiobookshelf_internal` (internal)
- **vhost.d**: `client_max_body_size 0` (unlimited uploads), WebSocket-Header
- **Kein Host-Port**: Nur `expose: ["80"]` — keine `ports:`-Mapping
- **Healthcheck**: prüft `http://localhost:80/` (Status 200)

## Korrektur (PR #70)

PR #68 setzte `VIRTUAL_PORT: "13378"`, aber PR #65 (intermediate merge)
korrigierte den Container-Expose-Port auf `80`. PR #70 korrigiert `VIRTUAL_PORT`
auf `"80"` und den zugehörigen Test.

Ohne Fix würde nginx-proxy an Port 13378 routen, wo kein Prozess lauscht →
502 Bad Gateway.

## Risiken

- Gering. Nur versionierte Compose- und Konfigurationsdateien.
- Keine neuen Host-Ports, keine Firewall-Änderung, keine Secrets.
- vhost.d erlaubt unlimitierte Uploads (`client_max_body_size 0`) — akzeptabel
  für privates Homelab hinter Authentifizierung.

## Excluded

- OIDC/Keycloak (GH-60)
- NAS-Medienimport (separates Issue)
- Rollen und Berechtigungen

## Verifikation (lokal, vor Merge)

- `docker-compose -f pi/compose/audiobookshelf.yml config` — valid
- `bash pi/tests/test_audiobookshelf_proxy.sh` — 27 Assertions, alle PASS
- `make lint` — alle Checks PASS
- `make test` — alle Tests inkl. neuer audiobookshelf-proxy: PASS
- CI (Gitea Actions Run #613): success
