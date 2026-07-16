# Tests

- `docker compose config` ist fehlerfrei.
- Das produktive Image ist auf Digest, Tag oder Commit gepinnt und fuer die Zielarchitektur verfuegbar.
- Container startet nach Host-Neustart ohne manuelle Eingriffe.
- Healthcheck erkennt Startfehler und Upstream-Ausfaelle sinnvoll.
- Port 8317 ist nur aus dem vorgesehenen internen Netz erreichbar; Management- und Callback-Ports sind nicht dauerhaft extern offen.
- Requests ohne oder mit falschem Client-Key werden abgewiesen.
- Zwei getrennte Client-Keys koennen unabhaengig widerrufen werden.
- OpenCode kann Modellliste, nicht-streamende und streamende Anfrage ueber den Gateway ausfuehren.
- Providerfehler, Quotenende und Credential-Ausfall fuehren nicht zur Offenlegung anderer Credentials.
- Logs und Fehlerausgaben enthalten keine API-Keys, OAuth-Tokens, Authorization-Header, Prompts oder Antworten.
- Backup und Restore stellen Konfiguration und Auth-Zustand auf einer Testinstanz wieder her.
- Update und Rollback werden mit gepinnten Versionen getestet.
- Ressourcentest erfasst Idle-RAM, Last-RAM, CPU und Plattenwachstum auf dem Zielhost.