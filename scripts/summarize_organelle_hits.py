#!/usr/bin/env python3
"""Summarize assembly-vs-organelle PAF hits into sequence-level candidates."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def parse_paf(path: Path):
    with path.open() as handle:
        for line in handle:
            if not line.strip():
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 12:
                continue
            yield {
                "query": fields[0],
                "query_len": int(fields[1]),
                "query_start": int(fields[2]),
                "query_end": int(fields[3]),
                "strand": fields[4],
                "target": fields[5],
                "target_len": int(fields[6]),
                "matches": int(fields[9]),
                "block_len": int(fields[10]),
                "mapq": int(fields[11]),
            }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize organelle PAF alignments into keep/remove/review candidates.")
    parser.add_argument("paf", type=Path, help="PAF from minimap2 assembly-vs-organelle reference alignment")
    parser.add_argument("-o", "--output", required=True, type=Path, help="output TSV")
    parser.add_argument("--remove-coverage", type=float, default=0.80, help="query coverage threshold for remove candidate")
    parser.add_argument("--review-coverage", type=float, default=0.10, help="query coverage threshold for review candidate")
    parser.add_argument("--min-identity", type=float, default=0.90, help="minimum alignment identity to count")
    args = parser.parse_args()

    grouped = defaultdict(lambda: {"query_len": 0, "aligned_bases": 0, "matches": 0, "block_len": 0, "targets": set(), "best_identity": 0.0})

    for hit in parse_paf(args.paf):
        identity = hit["matches"] / hit["block_len"] if hit["block_len"] else 0.0
        if identity < args.min_identity:
            continue
        row = grouped[hit["query"]]
        row["query_len"] = max(row["query_len"], hit["query_len"])
        row["aligned_bases"] += max(0, hit["query_end"] - hit["query_start"])
        row["matches"] += hit["matches"]
        row["block_len"] += hit["block_len"]
        row["targets"].add(hit["target"])
        row["best_identity"] = max(row["best_identity"], identity)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        fieldnames = [
            "sequence_id",
            "length_bp",
            "organelle_aligned_bases",
            "organelle_query_coverage",
            "best_identity",
            "targets",
            "candidate_decision",
            "rationale",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for sequence_id, row in sorted(grouped.items()):
            length = row["query_len"]
            coverage = min(1.0, row["aligned_bases"] / length) if length else 0.0
            identity = row["matches"] / row["block_len"] if row["block_len"] else 0.0
            if coverage >= args.remove_coverage:
                decision = "remove_or_submit_separately"
                rationale = "most of sequence aligns to organelle reference"
            elif coverage >= args.review_coverage:
                decision = "review"
                rationale = "partial organelle alignment; distinguish nuclear insertion from contaminant/free organelle contig"
            else:
                decision = "keep"
                rationale = "low organelle alignment coverage"
            writer.writerow(
                {
                    "sequence_id": sequence_id,
                    "length_bp": length,
                    "organelle_aligned_bases": row["aligned_bases"],
                    "organelle_query_coverage": f"{coverage:.6f}",
                    "best_identity": f"{row['best_identity']:.6f}",
                    "targets": ",".join(sorted(row["targets"])),
                    "candidate_decision": decision,
                    "rationale": rationale,
                }
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
