#!/usr/bin/env python3
"""Check local Markdown links in repository documentation."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return target.split("#", 1)[0]


def is_external_or_special(target: str) -> bool:
    return (
        not target
        or "://" in target
        or target.startswith("mailto:")
        or target.startswith("#")
        or target.startswith("app:")
    )


def iter_markdown_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
    return sorted(set(files))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local Markdown links.")
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown files or directories to scan")
    parser.add_argument("-o", "--output", type=Path, help="optional TSV output")
    args = parser.parse_args()

    rows = []
    missing = False
    for md_path in iter_markdown_files(args.paths):
        text = md_path.read_text()
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in LINK_RE.finditer(line):
                raw_target = match.group(1)
                target = normalize_target(raw_target)
                if is_external_or_special(target):
                    continue
                target_path = (md_path.parent / target).resolve()
                exists = target_path.exists()
                if not exists:
                    missing = True
                rows.append(
                    {
                        "source": str(md_path),
                        "line": line_number,
                        "target": raw_target,
                        "resolved": str(target_path),
                        "exists": "yes" if exists else "no",
                        "status": "pass" if exists else "missing",
                    }
                )

    handle = args.output.open("w", newline="") if args.output else sys.stdout
    with handle:
        fieldnames = ["source", "line", "target", "resolved", "exists", "status"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
