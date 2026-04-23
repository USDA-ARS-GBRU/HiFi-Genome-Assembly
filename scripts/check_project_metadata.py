#!/usr/bin/env python3
"""Check that public project metadata files are present."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


REQUIRED = [
    ("VERSION", "version"),
    ("CHANGELOG.md", "changelog"),
    ("README.md", "readme"),
    ("CONTRIBUTING.md", "contributing"),
    ("CITATION.cff", "citation"),
    ("LICENSE", "license"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check required project metadata files.")
    parser.add_argument("-o", "--output", type=Path, help="optional TSV output")
    args = parser.parse_args()

    rows = []
    missing = False
    for path_text, kind in REQUIRED:
        path = Path(path_text)
        exists = path.exists() and path.stat().st_size > 0
        if not exists:
            missing = True
        rows.append(
            {
                "path": path_text,
                "kind": kind,
                "exists": "yes" if exists else "no",
                "status": "pass" if exists else "missing",
            }
        )

    handle = args.output.open("w", newline="") if args.output else sys.stdout
    with handle:
        fieldnames = ["path", "kind", "exists", "status"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
