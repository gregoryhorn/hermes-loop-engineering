import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_loop_state.py"


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class ValidateLoopStateTest(unittest.TestCase):
    def test_valid_template_passes_with_recommended_warnings_only(self):
        result = run_validator(ROOT / "templates" / "state.example.json")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("valid", result.stdout.lower())
        self.assertIn("warning", result.stdout.lower())
        self.assertIn("owner", result.stdout)

    def test_missing_required_core_field_fails(self):
        state = {
            "loop_name": "missing-kill-switch",
            "level": "L1 Report",
            "status": "active",
            "last_run_at": None,
            "last_status": None,
            "notification_policy": "notify only on state changes",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            path.write_text(json.dumps(state), encoding="utf-8")

            result = run_validator(path)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("missing required field: kill_switch", result.stdout)

    def test_extension_fields_are_allowed(self):
        state = {
            "loop_name": "custom-loop",
            "level": "L1 Report",
            "status": "active",
            "last_run_at": None,
            "last_status": "ok",
            "notification_policy": "notify only on state changes",
            "kill_switch": "hermes cron pause abc123",
            "custom_private_extension": {"team": "local"},
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            path.write_text(json.dumps(state), encoding="utf-8")

            result = run_validator(path)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("custom_private_extension", result.stdout)


if __name__ == "__main__":
    unittest.main()
