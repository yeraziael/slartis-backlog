# Contract

- Betreibe Jellyfin intern auf Port 8096 und Audiobookshelf auf seinem internen Standardport.
- Beide Container treten dem bestehenden Proxy-Netzwerk bei.
- Setze die vorhandenen Proxy-/ACME-Variablen, insbesondere `VIRTUAL_HOST`, `LETSENCRYPT_HOST` und `LETSENCRYPT_EMAIL`.
- Keine direkten externen Host-Portfreigaben.
- Jellyfin-Bibliotheken getrennt fuer `movies`, `series`, `music` und optional `youtube`.
- Audiobookshelf-Bibliotheken getrennt fuer `audiobooks` und `podcasts`; native Podcast-RSS-Funktionen verwenden.
- Medien moeglichst read-only mounten. Konfiguration, Datenbanken, Cache und Metadaten persistent auf SSD speichern.
- Gezielte Bibliotheks-Scans fuer Eddie bereitstellen.
- Hardware-Transcoding nur nach Test aktivieren.
- Backup und Restore der Dienstkonfiguration implementieren.
