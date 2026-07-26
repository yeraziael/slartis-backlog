# Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Unrecognised secret format | Medium | High | Fail-closed publication gate; patterns are versioned and testable |
| Corrupt or altered bundle | Low | High | Validator checks inventory membership, byte sizes, and SHA-256 hashes |
| Retention not enforced by Gitea | Medium | Medium | Bundle carries an enforceable class; upload/deletion scheduling is deliberately deferred |
| Screenshot pixels contain sensitive text | Medium | Medium | Metadata is scanned now; OCR/redaction is deferred and no upload is implemented |
