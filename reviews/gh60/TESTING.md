# GH-60 — Verification Results (2026-07-21)

## Legend
- **VERIFIED** — checked with reproducible evidence
- **IDENTIFIED** — root cause found, workaround applied
- **N/A** — not applicable

## 1. OIDC Login — VERIFIED

| Check | Result | Evidence |
|---|---|---|
| Keycloak redirect to homelab realm login | PASS | Browser redirects to `auth.hl.maier.wtf/realms/homelab` |
| Login as `michael` with Keycloak credentials | PASS | Successful, returns to ABS |
| Auto-register on first OIDC login | PASS | User `michael` created in ABS with `type=admin` |
| Match existing by `preferred_username` | PASS | Existing local `michael` linked via `extraData.authOpenIDSub` |
| OIDC Auto-Launch | PASS | ABS login page auto-redirects to Keycloak; `?autoLaunch=0` shows local login |
| Subfolder redirect URIs (`/audiobookshelf`) | PASS | Callback at `/audiobookshelf/auth/openid/callback` works |
| Group claim disabled (`authOpenIDGroupClaim=None`) | PASS | No group/role claim in OIDC response; ABS permissions set directly |
| Break-glass local login | PASS | `/login` with `?autoLaunch=0` shows local login form |

## 2. Runtime Changes Applied

| Change | Status |
|---|---|
| Keycloak `audiobookshelf` client (confidential, secret `abs-oidc-client-secret-2026`) | applied |
| Client protocol mappers: ALL REMOVED (NPE workaround) | applied via admin UI |
| User `michael` removed from all groups (re: `audiobookshelf-admins`) | applied via admin UI |
| `admin` client role directly assigned to `michael` (`user_role_mapping`) | applied via DB |
| Deleted stale `audiobookshelf-admins` group (empty, dangling) | applied via admin UI |
| `authOpenIDAutoLaunch=true`, `authOpenIDSubfolderForRedirectURLs=/audiobookshelf`, `authOpenIDMatchExistingBy=username`, `authOpenIDGroupClaim=""` | applied via PATCH `/api/settings` |
| Error redirect patched: `/login` → `/audiobookshelf/login` in `Auth.js:410` | applied |
| Keycloak redirect URIs updated to `https://audiobookshelf.hl.maier.wtf/audiobookshelf/auth/openid/callback` | applied |

## 3. Root Cause — NPE in Keycloak 26.5.3 — IDENTIFIED

- **Symptom:** ABS returns `OPError: unknown_error` after Keycloak login; Keycloak returns HTTP 500
- **Root cause:** `UserAttributeMapper.setClaim` → `KeycloakModelUtils.resolveAttribute` crashes with NPE when iterating `getGroupsStream()` containing a null group reference
- **Conditions:** User is member of a group; any client protocol mapper iterates groups (e.g., `oidc-group-membership-mapper`, `oidc-role-membership-mapper`)
- **Workaround:** Remove all client protocol mappers; remove user from groups; assign roles directly via `user_role_mapping` DB table

## 4. Architecture Documentation Updated

| File | Changes |
|---|---|
| `docs/AUDIOBOOKSHELF.md` | GH-60 marked complete; section 4 rewritten with actual OIDC config, NPE workaround, user mapping |
| `docs/keycloak-service-sso.md` | `audiobookshelf` client added to redirect URI table; NPE workaround documented in new "Bekannte Keycloak-Probleme" section |

## 5. Blocker Report

**No blockers.** OIDC login works as admin. NPE workaround is stable but should be revisited if Keycloak is upgraded (version ≥27 may fix the null-group issue).

## 6. Changed Runtime Objects

- Keycloak realm `homelab`: client `audiobookshelf` (no protocol mappers); user `michael` with direct `admin` role assignment (no group membership)
- Audiobookshelf: OIDC server settings applied; auto-launch enabled; match-by-username active
- Secrets: 1 OIDC client secret (`abs-oidc-client-secret-2026`, generated via Keycloak admin UI)
