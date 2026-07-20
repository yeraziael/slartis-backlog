# TESTING.md — GH-59 Audiobookshelf Reverse Proxy und TLS

## CI Evidence

Gitea Actions (Run #613): ✅ success

```
Jobs: lint (success), test-unit (success), report (success)
  - check-links:         PASS
  - check-compose:       PASS (17 files valid)
  - check-git-diff:      PASS
  - scan-secrets:        PASS
  - check-scripts:       PASS
  - ci-generator:        PASS
  - audiobookshelf-proxy: PASS (27 assertions)
```

## Local Validation

### docker compose config (effective state after both PRs)
```
$ docker-compose -f pi/compose/audiobookshelf.yml config | grep -E "VIRTUAL_PORT|expose|VIRTUAL_HOST|LETSENCRYPT"
      VIRTUAL_HOST: audiobookshelf.hl.maier.wtf
      VIRTUAL_PORT: '80'
      LETSENCRYPT_HOST: audiobookshelf.hl.maier.wtf
      LETSENCRYPT_EMAIL: webmaster@maier.wtf
    expose:
    - '80'
```

### Contract test output (27 PASS, 0 FAIL)
```
$ bash pi/tests/test_audiobookshelf_proxy.sh | grep -E "PASS|FAIL"
PASS: stack defines only Audiobookshelf
PASS: Audiobookshelf image is pinned by immutable digest
PASS: Audiobookshelf publishes no host port
PASS: Audiobookshelf exposes only internal port 80
PASS: Audiobookshelf proxy env: VIRTUAL_HOST=audiobookshelf.hl.maier.wtf
PASS: Audiobookshelf proxy env: VIRTUAL_PORT=80
PASS: Audiobookshelf joins frontproxy_default network
PASS: Audiobookshelf joins audiobookshelf_internal network
PASS: network declarations are exact
PASS: vhost.d sets client_max_body_size for large uploads
PASS: vhost.d forwards WebSocket Upgrade header
PASS: vhost.d forwards WebSocket Connection header
... (27 PASS total)
```

## Blackbox Procedure (post-deployment)

### HTTP → HTTPS Redirect
```
curl -s -o /dev/null -w "%{http_code}" http://audiobookshelf.hl.maier.wtf/
# Expected: 301/302 (redirect via frontproxy/acme-companion)
```

### HTTPS
```
curl -s -o /dev/null -w "%{http_code}" https://audiobookshelf.hl.maier.wtf/
# Expected: 200
```

### Certificate
```
openssl s_client -connect audiobookshelf.hl.maier.wtf:443 \
  -servername audiobookshelf.hl.maier.wtf 2>/dev/null \
  | openssl x509 -noout -subject -ext subjectAltName
# Subject: CN=audiobookshelf.hl.maier.wtf
# SAN: audiobookshelf.hl.maier.wtf
```

### WebSocket
```
# vhost.d forwards these headers:
#   proxy_set_header Upgrade $http_upgrade;
#   proxy_set_header Connection $connection_upgrade;
```
