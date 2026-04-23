#!/usr/bin/env python3
"""Compare repeat summary TSV files side by side."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_COLUMNS = [
    "sample",
    "total_masked_percent",
    "ltr_percent",
    "dna_transposon_percent",
    "unclassified_percent",
    "method",
    "notes",
]


def load_summary(path: Path) -> dict[str, str]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise SystemExit(f"{path} is missing a header")
        missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing:
            raise SystemExit(f"{path} is missing required columns: {', '.join(missing)}")
        rows = list(reader)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one summary row")
    return rows[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare repeat summary TSVs.")
    parser.add_argument(
        "--candidate",
        action="append",
        required=True,
        metavar="LABEL=TSV",
        help="repeat summary candidate in label=path format; repeat for multiple candidates",
    )
    parser.add_argument("-o", "--output", type=Path, required=True, help="output TSV path")
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    for item in args.candidate:
        if "=" not in item:
            raise SystemExit(f"candidate must be label=path, got: {item}")
        label, path_text = item.split("=", 1)
        summary = load_summary(Path(path_text))
        rows.append(
            {
                "candidate": label,
                "sample": summary["sample"],
                "method": summary["method"],
                "total_masked_percent": summary["total_masked_percent"],
                "ltr_percent": summary["ltr_percent"],
                "dna_transposon_percent": summary["dna_transposon_percent"],
                "unclassified_percent": summary["unclassified_percent"],
                "notes": summary["notes"],
            }
        )

    with args.output.open("w", newline="") as handle:
        fieldnames = [
            "candidate",
            "sample",
            "method",
            "total_masked_percent",
            "ltr_percent",
            "dna_transposon_percent",
            "unclassified_percent",
            "notes",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
