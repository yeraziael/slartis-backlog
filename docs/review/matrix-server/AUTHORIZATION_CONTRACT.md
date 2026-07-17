# Inbound Authorization — End-to-End Contract

## Design Principle

Der `MatrixInboundAdapter` (inbound.py) ist autori­sierungs­agnostisch.
Seine einzige Aufgabe: Matrix-Sync-Events in kanalneutrale Lydia-Envelopes
konvertieren. Die Authorization ist auf **vier nachgelagerte Schichten**
verteilt, von denen jede fail-closed arbeitet:

### Matrix-Spezifisch: Sender-ID als Policy-Key

Für Telegram und Signal wird `target.id` (Chat-ID / Gruppen-ID) als
Policy-Key verwendet. Für Matrix wäre dies die `room_id` — das ist
semantisch falsch, weil die Authorization pro **Matrix-User** erfolgen
muss, nicht pro Raum.

Daher führt der Processor (`processor.sh`) eine kanalabhängige Auflösung
durch:

- **Telegram/Signal:** `policy_chat_id = target.id` (Chat-ID oder Gruppen-ID),
  ggf. Signal-UUID → canonical chat_id aufgelöst
- **Matrix:** `policy_chat_id = sender.id` (Matrix-User-ID wie
  `@admin:matrix.example.org`)

Damit wird die Matrix-User-ID als Policy-Key behandelt — genau wie ein
Telegram-Chat-ID oder eine Signal-UUID. Die `room_id` (target.id) bleibt
für das Response-Routing erhalten.

**Effekt:** Ein Matrix-User wird in der Policy wie ein Telegram-User
behandelt: `policy_get_role("@admin:matrix.example.org")` gibt dessen
Rolle zurück. Die Auto-Registrierung legt den Matrix-User (nicht den
Raum) als pending an. Der Admin kann den User via `/accept @admin...`
freischalten, und der User ist dann in allen Matrix-Räumen authorisiert.

```
Matrix-Event
  │
  ▼
[1] InboundAdapter (inbound.py):
    ├── Filtert: nur m.room.message + m.text → Envelope
    ├── Ignoriert: andere Event-Typen und MsgTypes (audit trail)
    └── KEINE Autorisierung — reine Format-Konversion
  │
  ▼
[2] Processor (processor.sh):
    ├── policy_get_role() → unknown/known/authorized
    ├── unknown + nicht Admin → auto-registrieren → DROP
    ├── !routing_has_policy(chat_id, admin) → SILENT DROP
    └── Bot-scope (/grill nur slarti, /generate nur lydia)
  │
  ▼
[3] Router (routing.sh):
    ├── @-mention Allowlist (ROUTING_AT_MAP)
    ├── Per-user @-Restriktionen (ROUTING_USER_RESTRICTIONS)
    └── Issue-Policy-Gate (nur bekannte User mit Default)
  │
  ▼
[4] Execution Gates:
    ├── execution_gate.sh: allow_execute(BLOCK|REVIEW|ESCALATE)
    ├── safe_execute.sh: Pattern-basierte Command-Blocklist
    ├── policy_guard.sh: Handler-Pfad-Restriktionen
    ├── gate/approvals.py: Principal-Gebundene Approval-Store
    └── executor_server.py: OPS_COMMANDS-Allowlist
  │
  ▼
[5] Bridge- / Replay-Schutz (loop_guard.py):
    ├── Atomic Claims (message_id, trace_id)
    ├── Replay: selbe message_id → rejected
    ├── Repeated trace: selbe trace_id → rejected
    └── Max Bridge-Hops: 1
```

## Negative Tests

### NT1: Unknown Room → Silent Drop

Ein Event aus einem nicht-autorisierten Matrix-Raum wird vom InboundAdapter
trotzdem in ein Envelope konvertiert (inbound.py hat keine Room-Allowlist).
Der Processor (processor.sh) prüft routing_has_policy() anhand der chat_id
(bei Telegram/Signal) bzw. des resolved chat_id. Ein Raum ohne zugeordnete
Policy wird **silent dropped** — keine Antwort, kein Issue.

