# Media Platform

Das Homelab soll eine selbst gehostete Medienplattform fuer Filme, Serien, Musik, Hoerbuecher, Podcasts und legale Online-Quellen erhalten.

Jellyfin dient fuer Video und Musik. Audiobookshelf dient fuer Hoerbuecher und Podcasts. ytdl-sub uebernimmt wiederkehrende und einzelne Downloads. Das QNAP stellt den persistenten Medienbestand bereit. Eddie koordiniert schreibende Jobs und gezielte Bibliotheks-Scans. Lydia stellt die Messenger-Oberflaeche bereit.

Die bestehende Mediensammlung wird nicht als Big-Bang migriert. Eine leere, Jellyfin-optimierte Zielstruktur wird angelegt; bestehende Dateien werden danach inkrementell, bevorzugt einzeln, geprueft und verschoben.
