# Tests

- Anmeldung mit Testnutzer funktioniert ueber den OIDC-Provider.
- 24-Stunden-IdP-Sitzung verursacht keinen erneuten Passwortdialog beim erneuten CWA-Zugriff.
- Logout, abgelaufene Sitzung und widerrufene Sitzung verhalten sich korrekt.
- Nicht-Admin kann keine Admin-Funktionen aufrufen.
- Fehlende oder manipulierte Claims werden abgelehnt.
