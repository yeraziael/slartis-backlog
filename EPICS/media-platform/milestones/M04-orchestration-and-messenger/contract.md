# Milestone Contract

- Manuelle Jobs haben Vorrang vor Abo-Jobs.
- Strukturveraendernde Schreibjobs werden serialisiert.
- Nach abgeschlossenem Batch wird je betroffener Bibliothek genau ein Scan ausgeloest, mit Debounce.
- Lydia unterstuetzt Einzel-Download, Abo-Verwaltung, Queue-Status, Historie und Benachrichtigungen.
- Abo-Scans bleiben still; Meldungen erfolgen nur bei neuen Treffern, Erfolg mit relevantem Ereignis oder Fehler.
