# Contract

- Implementiere stabile QNAP-Mounts mit festen Host-Mountpoints, Wiederverbindung und eindeutigem Fehlerverhalten.
- Verhindere, dass Container bei nicht erreichbarem NAS gegen leere lokale Ersatzverzeichnisse starten.
- Erstelle mindestens `media/movies`, `media/series`, `media/music`, `media/audiobooks`, `media/podcasts`, `media/youtube`, `media/incoming` und `media/work`.
- Jeder Medientyp muss getrennt mount- und scannbar sein.
- Paperless, Gitea und Matrix bleiben auf SSD; nur Backups gehen auf das QNAP.
- Leser greifen direkt zu. Umbenennen, Verschieben und Loeschen erfolgen als koordinierte Jobs.
- Staging-Dateien werden erst nach Validierung atomar in Zielpfade ueberfuehrt.
- Dokumentiere UID/GID, Ownership, minimale Rechte und Ausfallbetrieb.
