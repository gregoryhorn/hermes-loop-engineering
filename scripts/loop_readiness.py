#!/usr/bin/env python3
"""Lightweight readiness checker for Hermes Loop Engineering LOOP.md specs."""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "purpose",
    "non-goals",
    "watched scope",
    "schedule",
    "durable state",
    "verification evidence",
    "notification rule",
    "human escalation triggers",
    "kill switch",
]

RISKY_WORDS = [
    "auto-merge",
    "delete",
    "production",
    "payment",
    "secret",
    "credential",
    "publish",
    "deploy",
]


def normalize_heading(line: str) -> str | None:
    m = re.match(r"^#+\s+(.+?)\s*$", line)
    if not m:
        return None
    return re.sub(r"[^a-z0-9 -]", "", m.group(1).lower()).strip()


def check(path: Path) -> tuple[int, list[str]]:
    text = path.read_text(encoding="utf-8")
    headings = {h for line in text.splitlines() if (h := normalize_heading(line))}
    messages: list[str] = []
    score = 100

    for section in REQUIRED_SECTIONS:
        if not any(section in h for h in headings):
            score -= 8
            messages.append(f"missing section: {section}")

    lower = text.lower()
    if "l1" not in lower and "report" not in lower:
        score -= 10
        messages.append("does not clearly start as L1/report-only")

    if "state" not in lower:
        score -= 12
        messages.append("no durable state mentioned")

    if "hermes cron pause" not in lower and "kill switch" not in lower:
        score -= 10
        messages.append("no concrete kill switch")

    for word in RISKY_WORDS:
        if word in lower and "human" not in lower and "approval" not in lower:
            score -= 5
            messages.append(f"risky term appears without obvious human gate: {word}")

    return max(score, 0), messages


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: loop_readiness.py LOOP.md", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    score, messages = check(path)
    print(f"Loop readiness score: {score}/100")
    if messages:
        print("Findings:")
        for msg in messages:
            print(f"- {msg}")
    else:
        print("No basic readiness issues found.")
    return 0 if score >= 80 else 1


if __name__ == "__main__":
    raise SystemExit(main())
