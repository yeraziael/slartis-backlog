# Epic Contract

> **STATUS (2026-07-20): DISCARDED.** Das Epic wird verworfen. CWAuto-OIDC ist
> ohne Fork umsetzbar (upstream Generic-OAuth-Provider, seit v4.0.6 vorhanden)
> und als Konfiguration in `app.db` live. Die Anbindung ist in
> `Homelab/Architecture` `docs/keycloak-service-sso.md` (Gitea PR #74)
> dokumentiert. Issues #73, #56, #55 sind geschlossen. Fork/Mirror/MAINTENANCE
> (M01) sowie Mobile-Admin-Fixes (M03) und REST-API-Erweiterung (M04) entfallen.
> Künftige Anbindungen erfolgen direkt über das Keycloak-SSO-Runbook.

1. Ein nachvollziehbarer, nicht-destruktiver Mirror des CWA-Upstreams existiert in Gitea.
2. Der Homelab-Fork bewahrt Upstream-Herkunft, Lizenz, Version und Patch-Historie.
3. Der Fork nutzt vorhandene CWA-OIDC-Funktionen, sofern sie die Anforderungen erfuellen; nur fehlende oder fehlerhafte Teile werden erweitert.
4. OIDC ist fuer CWA via Konfiguration aktivierbar, ohne Secrets im Repository.
5. Die mobile Administration ist fuer definierte, reproduzierte Fehler auf aktuellen iOS-Safari-Ansichten repariert.
6. Der vorhandene REST-API-Funktionsumfang ist analysiert; fehlende, begruendete Funktionen werden als versionierte und abgesicherte API im Fork ergaenzt.
7. Upstream-Updates bleiben nachvollziehbar integrierbar.
