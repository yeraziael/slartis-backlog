# Milestone Contract

> **STATUS (2026-07-20): SUPERSEDED/COMPLETED.** OIDC ist ohne Fork über den
> upstream Generic-OAuth-Provider (in v4.0.6 enthalten) als `app.db`-Konfiguration
> live. Dokumentiert in `Homelab/Architecture` `docs/keycloak-service-sso.md`
> (Gitea PR #74). Issue #56 geschlossen. Kein Fork-Code nötig.



- Nutze OIDC Authorization Code Flow mit PKCE, sofern CWA und Provider dies unterstuetzen.
- Discovery-URL, Client-ID, Secret und Session-Policy sind konfigurierbar.
- Die Identitaetszuordnung nutzt stabilen subject claim; E-Mail allein ist nicht primaerer Schluessel.
- Admin-Zugriff wird explizit ueber CWA-Rollen/Claims geregelt und nicht durch blossen Login vergeben.
- Lokaler Break-Glass-Admin bleibt dokumentiert und ist nur im Ausfallfall nutzbar.
