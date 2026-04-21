#!/usr/bin/env python3
"""Validate FASTA files for genome assembly release readiness."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


VALID_SEQ_RE = re.compile(r"^[ACGTRYSWKMBDHVNacgtryswkmbdhvn.-]*$")
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_.:-]+$")


def read_fasta(path: Path):
    name = None
    seq_parts = []
    with path.open() as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.rstrip("\n")
            if line.startswith(">"):
                if name is not None:
                    yield name, "".join(seq_parts), line_number
                name = line[1:].split()[0]
                seq_parts = []
            elif name is None:
                yield "", "", line_number
            else:
                seq_parts.append(line.strip())
        if name is not None:
            yield name, "".join(seq_parts), line_number if "line_number" in locals() else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate FASTA IDs, sequence characters, lengths, and duplicate IDs.")
    parser.add_argument("fasta", type=Path, help="input FASTA")
    parser.add_argument("--min-length", type=int, default=200, help="minimum sequence length for release")
    parser.add_argument("--allow-gaps", action="store_true", help="allow '-' gap characters")
    parser.add_argument("-o", "--output", type=Path, help="optional TSV report path")
    args = parser.parse_args()

    issues = []
    lengths = {}
    ids = []

    for name, seq, line_number in read_fasta(args.fasta):
        if not name:
            issues.append(("ERROR", "missing_header", str(line_number), "", "sequence data found before first FASTA header"))
            continue
        ids.append(name)
        lengths[name] = len(seq)
        if not SAFE_ID_RE.match(name):
            issues.append(("ERROR", "unsafe_id", str(line_number), name, "ID should contain only letters, numbers, underscore, period, colon, or hyphen"))
        if len(seq) < args.min_length:
            issues.append(("WARN", "short_sequence", str(line_number), name, f"length {len(seq)} < {args.min_length}"))
        if not VALID_SEQ_RE.match(seq):
            issues.append(("ERROR", "invalid_sequence_character", str(line_number), name, "sequence contains characters outside IUPAC DNA alphabet"))
        if "-" in seq and not args.allow_gaps:
            issues.append(("ERROR", "gap_character", str(line_number), name, "sequence contains '-' gap characters"))

    counts = Counter(ids)
    for name, count in counts.items():
        if count > 1:
            issues.append(("ERROR", "duplicate_id", "", name, f"ID occurs {count} times"))

    summary = [
        ("INFO", "num_sequences", "", "", str(len(ids))),
        ("INFO", "total_length", "", "", str(sum(lengths.values()))),
        ("INFO", "min_length", "", "", str(min(lengths.values()) if lengths else 0)),
        ("INFO", "max_length", "", "", str(max(lengths.values()) if lengths else 0)),
    ]
    rows = summary + issues

    handle = args.output.open("w") if args.output else sys.stdout
    with handle:
        handle.write("level\tcheck\tline_or_record\tsequence_id\tmessage\n")
        for row in rows:
            handle.write("\t".join(row) + "\n")

    return 1 if any(level == "ERROR" for level, *_ in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())

