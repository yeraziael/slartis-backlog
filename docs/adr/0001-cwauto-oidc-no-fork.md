# CWAuto-OIDC ohne Fork/Mirror

Das CWAuto-Upstream-Mirror- und Homelab-Fork-Epic (GitHub #73, Plan PR #72) wurde
verworfen. CWAuto wird stattdessen direkt über den upstream-eigenen
Generic-OAuth/OIDC-Provider an Keycloak angebunden — als reine Konfiguration in
`app.db`, ohne Fork, ohne gespiegelten Upstream und ohne Code-Änderung.

## Status

accepted

## Context

Das Epic sah vor, einen Gitea-Mirror des CWAuto-Upstreams und einen davon
getrennten Homelab-Fork anzulegen, um Homelab-spezifische OIDC-, Mobile-Admin-
und REST-API-Erweiterungen versioniert zu pflegen. Bei der Umsetzung der
OIDC-Anbindung (Session 2026-07-19, Issue #56) zeigte sich, dass CWAuto bereits
seit Upstream-Commit `44b053b5` (2025-08-31, OIDC-Discovery-Fixes Issue #715 im
Okt 2025) einen vollwertigen Generic-OAuth/OIDC-Provider mit `metadata_url`-
Discovery und Admin-Group-Mapping enthält — also lange vor dem eingesetzten
v4.0.6. Die Anbindung benötigte ausschließlich Konfiguration (Keycloak-Client
`calibre-web-automated` + `generic`-Provider-Zeile in `app.db`), keinen
Code-Eingriff.

Gleichzeitig entfiel der ursprüngliche Anreiz für Mobile-Admin- und
REST-API-Erweiterungen im Fork: Diese sollten nur bei hinreichendem Mehrwert
angefasst werden; mit Wegfall des OIDC-Fork-Zwangs gab es keinen Anlass, den
CWAuto-Code überhaupt zu berühren.

## Considered Options

- **Fork + Mirror (ursprünglicher Plan, #73):** Maximale Kontrolle und
  versionierte Homelab-Patches, aber dauerhafter Pflegeaufwand (Rebase/Sync,
  Lizenz-/Attributionserhalt, eigene CI). Unverhältnismäßig für eine reine
  Konfigurationsanbindung.
- **Upstream Generic-OAuth direkt nutzen (gewählt):** Kein Fork, keine
  Mirror-Pflege, OIDC ist in wenigen Config-Schritten live. Nachteil: die
  CWAuto-OIDC-Config lebt in `app.db` (Container-Volume) statt in einem
  versionierten Repo; ein Upgrade muss die `app.db`-Config mitführen.
- **Dedizierter Fork nur für Mobile-Admin/REST-API:** Verworfen, da kein
  hinreichender Mehrwert gegenüber upstream besteht.

## Consequences

- Issue #73 (M01 Fork/Mirror) und die Mobile-Admin- (M03) sowie REST-API-
  Erweiterungs-Meilensteine (M04) sind entfallen.
- Issue #56 (CWAuto-OIDC) ist erledigt und live verifiziert; die Anbindung ist
  in `Homelab/Architecture` `docs/keycloak-service-sso.md` (Gitea PR #74)
  dokumentiert.
- Issue #55 (homelab-weites Keycloak-Authorization-Epic) bleibt **offen**; nur
  der CWAuto-Anteil ist hiermit abgedeckt.
- **Source of Truth für neue OIDC-Anbindungen:** das Keycloak-SSO-Runbook in
  `Homelab/Architecture` `docs/keycloak-service-sso.md`. Künftige Anbindungen
  laufen nicht mehr unter einem separaten Keycloak-Epic.
- Risiko: Produktion läuft auf `crocodilestick/calibre-web-automated:latest`
  ohne gepinnten Digest; ein Upgrade muss die `app.db`-OIDC-Config erhalten.
