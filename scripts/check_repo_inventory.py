#!/usr/bin/env python3
"""Check that README-listed project paths exist."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PREFIXES = ("docs/", "scripts/", "examples/", "01_sbatch_templates/")
PATH_RE = re.compile(r"(?P<path>(?:docs|scripts|examples|01_sbatch_templates)/[A-Za-z0-9_./-]+)")


def iter_paths(text: str) -> set[str]:
    paths = set()
    for match in PATH_RE.finditer(text):
        token_start = max(text.rfind(char, 0, match.start()) for char in " \t\n(") + 1
        token_end_candidates = [text.find(char, match.end()) for char in " \t\n)"]
        token_end = min(index for index in token_end_candidates if index != -1) if any(index != -1 for index in token_end_candidates) else len(text)
        token = text[token_start:token_end]
        if "://" in token:
            continue
        path = match.group("path").rstrip(".,)")
        if path.startswith(PREFIXES):
            paths.add(path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Check that README-referenced repo paths exist.")
    parser.add_argument("--readme", type=Path, default=Path("README.md"), help="README or markdown file to scan")
    parser.add_argument("-o", "--output", type=Path, help="output TSV; default stdout")
    args = parser.parse_args()

    text = args.readme.read_text()
    rows = []
    missing = False
    for raw_path in sorted(iter_paths(text)):
        path = Path(raw_path)
        exists = path.exists()
        if not exists:
            missing = True
        rows.append((raw_path, "yes" if exists else "no", "pass" if exists else "missing"))

    handle = args.output.open("w") if args.output else sys.stdout
    with handle:
        handle.write("path\texists\tstatus\n")
        for row in rows:
            handle.write("\t".join(row) + "\n")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
