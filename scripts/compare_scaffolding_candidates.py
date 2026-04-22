#!/usr/bin/env python3
"""Compare FASTA-level metrics for alternative scaffolding candidates."""

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


def n_stat(lengths: list[int], fraction: float) -> int:
    if not lengths:
        return 0
    threshold = sum(lengths) * fraction
    running = 0
    for length in sorted(lengths, reverse=True):
        running += length
        if running >= threshold:
            return length
    return 0


def summarize(label: str, path: Path) -> dict[str, object]:
    lengths: list[int] = []
    gap_lengths: list[int] = []
    for _seq_id, seq in read_fasta(path):
        lengths.append(len(seq))
        gap_lengths.extend(match.end() - match.start() for match in GAP_RE.finditer(seq))

    total_bp = sum(lengths)
    gap_bp = sum(gap_lengths)
    return {
        "candidate": label,
        "fasta": str(path),
        "sequence_count": len(lengths),
        "total_bp": total_bp,
        "max_bp": max(lengths, default=0),
        "n50_bp": n_stat(lengths, 0.5),
        "n90_bp": n_stat(lengths, 0.9),
        "gap_count": len(gap_lengths),
        "gap_bp": gap_bp,
        "gap_pct": f"{(gap_bp / total_bp * 100) if total_bp else 0:.6f}",
        "max_gap_bp": max(gap_lengths, default=0),
    }


def parse_candidate(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("candidate must use label=/path/to/file.fa")
    label, path = value.split("=", 1)
    if not label:
        raise argparse.ArgumentTypeError("candidate label cannot be empty")
    return label, Path(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare FASTA metrics for scaffolding candidates.")
    parser.add_argument(
        "--candidate",
        action="append",
        type=parse_candidate,
        required=True,
        help="candidate in label=fasta format; repeat for YaHS, 3D-DNA, RagTag, gapfilled, etc.",
    )
    parser.add_argument("-o", "--output", type=Path, required=True, help="output TSV")
    args = parser.parse_args()

    rows = [summarize(label, path) for label, path in args.candidate]
    with args.output.open("w", newline="") as handle:
        fieldnames = [
            "candidate",
            "fasta",
            "sequence_count",
            "total_bp",
            "max_bp",
            "n50_bp",
            "n90_bp",
            "gap_count",
            "gap_bp",
            "gap_pct",
            "max_gap_bp",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
