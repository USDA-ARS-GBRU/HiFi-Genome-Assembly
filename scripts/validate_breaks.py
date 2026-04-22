#!/usr/bin/env python3
"""Validate curated FASTA breakpoints before editing an assembly."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


def read_fasta_lengths(path: Path) -> dict[str, int]:
    lengths: dict[str, int] = {}
    name = None
    seq_parts: list[str] = []
    with path.open() as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line.startswith(">"):
                if name is not None:
                    lengths[name] = len("".join(seq_parts))
                name = line[1:].split()[0]
                seq_parts = []
            else:
                seq_parts.append(line.strip())
        if name is not None:
            lengths[name] = len("".join(seq_parts))
    return lengths


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit breakpoints before using split_fasta_at_breaks.py.")
    parser.add_argument("--fasta", type=Path, required=True, help="input FASTA that would be edited")
    parser.add_argument("--breaks", type=Path, required=True, help="TSV with sequence_id and break_after_1based columns")
    parser.add_argument("-o", "--output", type=Path, help="output TSV; default stdout")
    args = parser.parse_args()

    lengths = read_fasta_lengths(args.fasta)
    rows = []
    keys = []
    has_error = False

    with args.breaks.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {"sequence_id", "break_after_1based"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"break TSV missing required columns: {', '.join(sorted(missing))}")

        for row_number, row in enumerate(reader, start=2):
            seq_id = row.get("sequence_id", "").strip()
            raw_break = row.get("break_after_1based", "").strip()
            status = "pass"
            message = "breakpoint is within sequence bounds"
            length = lengths.get(seq_id, 0)
            break_after = ""

            if not seq_id:
                status = "error"
                message = "missing sequence_id"
            elif seq_id not in lengths:
                status = "error"
                message = "sequence_id not found in FASTA"
            else:
                try:
                    break_after_int = int(raw_break)
                    break_after = str(break_after_int)
                except ValueError:
                    status = "error"
                    message = "break_after_1based is not an integer"
                else:
                    if break_after_int < 1 or break_after_int >= length:
                        status = "error"
                        message = f"breakpoint must be between 1 and {length - 1}"

            if status == "error":
                has_error = True
            key = (seq_id, break_after or raw_break)
            keys.append(key)
            rows.append(
                {
                    "row": row_number,
                    "sequence_id": seq_id,
                    "break_after_1based": break_after or raw_break,
                    "sequence_length": length,
                    "status": status,
                    "message": message,
                }
            )

    counts = Counter(keys)
    for row in rows:
        key = (row["sequence_id"], row["break_after_1based"])
        if row["status"] == "pass" and counts[key] > 1:
            row["status"] = "error"
            row["message"] = "duplicate breakpoint"
            has_error = True

    handle = args.output.open("w", newline="") if args.output else sys.stdout
    with handle:
        fieldnames = ["row", "sequence_id", "break_after_1based", "sequence_length", "status", "message"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
