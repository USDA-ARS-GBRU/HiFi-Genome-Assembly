#!/usr/bin/env python3
"""Summarize telomeric motif hits near FASTA sequence ends."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


COMPLEMENT = str.maketrans("ACGTacgt", "TGCAtgca")


def reverse_complement(seq: str) -> str:
    return seq.translate(COMPLEMENT)[::-1].upper()


def read_fasta(path: Path):
    name = None
    seq_parts: list[str] = []
    with path.open() as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line.startswith(">"):
                if name is not None:
                    yield name, "".join(seq_parts).upper()
                name = line[1:].split()[0]
                seq_parts = []
            else:
                seq_parts.append(line.strip())
        if name is not None:
            yield name, "".join(seq_parts).upper()


def count_overlapping(seq: str, motif: str) -> int:
    count = 0
    start = 0
    while True:
        index = seq.find(motif, start)
        if index == -1:
            return count
        count += 1
        start = index + 1


def motif_count(seq: str, motif: str, rev_motif: str) -> int:
    count = count_overlapping(seq, motif)
    if rev_motif != motif:
        count += count_overlapping(seq, rev_motif)
    return count


def status(left_count: int, right_count: int, internal_count: int, min_hits: int) -> str:
    left = left_count >= min_hits
    right = right_count >= min_hits
    if left and right:
        return "terminal_telomere_both"
    if left or right:
        return "terminal_telomere_one"
    if internal_count >= min_hits:
        return "internal_telomere_review"
    return "no_telomere_signal"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize telomeric motif counts at sequence ends.")
    parser.add_argument("fasta", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True, help="output TSV")
    parser.add_argument("--motif", default="TTTAGGG", help="telomeric repeat motif")
    parser.add_argument("--window", type=int, default=10000, help="terminal window size in bp")
    parser.add_argument("--min-hits", type=int, default=3, help="minimum motif hits for a positive call")
    args = parser.parse_args()

    motif = args.motif.upper()
    rev_motif = reverse_complement(motif)
    rows = []
    for seq_id, seq in read_fasta(args.fasta):
        window = min(args.window, len(seq))
        left_seq = seq[:window]
        right_seq = seq[-window:] if window else ""
        internal_seq = seq[window:-window] if len(seq) > 2 * window else ""
        left_count = motif_count(left_seq, motif, rev_motif)
        right_count = motif_count(right_seq, motif, rev_motif)
        internal_count = motif_count(internal_seq, motif, rev_motif)
        rows.append(
            {
                "sequence_id": seq_id,
                "length": len(seq),
                "motif": motif,
                "reverse_complement": rev_motif,
                "window_bp": window,
                "left_terminal_hits": left_count,
                "right_terminal_hits": right_count,
                "internal_hits": internal_count,
                "status": status(left_count, right_count, internal_count, args.min_hits),
            }
        )

    with args.output.open("w", newline="") as handle:
        fieldnames = [
            "sequence_id",
            "length",
            "motif",
            "reverse_complement",
            "window_bp",
            "left_terminal_hits",
            "right_terminal_hits",
            "internal_hits",
            "status",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
