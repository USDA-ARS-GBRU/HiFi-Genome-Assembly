#!/usr/bin/env python3
"""Create simple QC plots from an assembly dashboard TSV.

This script is optional and requires matplotlib. It is meant to provide quick
review figures, not final manuscript styling.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Optional


def as_float(value: str) -> Optional[float]:
    if value is None:
        return None
    cleaned = value.replace(",", "").rstrip("%")
    if cleaned == "":
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def read_dashboard(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def plot_bar(rows: list[dict[str, str]], field: str, ylabel: str, output: Path) -> bool:
    import matplotlib.pyplot as plt

    values = []
    labels = []
    for row in rows:
        value = as_float(row.get(field, ""))
        if value is None:
            continue
        labels.append(row.get("sample", "sample"))
        values.append(value)

    if not values:
        return False

    fig_width = max(7, len(labels) * 0.45)
    fig, ax = plt.subplots(figsize=(fig_width, 4.5))
    ax.bar(labels, values, color="#4C78A8")
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Sample")
    ax.tick_params(axis="x", rotation=60)
    ax.grid(axis="y", color="#D0D0D0", linewidth=0.6)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Create quick QC bar plots from assembly_qc_dashboard.tsv.")
    parser.add_argument("-i", "--input", required=True, type=Path, help="assembly QC dashboard TSV")
    parser.add_argument("-o", "--output-dir", required=True, type=Path, help="directory for PNG plots")
    args = parser.parse_args()

    rows = read_dashboard(args.input)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    plot_specs = [
        ("assembly_sum_len", "Assembly length (bp)", "assembly_length.png"),
        ("assembly_num_seqs", "Number of sequences", "assembly_num_sequences.png"),
        ("assembly_max_len", "Largest sequence (bp)", "assembly_largest_sequence.png"),
        ("busco_complete", "BUSCO complete (%)", "busco_complete.png"),
        ("busco_duplicated", "BUSCO duplicated (%)", "busco_duplicated.png"),
        ("merqury_qv", "Merqury QV", "merqury_qv.png"),
        ("merqury_completeness", "Merqury completeness (%)", "merqury_completeness.png"),
        ("hifiasm_coverage_from_bases", "HiFi coverage from hifiasm log", "hifiasm_coverage.png"),
        ("fcs_adaptor_records", "FCS-adaptor records", "fcs_adaptor_records.png"),
        ("fcs_gx_records", "FCS-GX records", "fcs_gx_records.png"),
    ]

    written = 0
    for field, ylabel, filename in plot_specs:
        if plot_bar(rows, field, ylabel, args.output_dir / filename):
            written += 1

    print(f"Wrote {written} plot(s) to {args.output_dir}")


if __name__ == "__main__":
    main()
