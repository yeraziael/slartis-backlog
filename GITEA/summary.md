# Gitea Backlog Summary

Stand: 2026-07-17

## Snapshot

- Quelle ist `slarti/backlog` in Gitea.
- Der Index enthaelt 235 oeffentlich bereinigte Issue-Records bis Issue `#247`.
- Diese Aktualisierung uebernimmt die geaenderten Records `#185`, `#186`,
  `#187` und `#233`; alle vier sind inzwischen geschlossen.
- Interne URLs, Transportdaten, Attachments, lokale Pfade und Zugangsdaten sind
  nicht enthalten.

## Abgeschlossene Lieferungen

- `#185`: `homelab-release/v1` Contract und Guideline, umgesetzt in
  `lydia/home-repo#369`, Merge-Commit `beb87d2`.
- `#186`: gehaertete Eddie Build-Inputs, ARM64-Imagevertrag und
  Versionsmetadaten, umgesetzt in `lydia/home-repo#372`, Merge-Commit
  `860fed5`.
- `#187`: deterministischer Eddie Release-Packager mit exakter Asset-Allowlist,
  Manifest, `SHA256SUMS`, Fresh-Copy-Verifikation und isoliertem Image-Smoke,
  umgesetzt in `lydia/home-repo#373` und Follow-up `#374`. Finale
  Merge-Commits: `c5ae96a` und `a9e6a99`.
- `#231`: Matrix-Approvals an das Execution Gate angebunden,
  `lydia/home-repo#370`, Merge-Commit `72318ec`.
- `#233`: kanal- und replay-sicherer Bridge-Loop-Guard,
  `lydia/home-repo#371`, Merge-Commit `6b1910f`.
- `#239`: Matrix Betriebs-, Notfall- und Rollback-Handbuch,
  `Homelab/Architecture#26`.

## Verifikation

- Die finale generierte CI fuer Eddie `#187` war auf `main` erfolgreich.
- Der finale Eddie-Lauf baute und startete das ARM64-Image auch auf einem
  amd64-Runner ueber gepinnte Binfmt-Emulation.
- Paketgenerierung, kopierte Paketverifikation, Version/Commit-Pruefung und
  isolierte Image-Smokes liefen erfolgreich.
- Es wurde kein Release oder Image publiziert und kein Deployment, Restart,
  Credential- oder Produktionswechsel ausgefuehrt.

## Naechste Kette

- Naechster Release-Vorgaenger ist `#188`: Release Notes und Changelog Policy.
- Danach folgt `#189`, sobald `#186`, `#187` und `#188` abgeschlossen sind.
- Parallel fuehren `#190` und `#192` zu `#191`.
- `#241` benoetigt `#189` und `#191`; erst danach kann das blockierte `#237`
  fortgesetzt werden.
- Produktive Matrix-Aktionen wie DNS, Firewall, Zertifikate, Secrets,
  Deployment, Restore-Nachweis und Operatorabnahme bleiben getrennte
  Operatoraufgaben.
