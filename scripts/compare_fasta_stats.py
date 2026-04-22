#!/usr/bin/env python3
"""Compare basic FASTA statistics before and after correction."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_lengths(path: Path) -> list[int]:
    lengths = []
    name = None
    seq_parts: list[str] = []
    with path.open() as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line.startswith(">"):
                if name is not None:
                    lengths.append(len("".join(seq_parts)))
                name = line[1:].split()[0]
                seq_parts = []
            else:
                seq_parts.append(line.strip())
        if name is not None:
            lengths.append(len("".join(seq_parts)))
    return lengths


def n_stat(lengths: list[int], fraction: float) -> int:
    if not lengths:
        return 0
    total = sum(lengths)
    threshold = total * fraction
    running = 0
    for length in sorted(lengths, reverse=True):
        running += length
        if running >= threshold:
            return length
    return 0


def stats(path: Path) -> dict[str, int]:
    lengths = read_lengths(path)
    return {
        "sequence_count": len(lengths),
        "total_bp": sum(lengths),
        "min_bp": min(lengths) if lengths else 0,
        "max_bp": max(lengths) if lengths else 0,
        "n50_bp": n_stat(lengths, 0.5),
        "n90_bp": n_stat(lengths, 0.9),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare pre/post correction FASTA statistics.")
    parser.add_argument("--before", type=Path, required=True, help="pre-correction FASTA")
    parser.add_argument("--after", type=Path, required=True, help="post-correction FASTA")
    parser.add_argument("-o", "--output", type=Path, required=True, help="output TSV")
    args = parser.parse_args()

    before = stats(args.before)
    after = stats(args.after)

    with args.output.open("w", newline="") as handle:
        fieldnames = ["metric", "before", "after", "delta"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for metric in before:
            writer.writerow(
                {
                    "metric": metric,
                    "before": before[metric],
                    "after": after[metric],
                    "delta": after[metric] - before[metric],
                }
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
