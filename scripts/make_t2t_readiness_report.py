#!/usr/bin/env python3
"""Combine gap, telomere, and optional centromere evidence into a T2T readiness report."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
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


def gap_metrics(path: Path) -> dict[str, dict[str, int]]:
    metrics = {}
    for seq_id, seq in read_fasta(path):
        gap_lengths = [match.end() - match.start() for match in GAP_RE.finditer(seq)]
        metrics[seq_id] = {
            "length": len(seq),
            "gap_count": len(gap_lengths),
            "gap_bp": sum(gap_lengths),
            "max_gap_bp": max(gap_lengths, default=0),
        }
    return metrics


def read_telomeres(path: Path | None) -> dict[str, dict[str, str]]:
    if path is None:
        return {}
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return {row["sequence_id"]: row for row in reader if row.get("sequence_id")}


def read_centromeres(path: Path | None) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    if path is None:
        return counts
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            seq_id = row.get("sequence_id") or row.get("seq_id") or row.get("chromosome") or row.get("object")
            if seq_id:
                counts[seq_id] += 1
    return counts


def classify(gaps: dict[str, int], telomere_status: str, centromere_count: int) -> str:
    if gaps["gap_count"] == 0 and telomere_status == "terminal_telomere_both" and centromere_count > 0:
        return "candidate_t2t_chromosome"
    if gaps["gap_count"] == 0 and telomere_status in {"terminal_telomere_both", "terminal_telomere_one"}:
        return "gapless_telomere_supported"
    if gaps["gap_count"] == 0:
        return "gapless_needs_terminal_review"
    if telomere_status == "internal_telomere_review":
        return "internal_telomere_review"
    return "scaffold_with_documented_gaps"


def write_markdown(path: Path, sample: str, version: str, rows: list[dict[str, object]]) -> None:
    lines = [
        f"# T2T Readiness Report: {sample}",
        "",
        f"- Protocol version: `{version}`",
        "",
        "| Sequence | Length | Gaps | Gap bp | Telomere status | Centromeres | Readiness class |",
        "| --- | ---: | ---: | ---: | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['sequence_id']} | {row['length']} | {row['gap_count']} | {row['gap_bp']} | "
            f"{row['telomere_status']} | {row['centromere_count']} | {row['readiness_class']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This report is a triage table, not a final T2T claim. Candidate complete chromosomes still require contact-map review, dotplots, contamination checks, repeat/centromere interpretation, and project-specific biological review.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a T2T readiness report.")
    parser.add_argument("--fasta", type=Path, required=True, help="final or candidate FASTA")
    parser.add_argument("--telomere-summary", type=Path, help="output from summarize_telomeres.py")
    parser.add_argument("--centromere-table", type=Path, help="optional TSV with sequence_id/seq_id/chromosome/object column")
    parser.add_argument("--sample", default="sample")
    parser.add_argument("--version", default="0.5.0-dev")
    parser.add_argument("-o", "--output", type=Path, required=True, help="output TSV")
    parser.add_argument("--markdown", type=Path, help="optional markdown report")
    args = parser.parse_args()

    gaps = gap_metrics(args.fasta)
    telomeres = read_telomeres(args.telomere_summary)
    centromeres = read_centromeres(args.centromere_table)
    rows: list[dict[str, object]] = []
    for seq_id in sorted(gaps):
        telomere_status = telomeres.get(seq_id, {}).get("status", "not_assessed")
        centromere_count = centromeres.get(seq_id, 0)
        row = {
            "sequence_id": seq_id,
            **gaps[seq_id],
            "telomere_status": telomere_status,
            "centromere_count": centromere_count,
            "readiness_class": classify(gaps[seq_id], telomere_status, centromere_count),
        }
        rows.append(row)

    with args.output.open("w", newline="") as handle:
        fieldnames = [
            "sequence_id",
            "length",
            "gap_count",
            "gap_bp",
            "max_gap_bp",
            "telomere_status",
            "centromere_count",
            "readiness_class",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    if args.markdown:
        write_markdown(args.markdown, args.sample, args.version, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
