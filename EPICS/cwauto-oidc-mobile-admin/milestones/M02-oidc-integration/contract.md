# Milestone Contract

- Nutze OIDC Authorization Code Flow mit PKCE, sofern CWA und Provider dies unterstuetzen.
- Discovery-URL, Client-ID, Secret und Session-Policy sind konfigurierbar.
- Die Identitaetszuordnung nutzt stabilen subject claim; E-Mail allein ist nicht primaerer Schluessel.
- Admin-Zugriff wird explizit ueber CWA-Rollen/Claims geregelt und nicht durch blossen Login vergeben.
- Lokaler Break-Glass-Admin bleibt dokumentiert und ist nur im Ausfallfall nutzbar.
