import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "extract_cron_response.py"


class ExtractCronResponseTest(unittest.TestCase):
    def test_extracts_response_and_writes_health_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            output = tmp_path / "2026-06-28_10-00-00.md"
            response = tmp_path / "last-response.md"
            health = tmp_path / "health.json"
            output.write_text(
                "# Cron Run\n\n## Prompt\nlarge prompt\n\n## Response\nstate changed: fixed docs\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(output),
                    "--loop-id",
                    "example-loop",
                    "--job-id",
                    "abc123",
                    "--state-path",
                    "state.json",
                    "--write-response",
                    str(response),
                    "--write-health",
                    str(health),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(response.read_text(encoding="utf-8"), "state changed: fixed docs\n")
            health_data = json.loads(health.read_text(encoding="utf-8"))
            self.assertEqual(health_data["loop_id"], "example-loop")
            self.assertEqual(health_data["job_id"], "abc123")
            self.assertEqual(health_data["last_status"], "ok")
            self.assertEqual(health_data["last_output_path"], str(output))
            self.assertEqual(health_data["last_response_path"], str(response))
            self.assertEqual(health_data["last_response_line"], 7)
            self.assertEqual(health_data["next_safe_action"], "review compact response")

    def test_missing_response_marker_falls_back_to_full_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            output = tmp_path / "output.md"
            response = tmp_path / "last-response.md"
            output.write_text("short script-only output\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(output), "--write-response", str(response)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(response.read_text(encoding="utf-8"), "short script-only output\n")


if __name__ == "__main__":
    unittest.main()
