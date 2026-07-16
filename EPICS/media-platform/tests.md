# Epic Tests

- Medienpfade bleiben nach Host-Neustart verfuegbar.
- Jellyfin erkennt Testinhalte getrennt nach Filme, Serien und Musik.
- Audiobookshelf erkennt Testinhalte getrennt nach Hoerbuecher und Podcasts.
- Externe Apps erreichen Jellyfin und Audiobookshelf ausschliesslich per HTTPS ueber die vorhandenen Subdomains.
- ytdl-sub besitzt keinen eingehenden Port.
- Ein manueller Download wird vor einem wartenden Abo-Job ausgefuehrt.
- Mehrere Schreibjobs erzeugen nach Queue-Abschluss nur einen Scan je betroffener Bibliothek.
- Lydia kann Jobs erstellen, Status anzeigen, Abos verwalten und bei echten neuen Treffern benachrichtigen.
- Eine bestehende Mediendatei kann einzeln analysiert, umbenannt, verschoben und anschliessend korrekt indiziert werden.
