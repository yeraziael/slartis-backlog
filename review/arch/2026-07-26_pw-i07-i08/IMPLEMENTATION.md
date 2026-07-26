# Implementation

| Area | Change |
|---|---|
| `evidence/sanitisation/` | Prohibited-pattern scanner, Python ZIP/image helpers, clean/leak fixtures, and scanner contract tests |
| `evidence/bundle/` | Deterministic assembler, validator, and golden/negative self-test |
| `tests/test_playwright_bootstrap.py` | Sanitisation and bundle contract coverage |
| `tests/playwright/README.md` | Evidence bundle invocation and retention documentation |

The scanner reports only file and category-level status. It never writes a
matched value to output. The bundle assembler calls the scanner before copying
any evidence and rejects unknown file types.
