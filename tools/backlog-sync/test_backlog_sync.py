import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).with_name("backlog_sync.py")
SPEC = importlib.util.spec_from_file_location("backlog_sync", MODULE_PATH)
assert SPEC and SPEC.loader
sync = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync
SPEC.loader.exec_module(sync)


class BacklogSyncTests(unittest.TestCase):
    def test_replace_managed_preserves_manual_suffix(self):
        cfg = type("Cfg", (), {
            "marker_start": "<!-- start -->",
            "marker_end": "<!-- end -->",
        })()
        existing = "<!-- start -->\nold\n<!-- end -->\n\nManual notes"
        replacement = "<!-- start -->\nnew\n<!-- end -->"
        result = sync.replace_managed(existing, replacement, cfg)
        self.assertIn("new", result)
        self.assertNotIn("old", result)
        self.assertIn("Manual notes", result)

    def test_scan_epics_is_deterministic(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            epic = root / "EPICS" / "MEDIA"
            epic.mkdir(parents=True)
            (epic / "b.md").write_text("# Media\nB", encoding="utf-8")
            (epic / "a.md").write_text("A", encoding="utf-8")
            first = sync.scan_epics(root / "EPICS")["MEDIA"]
            second = sync.scan_epics(root / "EPICS")["MEDIA"]
            self.assertEqual(first.source_hash, second.source_hash)
            self.assertLess(first.body.index("source:a.md"), first.body.index("source:b.md"))

    def test_control_rejects_unknown_state(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "control.json"
            path.write_text(json.dumps({"state": "mystery"}), encoding="utf-8")
            with self.assertRaises(sync.ValidationError):
                sync.load_control(path)

    def test_atomic_json_is_noop_for_same_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "state.json"
            self.assertTrue(sync.atomic_json(path, {"b": 2, "a": 1}))
            self.assertFalse(sync.atomic_json(path, {"a": 1, "b": 2}))

    def test_deleted_epic_mapping_is_persistent(self):
        state = {"schema_version": "1.0", "items": {"OLD": {"issue_number": 17}}}
        current_epics = {"NEW": object()}
        removed = sorted(set(state["items"]) - set(current_epics))
        self.assertEqual(["OLD"], removed)


if __name__ == "__main__":
    unittest.main()
