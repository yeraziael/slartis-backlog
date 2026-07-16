---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#102
state: closed
updated_at: 2026-07-03T15:21:43+02:00
is_epic: false
labels:
  - "Aufgaben"
publication: sanitized
---

# Tests fur alle offenen Issues

**Meta:** Test-Suiten fur alle offenen Issues

Jeder Issue bekommt eine eigene Test-Suite (oder existierende wird erweitert), bevor Implementierung beginnt.

**Regel:** Tests First - keine Implementierung ohne vorherige Tests. Neue Tests mussen grun sein vor Merge.

## Test-Checkliste

- [ ] #12: Konzept: Opencode-Agent zur Analyse von Paperless-ngx auf Erstattungsstatus
- [x] #13: ✅ (done: 104 tests, PR #220) Lydia - Execution Layer Agent Implementation
- [ ] #15: Messenger Channels & Policy
- [x] #16: ✅ (Epic closed) Avatar Tooling
- [x] #27: ✅ (Closed) messenger_michael.sh — OpenCodeAgent Fork
- [ ] #5: 🌸 Lily Bloom – Agent für lokale Kurzfilm-Produktion (Backlog)
- [ ] #6: Lydia PDF-Formular-Assistent via Telegram-Bot (Plugin: pdf-form-filler)
- [ ] #7: Avatarbilder für alle Orgas und Repos
- [ ] #89: Lydia-Tutor-Skill
- [ ] #91: MS5: Full Platform
- [ ] #92: MS6: Self-Improving AI
- [ ] #93: MS7: Cognitive Digital Twin
- [ ] #94: MS4: Dashboard & Analytics
- [ ] #95: MS2: Learning Engine
- [ ] #96: MS3: Memory & Strategy
- [ ] #9: Paperless-ngx Fork: Automatische Entschlüsselung verschlüsselter Dokumente beim Import


## Aufgelöst
Aufgegliedert in 13 Einzel-Test-Issues (#108–#120), die jeweils als Blocker für das zugehörige Implementierungs-Issue gesetzt sind.

| Impl-Issue | Test-Issue |
|---|---|
| #12 | #108 -> Tests: #12 |
| #15 | #109 -> Tests: #15 |
| #5 | #110 -> Tests: #5 |
| #6 | #111 -> Tests: #6 |
| #7 | #112 -> Tests: #7 |
| #89 | #114 -> Tests: #89 |
| #9 | #113 -> Tests: #9 |
| #91 | #115 -> Tests: #91 |
| #92 | #116 -> Tests: #92 |
| #93 | #117 -> Tests: #93 |
| #94 | #118 -> Tests: #94 |
| #95 | #119 -> Tests: #95 |
| #96 | #120 -> Tests: #96 |
