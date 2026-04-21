#!/usr/bin/env python3
"""Filter FASTA records by length and optionally rename them with a prefix.

This is useful for creating release candidates with stable, NCBI-safe IDs.
It intentionally avoids third-party dependencies so it can run on login nodes
or minimal cluster environments.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def fasta_records(path: Path):
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter FASTA by minimum length and optionally rename records.")
    parser.add_argument("-i", "--input", required=True, type=Path, help="input FASTA")
    parser.add_argument("-o", "--output", required=True, type=Path, help="output FASTA")
    parser.add_argument("--min-length", type=int, default=200, help="minimum sequence length to keep")
    parser.add_argument("--prefix", default="", help="rename kept records as PREFIX_000001, PREFIX_000002, ...")
    parser.add_argument("--width", type=int, default=80, help="output line width")
    parser.add_argument("--map", type=Path, help="optional TSV mapping old IDs to new IDs")
    args = parser.parse_args()

    kept = 0
    dropped = 0
    mapping: list[tuple[str, str, int]] = []

    with args.output.open("w") as out:
        for old_name, seq in fasta_records(args.input):
            if len(seq) < args.min_length:
                dropped += 1
                continue
            kept += 1
            new_name = f"{args.prefix}_{kept:06d}" if args.prefix else old_name
            write_wrapped(new_name, seq, args.width, out)
            mapping.append((old_name, new_name, len(seq)))

    if args.map:
        with args.map.open("w") as out_map:
            out_map.write("old_id\tnew_id\tlength\n")
            for old_name, new_name, length in mapping:
                out_map.write(f"{old_name}\t{new_name}\t{length}\n")

    print(f"kept={kept}\tdropped={dropped}", file=sys.stderr)


if __name__ == "__main__":
    main()
