# Epic Contract

1. CLIProxyAPI wird reproduzierbar als Docker-Compose-Service betrieben.
2. Vor der Hostentscheidung werden ARM64-Kompatibilitaet, Image-Herkunft, Ressourcenbedarf und OAuth-Flows praktisch verifiziert.
3. Produktiv wird entweder ein selbst gebautes, auf Commit oder Release gepinntes Image oder ein verifiziertes Multi-Arch-Upstream-Image verwendet; kein unkontrolliertes `latest` mit `pull_policy: always`.
4. Der API-Port ist ausschliesslich im internen Homelab-Netz erreichbar. Es gibt initial keine oeffentliche Subdomain und keine Portweiterleitung am Router.
5. Die Management API bleibt deaktiviert oder auf localhost beziehungsweise ein separates Admin-Netz beschraenkt. Das Control Panel darf keine ungeprueften Assets automatisch nachladen.
6. API-Schluessel, OAuth-Tokens und Auth-Dateien liegen ausserhalb des Git-Repositories in der bestehenden Secret-Verwaltung beziehungsweise in restriktiv berechtigten persistenten Volumes.
7. Clients erhalten getrennte Gateway-API-Keys. Schluesselrotation und Widerruf sind dokumentiert.
8. Provider werden einzeln freigeschaltet. Vor Aktivierung wird die Vereinbarkeit des jeweiligen Authentifizierungswegs mit Providerbedingungen und dem vorgesehenen Tarif geprueft.
9. Funktionen zum Cloaking, Identity Confusion, Prompt-Ersatz oder zur Umgehung von Quoten bleiben standardmaessig deaktiviert.
10. Logs enthalten keine Prompts, Antworten, Tokens oder Secrets. Aufbewahrung und Groessenlimit sind konfiguriert.
11. Healthcheck, Backup, Restore, Update, Rollback und kontrollierter Credential-Refresh sind dokumentiert und getestet.
12. OpenCode wird als erster Client integriert; Slarti und Lydia folgen erst nach bestandenem Pilotbetrieb.