#!/usr/bin/env python3
"""Check relative Markdown links in this repository.

The checker is intentionally dependency-free so scheduled Hermes loops can run it
before committing documentation changes. It validates inline Markdown links and
images that point to local files, while ignoring URLs, mail links, pure anchors,
and Obsidian-style wikilinks.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_SCHEMES = {"http", "https", "mailto", "tel"}


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if ".git" not in path.parts and path.is_file()
    )


def normalize_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if not target or target.startswith("#") or target.startswith("[["):
        return None
    parsed = urlparse(target)
    if parsed.scheme in SKIP_SCHEMES:
        return None
    if parsed.scheme and parsed.scheme not in {""}:
        return None
    return unquote(parsed.path)


def check_file(path: Path, root: Path) -> list[str]:
    findings: list[str] = []
    text = path.read_text(encoding="utf-8")
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in LINK_RE.finditer(line):
            target = normalize_target(match.group(1))
            if target is None:
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                findings.append(
                    f"{path.relative_to(root)}:{line_number}: link escapes repo: {match.group(1)}"
                )
                continue
            if not candidate.exists():
                findings.append(
                    f"{path.relative_to(root)}:{line_number}: missing target: {match.group(1)}"
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check relative Markdown links")
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings: list[str] = []
    for md_file in iter_markdown_files(root):
        findings.extend(check_file(md_file, root))

    if findings:
        print("Markdown link check failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print(f"Markdown link check passed for {len(iter_markdown_files(root))} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
