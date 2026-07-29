# Risks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Synthetic safety coverage changes | Low | Medium | Focused safe-summary test remains green. |
| Scanner bypass through fixture exclusion | Low | High | No scanner exclusion was added; test source remains scanned. |
| Runtime regression | Low | Low | Change is test-only. |
