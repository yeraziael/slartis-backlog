# Contract

- Betreibe ytdl-sub containerisiert, ohne eingehenden Port.
- Trenne Profile fuer Einzeljobs und wiederkehrende Kanalabos.
- Schreibe Downloads zuerst nach Staging und verhindere Duplikate ueber eindeutige IDs/Archive.
- Native Podcasts werden ueber Audiobookshelf-RSS verarbeitet, nicht ueber ytdl-sub.
- Verarbeite ausschliesslich rechtmaessige Quellen; keine Darknet- oder offensichtlich illegalen Quellen.
- Erstelle eine persistente Importqueue fuer bestehende Medien.
- Verarbeite standardmaessig genau einen Film beziehungsweise eine abgeschlossene Medieneinheit gleichzeitig.
- Erfasse Container, Video-/Audiocodec, Aufloesung, Bitrate, HDR, Kanaele und Laufzeit.
- Normalisiere Benennung auf Jellyfin-konforme Schemata wie `Titel (Jahr)`.
- Bewerte Qualitaet gegen konfigurierbare Zielprofile und markiere Neu-Rip-Kandidaten; keine automatische Neubeschaffung.
- Entferne oder archiviere die Quelle erst nach verifiziertem Ziel, Metadatencheck und erfolgreichem Index.
- Unterstuetze Pause, Fortsetzen, Retry und Historie ohne Datenverlust.
