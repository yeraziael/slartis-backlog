# Voraussetzungen

- Docker Engine und Compose auf dem Zielhost.
- Internes Docker-Netz beziehungsweise eindeutig begrenztes Host-Netz fuer OpenCode und Agenten.
- Entscheidung, ob der Pi 5 oder der Rechenknecht Zielhost wird.
- Verifizierte ARM64-Unterstuetzung des Images oder reproduzierbarer ARM64-Eigenbau.
- Bestehende Secret-Verwaltung fuer API-Keys und OAuth-Dateien.
- Mindestens ein erlaubter Providerzugang fuer den Pilotbetrieb.
- Dokumentierte OpenCode-Konfiguration fuer einen OpenAI-kompatiblen Base-URL-Endpunkt.
- Backupziel fuer Konfiguration und verschluesselte Auth-Daten.

Blocker:

- Ungeklaerte Vereinbarkeit eines providerbezogenen OAuth- oder Subscription-Zugangs mit dessen Nutzungsbedingungen.
- Fehlende ARM64-Unterstuetzung oder nicht vertretbarer Ressourcenverbrauch auf dem Pi 5.
- Notwendigkeit einer oeffentlichen Erreichbarkeit fuer den normalen API-Betrieb. OAuth-Callback-Ports duerfen nur temporaer und kontrolliert genutzt werden.