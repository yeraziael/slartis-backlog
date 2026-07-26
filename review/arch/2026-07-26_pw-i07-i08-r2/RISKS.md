# Risks

| Risk | Mitigation |
|---|---|
| Scanner dependency unavailable | Reject evidence instead of publishing uninspected artifacts |
| Archive malformed or encrypted | Structural validation/extraction failure rejects it |
| Symlink references a non-evidence path | Gate and assembler reject all symlinks and verify resolved containment |
| Screenshot pixels contain sensitive text | Upload remains deferred; OCR/redaction remains a future control |
