# Milestone Contract

> **STATUS (2026-07-20): SUPERSEDED / PARTIALLY VERIFIED.** OIDC ist ohne Fork
> über den upstream Generic-OAuth-Provider (in v4.0.6 enthalten) als
> `app.db`-Konfiguration live und im Login-UI verifiziert. Dokumentiert in
> `Homelab/Architecture` `docs/keycloak-service-sso.md` (Gitea PR #74). Issue
> #56 geschlossen. Die im #56 geforderte negative Abnahmeevidenz (negatives
> Admin-Mapping, Rollenentzug, Neustart, Break-Glass, dokumentierte Grenzen)
> ist in der Live-Config angelegt, aber nicht als formaler Testbericht
> hinterlegt. Kein Fork-Code nötig.



- Nutze OIDC Authorization Code Flow mit PKCE, sofern CWA und Provider dies unterstuetzen.
- Discovery-URL, Client-ID, Secret und Session-Policy sind konfigurierbar.
- Die Identitaetszuordnung nutzt stabilen subject claim; E-Mail allein ist nicht primaerer Schluessel.
- Admin-Zugriff wird explizit ueber CWA-Rollen/Claims geregelt und nicht durch blossen Login vergeben.
- Lokaler Break-Glass-Admin bleibt dokumentiert und ist nur im Ausfallfall nutzbar.
