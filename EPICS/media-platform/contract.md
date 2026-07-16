# Epic Contract

Lieferumfang:

1. QNAP-Medienfreigaben werden stabil und mit minimalen Rechten eingebunden.
2. Eine zukunftsfeste Top-Level-Struktur nach Medientyp wird erstellt: `movies`, `series`, `music`, `audiobooks`, `podcasts`, `youtube` und Arbeitsbereiche fuer eingehende beziehungsweise temporaere Dateien.
3. Jellyfin und Audiobookshelf werden per Docker Compose betrieben und nur ueber das bestehende Reverse-Proxy-Netz nach aussen veroeffentlicht.
4. ytdl-sub bleibt ohne eingehenden Port und verarbeitet Einzel- sowie Abo-Downloads.
5. Eddie priorisiert manuelle Jobs vor Abo-Jobs, serialisiert strukturveraendernde Schreibzugriffe und triggert genau einen gezielten Scan pro abgeschlossenem Batch.
6. Lydia nimmt Links und Abo-Befehle entgegen, erzeugt strukturierte Eddie-Jobs und meldet Status, neue Treffer und Fehler.
7. Bestehende Medien werden schrittweise importiert; pro Migrationseinheit werden Qualitaet, Benennung und Zielpfad geprueft.
8. Es werden ausschliesslich rechtmaessige Quellen verarbeitet; keine Darknet- oder offensichtlich illegalen Downloadquellen.
