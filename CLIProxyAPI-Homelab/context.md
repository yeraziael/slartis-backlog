# CLIProxyAPI Homelab

`router-for-me/CLIProxyAPI` soll als zentraler, OpenAI-/Claude-/Gemini-kompatibler API-Gateway im Homelab betrieben werden. Der Dienst vereinheitlicht den Zugriff von OpenCode, Slarti, Lydia und spaeteren Workern auf mehrere Modellanbieter und mehrere Accounts.

Der Upstream liefert bereits Dockerfile und Docker-Compose-Konfiguration. Standardmaessig lauscht der API-Dienst auf Port 8317; weitere veroeffentlichte Ports dienen providerbezogenen OAuth-Callbacks. Konfiguration, Authentifizierungsdaten und Logs werden persistent gemountet.

Die Einfuehrung ist sinnvoll, wenn der Dienst als internes Infrastruktur-Gateway behandelt wird. Er darf initial nicht aus dem Internet erreichbar sein. OAuth-Tokens und API-Schluessel sind hochkritische Secrets. Providerfunktionen, die Client-Identitaeten verschleiern, Prompts ersetzen oder Nutzungsbeschraenkungen umgehen koennten, werden nicht ungeprueft aktiviert.

Upstream: https://github.com/router-for-me/CLIProxyAPI
Lizenz: MIT
Zielhost: Raspberry Pi 5, sofern ARM64-Build, Laufzeit und Speicherbedarf im Spike bestaetigt werden; andernfalls Rechenknecht.