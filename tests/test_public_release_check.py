import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "public_release_check.py"

sys.path.insert(0, str(ROOT))
from scripts import public_release_check  # noqa: E402


class PublicReleaseCheckTest(unittest.TestCase):
    def test_current_repo_passes_public_release_gates(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Public release check passed", result.stdout)

    def test_workflow_action_gate_rejects_node20_action_majors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow_dir = root / ".github" / "workflows"
            workflow_dir.mkdir(parents=True)
            (workflow_dir / "validate.yml").write_text(
                "steps:\n"
                "  - uses: actions/checkout@v4\n"
                "  - uses: actions/setup-python@v5\n",
                encoding="utf-8",
            )

            result = public_release_check.check_workflow_actions(root)

        self.assertFalse(result.passed)
        self.assertIn("actions/checkout", result.detail)
        self.assertIn("actions/setup-python", result.detail)

    def test_readme_gate_rejects_wrong_user_journey_and_keyword_dump(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Example\n\n"
                "## Quick start\n\n"
                "### 1. Install Hermes Agent\n\n"
                "## SEO\n\n"
                "**Keywords:** AI agents, cron\n",
                encoding="utf-8",
            )

            result = public_release_check.check_readme_user_journey(root)

        self.assertFalse(result.passed)
        self.assertIn("Install Hermes Agent", result.detail)
        self.assertIn("Keywords", result.detail)

    def test_public_private_boundary_gate_rejects_private_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            private_path = "/home/" + "gregory" + "/private"
            (root / "docs" / "leak.md").write_text(f"local path: {private_path}", encoding="utf-8")

            result = public_release_check.check_public_private_boundary(root)

        self.assertFalse(result.passed)
        self.assertIn("/home/" + "gregory", result.detail)

    def test_public_private_boundary_ignores_png_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copy(ROOT / "assets" / "social-preview.png", root / "social-preview.png")

            result = public_release_check.check_public_private_boundary(root)

        self.assertTrue(result.passed, result.detail)


if __name__ == "__main__":
    unittest.main()
