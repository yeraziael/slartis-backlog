# Voraussetzungen

- QNAP ist im Homelab-Netz erreichbar.
- Raspberry Pi beziehungsweise Docker-Host kann das QNAP dauerhaft mounten.
- Der bestehende `jwilder/nginx-proxy` mit ACME Companion ist betriebsbereit.
- Jellyfin und Audiobookshelf koennen dem bestehenden Proxy-Netzwerk beitreten.
- Eddie und Lydia besitzen definierte Job- und Messenger-Schnittstellen oder koennen entsprechend erweitert werden.
- Keine Secrets werden im Repository abgelegt.
