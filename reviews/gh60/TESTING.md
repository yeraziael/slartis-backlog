# GH-60 — Verification Matrix

Status legend:
- **VERIFIED** — checked in this session with reproducible evidence.
- **PENDING RUNTIME** — procedure defined and ready; requires the runtime
  cutover (Keycloak client creation + ABS settings application + live login),
  which is executed by the runtime operator (Lydia) per the ACP work order.
  Not executed in the planning session; **not** marked as passed.
- **N/A** — not applicable.

All evidence is redacted: no secrets, tokens, cookies, or passwords appear.

## 1. Compatibility (source/discovery) — VERIFIED

| Check | Result | Evidence |
|---|---|---|
| Native OIDC (Authorization Code) | PASS | `OidcAuthStrategy.js` present; `openid-client` Strategy |
| Confidential client + secret | PASS | `authOpenIDClientSecret` field; server-side token exchange |
| Stable binding by `sub` | PASS | `User.findUserFromOpenIdUserInfo` → `getUserByOpenIDSub`; `extraData.authOpenIDSub` persisted (`User.js:220-227,330`) |
| No auto-link by email/username | PASS | `authOpenIDMatchExistingBy` left `null` (default) → no email/username branch (`ServerSettings.js:81,145`) |
| Auto-provisioning | PASS | `authOpenIDAutoRegister` → `createUserFromOpenIdUserInfo` (`OidcAuthStrategy.js:170-185`) |
| RP-Initiated Logout | PASS | `getEndSessionUrl` uses `id_token_hint` + `post_logout_redirect_uri` (`OidcAuthStrategy.js:393-419`, `Auth.js:502`) |
| Discovery endpoint live | PASS | `GET /.well-known/openid-configuration` returns issuer `https://auth.hl.maier.wtf/realms/homelab`, `end_session_endpoint`, `jwks_uri` (curl, 2026-07-21) |
| PKCE S256 (web flow) | **GAP (not blocker)** | No `authOpenIDUsePkce` field in `ServerSettings.js`; PKCE only for mobile flow — documented in `audiobookshelf-oidc.md §4` |
| Native group→role mapping | **GAP (integration logic)** | `setUserGroup` only understands `admin`/`user`/`guest`; resolved via Keycloak Role-Membership mapper → `abs_role` (documented) |

## 2. Configuration & artifacts — VERIFIED (structural)

| Artifact | Result |
|---|---|
| `pi/audiobookshelf/scripts/setup-keycloak.sh` | bash syntax OK; refuses `set -x`; secret to stdout only |
| `pi/audiobookshelf/scripts/apply-abs-settings.sh` | bash syntax OK; secret from env/file, substituted in memory |
| `pi/audiobookshelf/scripts/break-glass-setup.sh` | bash syntax OK; RNG password, Telegram once, no logging |
| `pi/audiobookshelf/scripts/verify-break-glass.sh` | bash syntax OK; password via `read -s`, never printed |
| `pi/audiobookshelf/scripts/rotate-keycloak-secret.sh` | bash syntax OK |
| `pi/audiobookshelf/oidc/abs-server-settings.json` | valid JSON; secret placeholder only |
| `pi/audiobookshelf/oidc/keycloak-client-config.json` | valid JSON; secret placeholder only |
| No secret committed | VERIFIED: only `${OIDC_CLIENT_SECRET}` placeholders present |
| `abs_role` mapper design | FIXED: two separate mappers (`abs_role-admin`, `abs_role-guest`) targeting the same claim. Original single mapper with duplicate `"role"` JSON keys was overwriting the second value. See PR review GH-78. |

## 3. Functional tests — PENDING RUNTIME

| Test (GH-60 §10) | Expected | Status |
|---|---|---|
| 10.1 login (member of `audiobookshelf-users`) | success | PENDING RUNTIME |
| 10.1 login denied (no `audiobookshelf-users`) | denied | PENDING RUNTIME |
| 10.1 invalid redirect URI rejected | denied | PENDING RUNTIME |
| 10.2 first login creates exactly one local account | 1 account | PENDING RUNTIME |
| 10.2 second login no extra account | still 1 | PENDING RUNTIME |
| 10.2 `preferred_username` change → same account | same `sub` | PENDING RUNTIME |
| 10.3 standard user read-only | guest | PENDING RUNTIME |
| 10.3 Michael admin via `audiobookshelf-admins` | admin | PENDING RUNTIME |
| 10.3 admin revocation at next login | downgraded | PENDING RUNTIME |
| 10.3 `audiobookshelf-users` removal blocks login | denied | PENDING RUNTIME |
| 10.4 logout ends local session | yes | PENDING RUNTIME |
| 10.4 logout ends Keycloak SSO | yes | PENDING RUNTIME |
| 10.4 reload stays unauthenticated | yes | PENDING RUNTIME |
| 10.4 different user can log in after | yes | PENDING RUNTIME |
| 10.5 restart preserves config + behavior | yes | PENDING RUNTIME |
| 10.6 secret rotation: new works, old fails | yes | PENDING RUNTIME |
| 10.7 break-glass local login (offline password) | success | PENDING RUNTIME |
| 10.7 independent of Keycloak | yes | PENDING RUNTIME |

**Procedure (runbook `audiobookshelf-runbook.md`):** execute
`setup-keycloak.sh` → `apply-abs-settings.sh` → login tests via browser →
`break-glass-setup.sh` + `verify-break-glass.sh` → `rotate-keycloak-secret.sh`
+ re-apply + restart → re-test.

## 4. Security negative tests — PENDING RUNTIME

| Test (GH-60 §10.8) | Expected | Status |
|---|---|---|
| Expired token rejected | denied | PENDING RUNTIME (isolated test env) |
| Wrong issuer rejected | denied | PENDING RUNTIME |
| Wrong audience / unauthorized party rejected | denied | PENDING RUNTIME |
| Invalid signature rejected | denied | PENDING RUNTIME |
| Token without `sub` rejected | denied | PENDING RUNTIME (`OidcAuthStrategy` throws `no sub`) |
| User without allowed group rejected | denied | PENDING RUNTIME |

These require a controlled environment with a forged/modified token and must
not mutate production signature/TLS validation. Procedure: use the existing
automated test harness or an isolated ABS instance with hand-crafted tokens.

## 5. Blocker report
**No blockers.** All MUSS capabilities (§4.1 sub-binding, §4.2 auto-provision,
§7.1 RP-Initiated logout) are natively supported by Audiobookshelf 2.35.1.
The two gaps (PKCE for web flow, native group-name mapping) are explicitly
**non-blocking** per GH-60 §3.1 and §5.3 and are resolved/documented via
permitted means (documentation; Keycloak role-membership integration logic).

## 6. Changed runtime objects (after runtime execution)
- Keycloak realm `homelab`: groups `audiobookshelf-users`, `audiobookshelf-admins`; client `audiobookshelf`; client roles `admin`, `guest`; mappers `audiobookshelf-groups`, `audiobookshelf-roles`; user `michael` in both groups.
- Audiobookshelf: OIDC server settings applied; local `admin` break-glass account.
- Secrets generated: 1 OIDC client secret, 1 break-glass password (values not recorded here).
