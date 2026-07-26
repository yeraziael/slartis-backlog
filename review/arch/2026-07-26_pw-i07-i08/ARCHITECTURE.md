# Architecture

## Publication Flow

1. `sanitise.sh` scans candidate evidence before bundle assembly.
2. `bundle-assemble.py` rejects unsafe input, copies only the manifest, JUnit,
   and permitted PNG/ZIP artifacts, then creates a sorted SHA-256 inventory.
3. `bundle-validate.py` verifies the layout, result-specific retention class,
   artifact policy, inventory membership, sizes, and checksums.

## Result Classes

| Result | Artifacts | Retention |
|---|---|---|
| `pass` | forbidden | 7 days |
| `fail` | PNG screenshot and ZIP trace required | 30 days |
| `prerequisite_error` | optional | 30 days |
| `error` | optional | 30 days |

The inventory intentionally does not hash itself. It binds every publishable
file: `manifest.json`, `junit.xml`, and any allowed artifact.
