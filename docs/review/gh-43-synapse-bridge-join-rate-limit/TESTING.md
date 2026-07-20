# Test Evidence

The hardening regression was added first and failed against the current template:

```text
FAIL: production inputs violate policy: ['synapse:bridge_portal_join_capacity']
```

Adding the bounded `rc_joins_per_room` override made the focused test green. All
local validations passed at source head
`29705bda2db24da7341b1290a83efd92cdf364c5`:

```bash
bash pi/tests/test_matrix_hardening.sh
python3 -c "import yaml; yaml.safe_load(open('pi/synapse/synapse.yaml.example', encoding='utf-8'))"
git diff --check
make ci
```

Gitea push CI run `557` and pull-request CI run `558` completed successfully.
Both exact-head results are recorded in `CI.json`.
