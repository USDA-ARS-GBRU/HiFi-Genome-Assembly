#!/usr/bin/env python3
"""Audit FASTA headers for NCBI-oriented release readiness."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path


SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_.:-]+$")


def read_headers(path: Path):
    with path.open() as handle:
        for line_number, line in enumerate(handle, start=1):
            if line.startswith(">"):
                header = line[1:].rstrip("\n")
                seq_id = header.split()[0] if header.split() else ""
                yield line_number, header, seq_id


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit FASTA headers for uniqueness and conservative NCBI-safe IDs.")
    parser.add_argument("fasta", type=Path)
    parser.add_argument("-o", "--output", type=Path, help="output TSV; default stdout")
    args = parser.parse_args()

    headers = list(read_headers(args.fasta))
    counts = Counter(seq_id for _, _, seq_id in headers)
    rows = []

    for line_number, header, seq_id in headers:
        issues = []
        if not seq_id:
            issues.append("empty_id")
        if counts[seq_id] > 1:
            issues.append("duplicate_id")
        if not SAFE_ID_RE.match(seq_id):
            issues.append("unsafe_id_characters")
        if len(seq_id) > 50:
            issues.append("long_id")
        if any(char.isspace() for char in header):
            issues.append("description_present")
        if "[" in header or "]" in header:
            issues.append("source_modifiers_present_review_format")
        rows.append(
            {
                "line": line_number,
                "sequence_id": seq_id,
                "header": header,
                "status": "pass" if not issues else "review",
                "issues": ",".join(issues),
            }
        )

    handle = args.output.open("w", newline="") if args.output else sys.stdout
    with handle:
        writer = csv.DictWriter(handle, fieldnames=["line", "sequence_id", "header", "status", "issues"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    return 1 if any(row["status"] == "review" for row in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())

