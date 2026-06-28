from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ACTION_MINIMUMS = {
    "actions/checkout": 7,
    "actions/setup-python": 6,
}

PRIVATE_PATTERNS = (
    "/home/" + "gregory",
    "gho" + "_",
    "github" + "_pat_",
    "cadd" + "860cd1ca",
    "327d" + "bf30b47e",
)

REQUIRED_README_PHRASES = (
    "This guide assumes you already use Hermes Agent",
    "L1 report-only loop",
    "Smoke-run once before trusting the schedule",
    "state-change-only reporting",
)

FORBIDDEN_README_PATTERNS = (
    r"^###\s+\d+\.\s+Install Hermes Agent\s*$",
    r"^##\s+SEO\s*$",
    r"\*\*Keywords:\*\*",
)


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def check_workflow_actions(root: Path = ROOT) -> CheckResult:
    workflow = root / ".github" / "workflows" / "validate.yml"
    text = read_text(workflow)
    failures: list[str] = []
    for action, minimum in ACTION_MINIMUMS.items():
        versions = [int(match) for match in re.findall(rf"{re.escape(action)}@v(\d+)", text)]
        if not versions:
            failures.append(f"missing {action}@v{minimum}+")
            continue
        too_old = [version for version in versions if version < minimum]
        if too_old:
            failures.append(f"{action} uses deprecated major(s): {', '.join('v' + str(v) for v in too_old)}")
    if failures:
        return CheckResult("workflow-actions", False, "; ".join(failures))
    return CheckResult("workflow-actions", True, "GitHub action majors meet public release floor")


def check_readme_user_journey(root: Path = ROOT) -> CheckResult:
    text = read_text(root / "README.md")
    failures: list[str] = []
    for phrase in REQUIRED_README_PHRASES:
        if phrase not in text:
            failures.append(f"missing README phrase: {phrase}")
    for pattern in FORBIDDEN_README_PATTERNS:
        if re.search(pattern, text, flags=re.MULTILINE):
            failures.append(f"forbidden README pattern present: {pattern}")
    if failures:
        return CheckResult("readme-user-journey", False, "; ".join(failures))
    return CheckResult("readme-user-journey", True, "README assumes existing Hermes user and avoids keyword-dump SEO")


def check_assets(root: Path = ROOT) -> CheckResult:
    completed = subprocess.run(
        [sys.executable, str(root / "scripts" / "check_assets.py")],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return CheckResult("assets", False, (completed.stdout + completed.stderr).strip())
    return CheckResult("assets", True, completed.stdout.strip())


def check_public_private_boundary(root: Path = ROOT) -> CheckResult:
    ignored_dirs = {".git", "__pycache__", ".pytest_cache"}
    scanned_files = 0
    hits: list[str] = []
    for path in root.rglob("*"):
        if any(part in ignored_dirs for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}:
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        scanned_files += 1
        for pattern in PRIVATE_PATTERNS:
            if pattern in text:
                hits.append(f"{path.relative_to(root)} contains {pattern}")
    if hits:
        return CheckResult("public-private-boundary", False, "; ".join(hits[:10]))
    return CheckResult("public-private-boundary", True, f"scanned {scanned_files} text files; no private boundary markers found")


def check_ci_public_surface(root: Path = ROOT) -> CheckResult:
    workflow = read_text(root / ".github" / "workflows" / "validate.yml")
    required_commands = (
        "python scripts/check_assets.py",
        "python scripts/check_markdown_links.py .",
        "python -m unittest discover -s tests -v",
    )
    missing = [command for command in required_commands if command not in workflow]
    if missing:
        return CheckResult("ci-public-surface", False, "missing CI command(s): " + "; ".join(missing))
    return CheckResult("ci-public-surface", True, "CI covers visual assets, links, and tests")


def run_checks(root: Path = ROOT) -> list[CheckResult]:
    return [
        check_workflow_actions(root),
        check_readme_user_journey(root),
        check_assets(root),
        check_public_private_boundary(root),
        check_ci_public_surface(root),
    ]


def main() -> int:
    results = run_checks(ROOT)
    failed = [result for result in results if not result.passed]
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name}: {result.detail}")
    if failed:
        print(f"Public release check failed: {len(failed)} issue(s).", file=sys.stderr)
        return 1
    print(f"Public release check passed for {len(results)} gates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
