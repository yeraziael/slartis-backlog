---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#144
state: closed
updated_at: 2026-07-14T00:32:27+02:00
is_epic: false
labels:
  - "done"
publication: sanitized
---

# 143 – CI/CD: Gitea Actions Runner + Secrets + erster Durchlauf

## Kontext

Issue #142 ist abgeschlossen: `ci-manifest.yaml`, Generator, Pipeline-Workflow, Docker-Testsystem liegen auf Branch `142/ci-manifest` in `lydia/home-repo`.

Bevor die Pipeline läuft, fehlen:

## 1. act_runner installieren

- [ ] act_runner auf **rechenknecht** (x86_64, Docker) installieren
- [ ] Runner bei Gitea registrieren (Token via `gitea admin actions generate-runner-token`)
- [ ] Runner als systemd-Service oder Docker-Container starten
- [ ] Verbindung prüfen: Runner erscheint in `GET /api/v1/admin/runners`

**Hinweise:**
- Gitea 1.26.4 auf Pi5 – Actions ist enabled (API antwortet)
- act_runner benötigt Docker-Socket-Zugriff (für Job-Container)
- Empfehlung: Runner per `docker compose` auf rechenknecht, registriert gegen `<internal-gitea-reference>

## 2. Secrets in Gitea hinterlegen

- [ ] `TELEGRAM_SLARTI_TOKEN` (aus `<credential-path-redacted>`)
- [ ] `TELEGRAM_LYDIA_TOKEN` (aus `<credential-path-redacted>` – Lydia-Token! → benötigt Erlaubnis)
- [ ] `SIGNAL_NUMBER` (aus `runtime/messenger/channels.json`)

## 3. Branch mergen & Pipeline-Test

- [ ] Branch `142/ci-manifest` in `main` mergen (nach Freigabe)
- [ ] Commit auf main triggert `feature/*`-Pipeline (lint + test-unit)
- [ ] Pipeline-Status in Gitea prüfen
- [ ] Bei Erfolg: develop-Branch anlegen, Pipeline für integration-test beobachten

## Akzeptanzkriterien

- [ ] `make ci` läuft lokal grün
- [ ] Gitea Actions zeigt grünen Haken bei Push auf feature-Branch
- [ ] Secrets sind hinterlegt, Integration-Tests laufen durch
- [ ] Deploy-Schritt auf main ist vorhanden (manuelle Freigabe)

## Verweis

- Parent: #142
- Repo: lydia/home-repo
- Branch: 142/ci-manifest
