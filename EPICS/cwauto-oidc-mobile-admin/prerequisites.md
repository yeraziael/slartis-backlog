# Voraussetzungen

- Betreiber und Ziel des bestehenden CWA-Deployments sind bekannt.
- Gitea-Organisation, Zielrepository und CI-Konventionen sind bekannt.
- Der zentrale OIDC-Provider ist vor produktiver OIDC-Konfiguration festgelegt; Issuer, Discovery-URL und Claims werden erst dann als Secrets/Konfiguration hinterlegt.
- Keine Zugangsdaten, Tokens oder produktiven Bibliotheksdaten werden in Git uebernommen.
