#!/usr/bin/env python3
"""Check that GFF3 sequence IDs are present in the submitted FASTA."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


def read_fasta_ids(path: Path) -> set[str]:
    ids = set()
    with path.open() as handle:
        for line in handle:
            if line.startswith(">"):
                seq_id = line[1:].strip().split()[0]
                if seq_id:
                    ids.add(seq_id)
    return ids


def read_gff3_seqids(path: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    with path.open() as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != 9:
                counts[f"malformed_line:{line_number}"] += 1
                continue
            counts[parts[0]] += 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit GFF3 sequence IDs against FASTA headers.")
    parser.add_argument("--fasta", type=Path, required=True, help="submitted genome FASTA")
    parser.add_argument("--gff3", type=Path, required=True, help="annotation GFF3")
    parser.add_argument("-o", "--output", type=Path, help="output TSV; default stdout")
    args = parser.parse_args()

    fasta_ids = read_fasta_ids(args.fasta)
    gff_counts = read_gff3_seqids(args.gff3)

    rows = []
    has_error = False

    for seq_id, count in sorted(gff_counts.items()):
        if seq_id.startswith("malformed_line:"):
            status = "error"
            in_fasta = "no"
            has_error = True
        elif seq_id in fasta_ids:
            status = "pass"
            in_fasta = "yes"
        else:
            status = "missing_from_fasta"
            in_fasta = "no"
            has_error = True
        rows.append(
            {
                "gff3_seqid": seq_id,
                "gff3_records": count,
                "in_fasta": in_fasta,
                "status": status,
            }
        )

    fasta_only = sorted(fasta_ids - {seq_id for seq_id in gff_counts if not seq_id.startswith("malformed_line:")})
    for seq_id in fasta_only:
        rows.append(
            {
                "gff3_seqid": seq_id,
                "gff3_records": 0,
                "in_fasta": "yes",
                "status": "fasta_only",
            }
        )

    handle = args.output.open("w", newline="") if args.output else sys.stdout
    with handle:
        writer = csv.DictWriter(handle, fieldnames=["gff3_seqid", "gff3_records", "in_fasta", "status"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