**Test:** processor.sh, routing_has_policy → return 1 → DROP

### NT2: Unknown Sender → Auto-Registrierung + DROP

Ein unbekannter Sender (role=unknown, nicht Admin) wird automatisch als
pending registration eingetragen. Die Nachricht wird **silent consumed**,
nicht verarbeitet. Der Admin erhält eine Telegram-Benachrichtigung über die
neue Registrierung.

**Test:** processor.sh, role=unknown + !admin → register_put + return 0

### NT3: Allowed Sender in Wrong Room → Bot-Scope Check

Ein autorisierter Sender sendet im Slarti-Bot-Raum (Matrix) den Befehl
`/generate`. Der Processor erkennt den Bot-Scope-Konflikt: `/generate` ist
nur auf Lydia verfügbar → **abgelehnt mit Fehlermeldung**.

**Test:** processor.sh dispatch, bot=slarti + cmd=/generate → "nur auf Lydia"

### NT4: Replay → LoopGuard Rejection

Eine bereits verarbeitete Event-ID wird erneut zugestellt (Sync-Reset,
Doppelzustellung). Der LoopGuard (loop_guard.py) erkennt das Replay über
message_id-Claims und lehnt ab.

**Test:** loop_guard_test: test_duplicate_claim, test_repeated_trace

### NT5: Matrix Unknown Sender → Auto-Registrierung mit Sender-ID

Ein unbekannter Matrix-User (`@unknown:matrix.example.org`) sendet eine
Nachricht. Der Processor setzt `policy_chat_id = @unknown:matrix.example.org`
(statt der room_id). Da der User nicht in der Policy ist (role=unknown),
wird er automatisch als pending registriert — mit der Matrix-User-ID als
Key. Der Admin erhält eine Notification, die den Matrix-User (nicht den
Raum) referenziert.

**Test:** NT5 in test_processor_handlers.sh

### NT6: Matrix Blocked User → Silent Drop (Catch-all)

Ein bekannter Matrix-User (`@blocked:matrix.example.org`) ohne
`routing_has_policy` sendet einen nicht-Kommando-Text. Die
`routing_has_policy`-Prüfung verwendet `policy_chat_id` (= sender.id)
und lehnt ab → silenter Drop. Kein Issue, keine Antwort.

**Test:** NT6 in test_processor_handlers.sh

### NT7: Matrix Known Sender → Command Dispatch mit Room-Response

Ein bekannter Matrix-User (`@admin:matrix.example.org`) sendet `/status`.
Der Processor dispatches das Kommando (role=authorized). Die Antwort geht
an die `room_id` (= target.id), nicht an den Sender — der User sieht die
Antwort im Matrix-Raum.

**Test:** NT7 in test_processor_handlers.sh

## Evidenz

| Schicht | Datei | Zeilen |
|---|---|---|
| Format-Konversion | runtime/matrix/inbound.py | 130 |
| Role + Policy | runtime/processor/processor.sh | dispatch_message() |
| Role-DB | runtime/processor/handlers/users.sh | policy_get_role, routing_has_policy |
| @-Allowlist | runtime/processor/handlers/routing.sh | ROUTING_AT_MAP |
| Bot-Scope | runtime/processor/processor.sh | bot-spezifische Command-Blöcke |
| Execution Gate | runtime/gate/execution_gate.sh | allow_execute() |
| Safe Execute | runtime/hardening/safe_execute.sh | validation_gate_v5 |
| Policy Guard | runtime/hardening/policy_guard.sh | register_handler_policy |
| Approvals | runtime/gate/approvals.py | create, decide |
| Ops Allowlist | runtime/processor/executor_server.py | OPS_COMMANDS |
| Replay Schutz | runtime/messaging/loop_guard.py | MemoryClaims, LoopGuard |
| Tests | runtime/tests/test_matrix_inbound.py | fail-closed tests |
| Tests | runtime/tests/test_processor_handlers.sh | dispatch, routing, policy, reply |
