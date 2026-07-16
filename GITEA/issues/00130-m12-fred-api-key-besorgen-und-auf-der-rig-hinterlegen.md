---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#130
state: open
updated_at: 2026-07-14T00:35:49+02:00
is_epic: false
labels:
  - "Aufgaben"
  - "clarifying"
publication: sanitized
---

# M12: FRED API-Key besorgen und auf der Rig hinterlegen

## Aufgabe
FRED (Federal Reserve Economic Data) API-Key für den Makrodaten-Import in M12.

## Was wird benötigt
- Registrierung unter https://fred.stlouisfed.org/docs/api/api_key.html
- Key ablegen in `<credential-path-redacted>` auf der Rig
- Berechtigung für Ægir zum Lesen

## Warum
M12 importiert Makrodaten (CPI, Zinssätze, Arbeitsmarkt) via FRED API. Der Alpha Vantage Key (`<credential-path-redacted>`) existiert bereits auf der Rig.

## Assignee
@slarti — bitte FRED-Key besorgen und ablegen
