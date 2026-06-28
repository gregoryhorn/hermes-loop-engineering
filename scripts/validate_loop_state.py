#!/usr/bin/env python3
"""Permissive validator for Hermes loop state JSON files.

The validator intentionally checks only a small required core and reports
recommended operational fields as warnings. Additional fields are allowed so
private/local loop state can extend the public starter contract safely.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = [
    "loop_name",
    "level",
    "status",
    "last_run_at",
    "last_status",
    "notification_policy",
    "kill_switch",
]

RECOMMENDED_FIELDS = [
    "owner",
    "job_id",
    "last_output_path",
    "last_blocker_id",
    "next_safe_action",
    "escalation_policy",
]

STRING_OR_NULL_FIELDS = {"last_run_at", "last_status", "last_output_path", "last_blocker_id", "next_safe_action"}
STRING_FIELDS = {"loop_name", "level", "status", "notification_policy", "kill_switch"}


def load_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("state file must contain a JSON object")
    return data


def validate_state(state: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in state:
            errors.append(f"missing required field: {field}")

    for field in RECOMMENDED_FIELDS:
        if field not in state:
            warnings.append(f"missing recommended field: {field}")

    for field in STRING_FIELDS:
        if field in state and not isinstance(state[field], str):
            errors.append(f"field must be a string: {field}")

    for field in STRING_OR_NULL_FIELDS:
        if field in state and state[field] is not None and not isinstance(state[field], str):
            errors.append(f"field must be a string or null: {field}")

    if "escalation_policy" in state and not isinstance(state["escalation_policy"], list):
        errors.append("field must be a list: escalation_policy")

    return errors, warnings


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: validate_loop_state.py STATE.json [STATE2.json ...]", file=sys.stderr)
        return 2

    exit_code = 0
    for raw_path in argv[1:]:
        path = Path(raw_path)
        print(f"{path}: ", end="")
        try:
            state = load_state(path)
            errors, warnings = validate_state(state)
        except ValueError as exc:
            print("invalid")
            print(f"error: {exc}")
            exit_code = 1
            continue

        if errors:
            print("invalid")
            for error in errors:
                print(f"error: {error}")
            exit_code = 1
        else:
            print("valid")
        for warning in warnings:
            print(f"warning: {warning}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
