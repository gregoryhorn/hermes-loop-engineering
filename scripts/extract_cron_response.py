#!/usr/bin/env python3
"""Extract the compact response from a Hermes cron output file.

Hermes agent cron outputs can contain long prompt/skill preambles. This helper
keeps the full output intact while writing a small response artifact and a
machine-readable health summary for loop dashboards.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RESPONSE_MARKERS = ("## Response", "# Response")


def extract_response(text: str) -> tuple[str, int | None]:
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.strip() in RESPONSE_MARKERS:
            response = "".join(lines[index + 1 :]).lstrip("\n")
            return response, index + 2
    return text, 1 if text else None


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_health(args: argparse.Namespace, output_path: Path, response_path: Path | None, response_line: int | None) -> dict[str, Any]:
    return {
        "kind": "hermes_loop_health",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "loop_id": args.loop_id,
        "job_id": args.job_id,
        "state_path": args.state_path,
        "last_status": args.status,
        "last_output_path": str(output_path),
        "last_response_path": str(response_path) if response_path else None,
        "last_response_line": response_line,
        "last_blocker_id": args.blocker_id,
        "next_safe_action": args.next_safe_action,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract compact Hermes cron response and optional loop health JSON.")
    parser.add_argument("output", help="Cron output Markdown/text file")
    parser.add_argument("--loop-id", default=None)
    parser.add_argument("--job-id", default=None)
    parser.add_argument("--state-path", default=None)
    parser.add_argument("--status", default="ok")
    parser.add_argument("--blocker-id", default=None)
    parser.add_argument("--next-safe-action", default="review compact response")
    parser.add_argument("--write-response", help="Path for compact response Markdown/text")
    parser.add_argument("--write-health", help="Path for loop health JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)
    text = output_path.read_text(encoding="utf-8")
    response, response_line = extract_response(text)

    response_path = Path(args.write_response) if args.write_response else None
    if response_path:
        write_text(response_path, response)

    health_path = Path(args.write_health) if args.write_health else None
    if health_path:
        write_json(health_path, build_health(args, output_path, response_path, response_line))

    print(json.dumps({"response_line": response_line, "response_path": str(response_path) if response_path else None, "health_path": str(health_path) if health_path else None}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
