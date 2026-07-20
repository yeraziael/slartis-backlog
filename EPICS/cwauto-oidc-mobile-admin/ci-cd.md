# CI/CD

- Upstream-Quellstand und Lizenz werden vor dem Build festgehalten.
- Container-/Compose-Konfiguration wird validiert.
- Keine CI darf produktive E-Book-Bibliotheken, Datenbanken oder Secrets verwenden.
- Mobile Regressionstests verwenden Testkonto und Testbibliothek.
- API-Contract-, Authentifizierungs- und Autorisierungstests laufen isoliert.
