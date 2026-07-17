# Testabdeckung

## Unit-Tests (Bash + Python)

### Architecture Repo (12 Test-Skripte, ~330 Tests)

| Test | Beschreibung | Status |
|---|---|---|
| test_synapse_compose.sh (251) | Synapse Compose-Contract: Networks, Secrets, Pre-Start Entrypoint | ✅ |
| test_synapse_poc.sh (859) | PoC-Isolation, Digests, HDD-Volumes, Bootstrap | ✅ |
| test_synapse_storage.sh (652) | Volume-Mounts, PoC-Isolation, Restore-Inputs | ✅ |
| test_coturn_compose.sh (215) | Coturn Ports, Secrets, ARM64, Digest-Pinned | ✅ |
| test_element_compose.sh (116) | Element Compose + Config-Contract | ✅ |
| test_matrix_backup.sh (247) | 5 Artefaktklassen, SHA256, Retention | ✅ |
| test_matrix_discovery.sh (79) | Federation-Mode, Well-Known, kein Federation-Port | ✅ |
| test_matrix_hardening.sh (108) | Open-Reg, Floating-Images, Host-Ports | ✅ |
| test_matrix_identity_policy.sh (375) | Identity-Model-Contract, Scope, Token-Lifecycle | ✅ |
| test_matrix_oidc.sh (113) | Keycloak-Client-Template, OIDC-Runbook | ✅ |
| test_matrix_operations.sh (77) | Runbook-Sections, Placeholder, Forbidden Secrets | ✅ |
| test_matrix_release_profile.sh (32) | Release-Profil-Contract (NEU in #241) | ✅ |

### Home-Repo (41 Test-Dateien, ~500 Tests)

**Matrix-spezifische Python-Tests (alle neu in diesem Epic):**

| Test | Beschreibung | Status |
|---|---|---|
| test_matrix_inbound.py | Event-Parsing, Message-Envelope-Mapping | ✅ |
| test_matrix_outbound.py | Outbound-Send, Reply-Mapping | ✅ |
| test_matrix_chunking.py | Message-Chunking an Wortgrenzen | ✅ |
| test_matrix_attachments.py | Attachment-Download, MIME-Validierung | ✅ |
| test_matrix_approvals.py | Approval-Flow, Execution-Gate-Binding | ✅ |
| test_matrix_room_bootstrap.py | Room-Creation, Power-Level-Setup | ✅ |
| test_matrix_state_store.py | Sync-Cursor-Persistenz, Deduplizierung | ✅ |
| test_matrix_observability.py | Health-Endpunkt, Sync-Lag-Messung | ✅ |
| test_loop_guard.py | Bridge-Loop-Erkennung, Trace-ID | ✅ |
| test_matrix_parallel_fixtures.py (NEU #238) | 20 Szenarien, 13 Contract-Tests | ✅ |
| test_ci_generator.py (erweitert #237) | Compose-Validate + Scan-Secrets-Assertions | ✅ |

**Sicherheitsrelevante Tests:**

| Test | Beschreibung | Status |
|---|---|---|
| test_messenger_secrets.sh (332) | 5 Security-Contract-Tests | ✅ |
| test_execution_approvals.py | Approval-Gate-Tests | ✅ |
| test_release_manifest.py | Manifest-Validierung | ✅ |

## Integrationstests

- messenger-test: Telegram/Signal-Adapter mit Mocks
- Matrix-Parallelbetrieb: 7-Tage-Operator-Runbook (dokumentiert, #238)

## Verbleibende Risiken

1. **Kein echter Synapse-Integrationstest in CI** — CI läuft auf ubuntu-latest
   (x86_64), Synapse-Image ist für ARM64. Ein Cross-Arch-Integrationstest
   müsste QEMU-emuliert werden oder auf dem Pi5 laufen.
2. **Kein automatischer E2E-Test über alle Kanäle** — Telegram/Signal-Mocks
   existieren, aber Matrix-E2E-Test ist nur als Operator-Runbook dokumentiert.
3. **CI-Generator-Tests prüfen nur Codegenerierung** — Nicht die tatsächliche
   CI-Ausführung auf dem Gitea-Runner.

## Manuelle Testschritte

1. Operator führt 7-Tage-Parallelbetrieb gemäß docs/matrix/parallel-operation-test.md durch
2. Tägliche Health-Checks (Matrix, Telegram, Signal)
3. Ressourcen-Messung (RAM, CPU, Disk)
4. Sync-Lag-Überwachung
5. Szenario-Tests S01–S20
6. Bei Erfolg: Primary-Channel-Declaration (#240)
