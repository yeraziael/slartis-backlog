# Risks — PW-I03 Result Semantics

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Container rootfs writable (--read-only removed) | Low | Medium | Still protected by --cap-drop ALL, --network none (test phase), --security-opt no-new-privileges, read-only repo bind mount |
| CI cannot run real Docker tests | High | Medium | Documented gap; static tests + manual verification on rechenknecht |
| npm lockfile generated with host node v18 (container expects v24) | Low | Low | lockfileVersion 3 is compatible; verified working in real Docker run |
| Root user runs run.sh | Low | High | Guard clause rejects UID 0/GID 0 with exit 2 |
| /mnt/raid0 noexec breaks direct script execution | Medium | Low | All script calls use explicit `bash` wrapper |
| Playwright version drift in lockfile | Low | Medium | validate-lock.mjs enforces @playwright/test@1.61.1 |
