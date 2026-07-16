# Contract

- Liefere vor Codeaenderungen API-INVENTORY.md mit Endpunkten, Authentifizierung, Autorisierung, Versionsstand, Stabilitaet und belegten Luecken.
- Definiere anschliessend nur die minimal benoetigten Use Cases. Startumfang fuer eine neue/erweiterte API: bibliothekssicheres Suchen und Listen, Buchdetail/Metadaten sowie klar abgegrenzter Status von Import-/Automationsjobs, sofern CWA diese Daten besitzt.
- Schreibende Aktionen, Datei-Upload, Loeschen, Benutzer-/Rechteverwaltung und direkte Bibliotheksmanipulation gehoeren nicht in den ersten API-Umfang, ausser ein spaeterer Auftrag definiert sie explizit.
- Neue Endpunkte verwenden einen Version-Prefix, stabile JSON-Schemata, Pagination wo Listen wachsen koennen und konsistente Fehlercodes.
- Nutze OIDC Bearer-Tokens oder eine gleichwertig sichere, zentral widerrufbare API-Authentifizierung. Pruefe serverseitig Audience, Ablauf, Issuer und Rollen/Scopes.
- Dokumentiere Endpunkte maschinenlesbar mit OpenAPI, sofern neue Endpunkte entstehen.
