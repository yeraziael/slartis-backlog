# Contract

- Implementiere eine persistente Media-Jobqueue mit mindestens Einzel-Download, Abo-Scan, Import, Audit, Move und Library-Scan.
- Manuelle Jobs haben Vorrang vor Abo-Jobs.
- Strukturveraendernde Jobs fuer denselben Zielbereich werden serialisiert; reine Leser greifen direkt auf Mounts zu.
- Nach Abschluss einer Schreibqueue wird mit Debounce genau ein gezielter Scan je betroffener Bibliothek erzeugt, nicht ein Scan pro Datei.
- Unterstuetze Retry, Dead-Letter, Abbruch, Fortschritt, konfigurierbare Parallelitaet und Historie.
- Lydia unterstuetzt sinngemaess `/download <url>`, `/subscribe <url>`, `/subscriptions`, Pause/Fortsetzen/Entfernen sowie `/media-jobs` und Jobdetails.
- Lydia validiert URL und Quellentyp, zeigt eine sichere Zusammenfassung und uebergibt nur strukturierte Jobs an Eddie.
- Abo-Scans bleiben still. Benachrichtigungen erfolgen bei echten neuen Treffern, relevanten Erfolgen und Fehlern.
- Laufende, wartende, fehlgeschlagene und abgeschlossene Jobzahlen sind abrufbar.
