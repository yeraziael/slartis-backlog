# Tests

- API-Inventar ist gegen den tatsaechlich verwendeten CWA-Commit nachvollziehbar.
- Nicht authentifizierte und nicht berechtigte Aufrufe werden abgewiesen.
- Gueltige Lesezugriffe funktionieren nur im erlaubten Umfang.
- Schreibende Endpunkte sind explizit autorisiert, idempotent oder mit klarer Duplikatbehandlung versehen.
- Fehlerantworten sind stabil und geben keine internen Details preis.
