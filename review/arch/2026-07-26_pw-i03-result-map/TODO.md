# TODO — PW-I03 Result Semantics

## Open Items

- Activate `playwright-platform` CI step (requires Docker non-root runner setup).
- Run full `run.sh prerequisite_error` and `run.sh error` in Docker-less
  environment (currently tested via static mock only).

## Follow-up Issues

- PW-I04 (planned): HTML/JSON result rendering and artifact collection.
- Infrastructure: Resolve CI Docker UID 0 issue to enable platform tests in
  pipeline (post-Issue).
- Documentation: Update PW-D01 runner-bootstrap ADR with --read-only removal
  rationale.

## Known Limitations

- The `chmod 777` call in `run.sh` generates a warning when the results
  directory is owned by a different user (non-fatal).
- Real Docker infrastructure errors (exit >=125) cannot be tested without
  actual Docker daemon failure.
