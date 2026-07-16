# Milestone Contract

- Beide Dienste laufen als Compose-Services.
- Nur notwendige Bibliothekspfade werden gemountet.
- Keine direkten Host-Ports werden nach aussen freigegeben.
- `VIRTUAL_HOST`, `LETSENCRYPT_HOST`, `LETSENCRYPT_EMAIL` und der interne Zielport sind korrekt gesetzt.
- Konfiguration und Metadaten liegen auf persistentem SSD-Storage; Medien liegen auf dem QNAP.
