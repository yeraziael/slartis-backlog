# Milestone Contract

- Ermittle aktuelle Releases, Container-Registry, Architekturen und Build-Reproduzierbarkeit.
- Baue beziehungsweise starte den Dienst auf ARM64 und erfasse Ressourcenverbrauch.
- Dokumentiere alle dauerhaft und temporaer benoetigten Ports je Provider.
- Pruefe API-, Management-, Control-Panel-, Plugin-, Debug- und Logging-Oberflaechen.
- Unterscheide offizielle API-Key-Nutzung von OAuth-/Subscription-Weiterleitung und bewerte jeden vorgesehenen Provider separat.
- Teste OpenCode gegen einen internen OpenAI-kompatiblen Endpunkt.
- Lege eine sichere Basiskonfiguration fest: remote management aus, Control-Panel-Autoupdate aus, Plugins aus, Debug/pprof aus, WebSocket-Auth an, keine Cloaking-/Identity-Confusion-Funktionen.
- Liefere Go/No-Go sowie Pi-5/Rechenknecht-Entscheidung.