#!/usr/bin/env python3
"""Split FASTA records at documented 1-based breakpoints."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


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


def write_wrapped(name: str, seq: str, width: int, handle) -> None:
    handle.write(f">{name}\n")
    for start in range(0, len(seq), width):
        handle.write(seq[start : start + width] + "\n")


def read_breaks(path: Path) -> dict[str, list[dict[str, str]]]:
    breaks: dict[str, list[dict[str, str]]] = defaultdict(list)
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {"sequence_id", "break_after_1based"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"break TSV missing required columns: {', '.join(sorted(missing))}")
        for row_number, row in enumerate(reader, start=2):
            seq_id = row["sequence_id"].strip()
            raw_break = row["break_after_1based"].strip()
            if not seq_id or not raw_break:
                raise SystemExit(f"missing sequence_id or break_after_1based on row {row_number}")
            try:
                break_after = int(raw_break)
            except ValueError as exc:
                raise SystemExit(f"break_after_1based must be an integer on row {row_number}") from exc
            row["break_after_1based"] = str(break_after)
            row["_row_number"] = str(row_number)
            breaks[seq_id].append(row)
    return breaks


def main() -> int:
    parser = argparse.ArgumentParser(description="Split FASTA records at curated breakpoints.")
    parser.add_argument("--fasta", type=Path, required=True, help="input FASTA")
    parser.add_argument("--breaks", type=Path, required=True, help="TSV with sequence_id and break_after_1based columns")
    parser.add_argument("-o", "--output", type=Path, required=True, help="output split FASTA")
    parser.add_argument("--map", type=Path, required=True, help="output TSV mapping new segments to source coordinates")
    parser.add_argument("--width", type=int, default=80, help="output FASTA line width")
    args = parser.parse_args()

    breaks_by_id = read_breaks(args.breaks)
    seen_ids: set[str] = set()
    had_error = False
    map_rows = []

    with args.output.open("w") as out:
        for seq_id, seq in read_fasta(args.fasta):
            seen_ids.add(seq_id)
            seq_breaks = breaks_by_id.get(seq_id, [])
            positions = sorted({int(row["break_after_1based"]) for row in seq_breaks})
            invalid = [pos for pos in positions if pos < 1 or pos >= len(seq)]
            if invalid:
                print(f"ERROR: invalid breakpoints for {seq_id}: {invalid}; length={len(seq)}", file=sys.stderr)
                had_error = True
                continue

            starts = [1] + [pos + 1 for pos in positions]
            ends = positions + [len(seq)]
            for index, (start, end) in enumerate(zip(starts, ends), start=1):
                suffix = f"part{index:02d}" if positions else "part01"
                new_id = f"{seq_id}_{suffix}" if positions else seq_id
                segment = seq[start - 1 : end]
                write_wrapped(new_id, segment, args.width, out)
                map_rows.append(
                    {
                        "source_id": seq_id,
                        "new_id": new_id,
                        "source_start_1based": start,
                        "source_end_1based": end,
                        "length": len(segment),
                        "split": "yes" if positions else "no",
                    }
                )

    missing_sequences = sorted(set(breaks_by_id) - seen_ids)
    if missing_sequences:
        print(f"ERROR: breakpoints refer to missing FASTA IDs: {', '.join(missing_sequences)}", file=sys.stderr)
        had_error = True

    with args.map.open("w", newline="") as handle:
        fieldnames = ["source_id", "new_id", "source_start_1based", "source_end_1based", "length", "split"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(map_rows)

    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
