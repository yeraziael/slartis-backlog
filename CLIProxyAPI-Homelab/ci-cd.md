# CI/CD

- YAML-, Compose- und Konfigurationsdateien werden statisch validiert.
- Images werden reproduzierbar gebaut, auf bekannte Schwachstellen gescannt und mit Version, Commit und Build-Datum versehen.
- Multi-Arch-Build oder ARM64-Nachweis ist verpflichtend, falls der Pi 5 Zielhost bleibt.
- Keine Secrets werden in Build-Kontext, Image-Layer, Artefakte oder Logs aufgenommen.
- Integrationstests verwenden ausschliesslich Test-Credentials und deaktivierte beziehungsweise begrenzte Providerkonten.
- Deployments erfolgen nur mit gepinnten Images und dokumentiertem Rollback-Ziel.
- Automatische Upstream-Updates sind deaktiviert; Renovate/Dependabot darf Updates nur als Review-PR vorschlagen.
- Nach Deployment laufen Netzwerk-, Auth-, Health- und Log-Leak-Smoke-Tests.
- Produktive Credentials werden niemals in CI verwendet.