from __future__ import annotations

import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

EXPECTED = {
    "assets/hermes-loop-engineering-banner.svg": {"kind": "svg"},
    "assets/hermes-loop-architecture.svg": {"kind": "svg"},
    "assets/hermes-loop-engineering-banner.png": {"kind": "png", "size": (1600, 840)},
    "assets/hermes-loop-architecture.png": {"kind": "png", "size": (1400, 900)},
    "assets/social-preview.png": {"kind": "png", "size": (1280, 640)},
}


def check_svg(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"{path}: invalid SVG XML: {exc}"]
    if not root.tag.endswith("svg"):
        errors.append(f"{path}: root element is not svg")
    if not root.get("width") or not root.get("height") or not root.get("viewBox"):
        errors.append(f"{path}: SVG must define width, height, and viewBox")
    text = path.read_text(encoding="utf-8", errors="replace")
    if "<title" not in text or "<desc" not in text:
        errors.append(f"{path}: SVG should include title and desc for accessibility")
    return errors


def read_png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 33 or data[:8] != PNG_SIGNATURE:
        raise ValueError("missing PNG signature")
    ihdr_length = struct.unpack(">I", data[8:12])[0]
    ihdr_type = data[12:16]
    if ihdr_length != 13 or ihdr_type != b"IHDR":
        raise ValueError("missing IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def check_png(path: Path, expected_size: tuple[int, int]) -> list[str]:
    try:
        actual_size = read_png_size(path)
    except Exception as exc:  # noqa: BLE001 - CLI validator should report decode failures
        return [f"{path}: invalid PNG: {exc}"]
    if actual_size != expected_size:
        return [f"{path}: expected {expected_size}, got {actual_size}"]
    return []


def main() -> int:
    errors: list[str] = []
    for rel, spec in EXPECTED.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"{rel}: missing")
            continue
        if spec["kind"] == "svg":
            errors.extend(check_svg(path))
        elif spec["kind"] == "png":
            errors.extend(check_png(path, spec["size"]))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Asset check passed for {len(EXPECTED)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
