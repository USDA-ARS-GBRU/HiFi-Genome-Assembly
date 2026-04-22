#!/usr/bin/env python3
"""Build a compact before/after gap-filling report for FASTA assemblies."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
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


def fasta_metrics(path: Path) -> dict[str, float]:
    lengths: list[int] = []
    gap_lengths: list[int] = []
    for _seq_id, seq in read_fasta(path):
        lengths.append(len(seq))
        gap_lengths.extend(match.end() - match.start() for match in GAP_RE.finditer(seq))

    total_bp = sum(lengths)
    gap_bp = sum(gap_lengths)
    return {
        "sequence_count": len(lengths),
        "total_bp": total_bp,
        "n50_bp": n_stat(lengths, 0.5),
        "n90_bp": n_stat(lengths, 0.9),
        "gap_count": len(gap_lengths),
        "gap_bp": gap_bp,
        "gap_pct": (gap_bp / total_bp * 100) if total_bp else 0,
        "max_gap_bp": max(gap_lengths, default=0),
    }


def read_decision_counts(path: Path | None) -> Counter:
    counts: Counter = Counter()
    if path is None:
        return counts
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if "final_decision" not in (reader.fieldnames or []):
            raise SystemExit(f"Decision log is missing final_decision column: {path}")
        for row in reader:
            counts[row.get("final_decision", "missing") or "missing"] += 1
    return counts


def write_tsv(path: Path, before: dict[str, float], after: dict[str, float]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "before", "after", "delta"], delimiter="\t")
        writer.writeheader()
        for metric in before:
            writer.writerow(
                {
                    "metric": metric,
                    "before": f"{before[metric]:.6f}" if metric == "gap_pct" else int(before[metric]),
                    "after": f"{after[metric]:.6f}" if metric == "gap_pct" else int(after[metric]),
                    "delta": f"{after[metric] - before[metric]:.6f}"
                    if metric == "gap_pct"
                    else int(after[metric] - before[metric]),
                }
            )


def write_markdown(path: Path, sample: str, version: str, before_path: Path, after_path: Path, before, after, decisions) -> None:
    lines = [
        f"# Gap-Filling Report: {sample}",
        "",
        f"- Protocol version: `{version}`",
        f"- Before FASTA: `{before_path}`",
        f"- After FASTA: `{after_path}`",
        "",
        "## Summary",
        "",
        "| Metric | Before | After | Delta |",
        "| --- | ---: | ---: | ---: |",
    ]
    for metric in before:
        before_value = f"{before[metric]:.6f}" if metric == "gap_pct" else str(int(before[metric]))
        after_value = f"{after[metric]:.6f}" if metric == "gap_pct" else str(int(after[metric]))
        delta = after[metric] - before[metric]
        delta_value = f"{delta:.6f}" if metric == "gap_pct" else str(int(delta))
        lines.append(f"| {metric} | {before_value} | {after_value} | {delta_value} |")

    lines.extend(["", "## Decision Log Counts", ""])
    if decisions:
        for decision, count in sorted(decisions.items()):
            lines.append(f"- `{decision}`: {count}")
    else:
        lines.append("- No decision log supplied.")

    lines.extend(
        [
            "",
            "## Release Interpretation",
            "",
            "Gap filling is acceptable only when each filled interval has independent support and downstream FASTA, AGP, dotplot, read-mapping, and contact-map checks are regenerated. Remaining gaps should be documented rather than hidden.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a before/after gap-filling report.")
    parser.add_argument("--before", type=Path, required=True, help="pre-gap-filling FASTA")
    parser.add_argument("--after", type=Path, required=True, help="post-gap-filling FASTA")
    parser.add_argument("--decision-log", type=Path, help="optional gap-filling decision TSV")
    parser.add_argument("--sample", default="sample", help="sample name for markdown report")
    parser.add_argument("--version", default="0.5.0-dev", help="protocol or assembly version")
    parser.add_argument("-o", "--output", type=Path, required=True, help="metric comparison TSV")
    parser.add_argument("--markdown", type=Path, help="optional markdown report")
    args = parser.parse_args()

    before = fasta_metrics(args.before)
    after = fasta_metrics(args.after)
    decisions = read_decision_counts(args.decision_log)

    write_tsv(args.output, before, after)
    if args.markdown:
        write_markdown(args.markdown, args.sample, args.version, args.before, args.after, before, after, decisions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
