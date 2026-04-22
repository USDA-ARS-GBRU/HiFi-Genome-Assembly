#!/usr/bin/env python3
"""Summarize N-gap runs in a FASTA file."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


GAP_RE = re.compile(r"N+", re.IGNORECASE)


def read_fasta(path: Path):
    name = None
    seq_parts: list[str] = []
    with path.open() as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line.startswith(">"):
                if name is not None:
                    yield name, "".join(seq_parts)
                name = line[1:].split()[0]
                seq_parts = []
            else:
                seq_parts.append(line.strip())
        if name is not None:
            yield name, "".join(seq_parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize gap runs represented by Ns in a FASTA.")
    parser.add_argument("fasta", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True, help="per-gap TSV output")
    parser.add_argument("--summary", type=Path, help="one-row summary TSV output")
    args = parser.parse_args()

    rows = []
    sequence_count = 0
    total_bp = 0

    for seq_id, seq in read_fasta(args.fasta):
        sequence_count += 1
        total_bp += len(seq)
        for index, match in enumerate(GAP_RE.finditer(seq), start=1):
            rows.append(
                {
                    "sequence_id": seq_id,
                    "gap_index": index,
                    "start_1based": match.start() + 1,
                    "end_1based": match.end(),
                    "length": match.end() - match.start(),
                }
            )

    with args.output.open("w", newline="") as handle:
        fieldnames = ["sequence_id", "gap_index", "start_1based", "end_1based", "length"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    if args.summary:
        total_gap_bp = sum(int(row["length"]) for row in rows)
        with args.summary.open("w", newline="") as handle:
            fieldnames = ["fasta", "sequence_count", "total_bp", "gap_count", "gap_bp", "gap_pct", "max_gap_bp"]
            writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerow(
                {
                    "fasta": str(args.fasta),
                    "sequence_count": sequence_count,
                    "total_bp": total_bp,
                    "gap_count": len(rows),
                    "gap_bp": total_gap_bp,
                    "gap_pct": f"{(total_gap_bp / total_bp * 100) if total_bp else 0:.6f}",
                    "max_gap_bp": max((int(row["length"]) for row in rows), default=0),
                }
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
