#!/usr/bin/env python3
"""Audit a release manifest for required files."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


TRUE_VALUES = {"yes", "true", "required", "y", "1"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check release_manifest.tsv paths and required-file status.")
    parser.add_argument("manifest", type=Path, help="TSV with file, category, description, required_for_release columns")
    parser.add_argument("--base-dir", type=Path, default=Path("."), help="base directory for relative paths")
    parser.add_argument("-o", "--output", type=Path, help="output TSV; default stdout")
    args = parser.parse_args()

    rows = []
    missing_required = False

    with args.manifest.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for raw in reader:
            file_value = raw.get("file", "")
            required_value = raw.get("required_for_release", "")
            required = required_value.strip().lower() in TRUE_VALUES
            path = args.base_dir / file_value
            exists = path.exists()
            if required and not exists:
                missing_required = True
            rows.append(
                {
                    "file": file_value,
                    "category": raw.get("category", ""),
                    "required_for_release": required_value,
                    "exists": "yes" if exists else "no",
                    "status": "pass" if exists or not required else "missing_required",
                }
            )

    handle = args.output.open("w", newline="") if args.output else sys.stdout
    with handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "category", "required_for_release", "exists", "status"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    return 1 if missing_required else 0


if __name__ == "__main__":
    raise SystemExit(main())

