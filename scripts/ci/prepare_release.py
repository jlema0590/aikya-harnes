#!/usr/bin/env python3
"""Prepare Aikya CHANGELOG release notes on an explicitly approved CI branch.

Does not create tags, releases or modify files other than CHANGELOG.md.
"""
from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALID_VERSION = re.compile(r"^v[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9][A-Za-z0-9.-]*)?$")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    version = args.version
    if not VALID_VERSION.fullmatch(version):
        parser.error("Use a version such as v5.8.0")
    changelog = ROOT / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    if re.search(r"(?m)^## " + re.escape(version) + r"(?:\s|$)", text):
        parser.error(f"Version {version} already exists in CHANGELOG.md")
    header = re.search(r"(?m)^## Sin publicar\s*$", text)
    if header is None:
        parser.error("Expected `## Sin publicar` in CHANGELOG.md")
    remaining = text[header.end():]
    next_heading = re.search(r"(?m)^## ", remaining)
    notes = remaining[:next_heading.start()] if next_heading else remaining
    if not re.search(r"(?m)^\s*[-*] .+", notes):
        parser.error("No unreleased changes to include in a release")
    date = datetime.now(timezone.utc).date().isoformat()
    replacement = f"## Sin publicar\n\n## {version} — {date}"
    updated = text[:header.start()] + replacement + text[header.end():]
    changelog.write_text(updated, encoding="utf-8")
    print(f"Prepared reviewable release notes for {version} in CHANGELOG.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
