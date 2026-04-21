#!/usr/bin/env python3
"""Extract simple coverage and k-mer peak metrics from hifiasm log files.

The hifiasm log format changes slightly across versions, so this script is
deliberately conservative. It reports fields when it can find them and leaves
unknown values blank.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


RE_BASES = re.compile(r"collected\s+([\d,]+)\s+bases\s+in\s+([\d,]+)\s+reads")
RE_MEDIAN = re.compile(r"median read length:\s*([\d,]+)")
RE_GENOME_SIZE = re.compile(r"estimated genome size:\s*([\d,]+)")
RE_PEAK = re.compile(r"peak_hom:\s*(-?\d+);\s*peak_het:\s*(-?\d+)")


def clean_int(value: str | None) -> str:
    if value is None:
        return ""
    return value.replace(",", "")


def parse_log(path: Path) -> dict[str, str]:
    row = {
        "log": str(path),
        "sample": path.name,
        "total_bases": "",
        "total_reads": "",
        "median_read_length": "",
        "estimated_genome_size": "",
        "last_peak_hom": "",
        "last_peak_het": "",
        "coverage_from_bases_and_genome_size": "",
    }

    try:
        text = path.read_text(errors="replace")
    except OSError as exc:
        row["sample"] = f"ERROR: {exc}"
        return row

    for line in text.splitlines():
        bases = RE_BASES.search(line)
        if bases:
            row["total_bases"] = clean_int(bases.group(1))
            row["total_reads"] = clean_int(bases.group(2))

        median = RE_MEDIAN.search(line)
        if median:
            row["median_read_length"] = clean_int(median.group(1))

        genome_size = RE_GENOME_SIZE.search(line)
        if genome_size:
            row["estimated_genome_size"] = clean_int(genome_size.group(1))

        peak = RE_PEAK.search(line)
        if peak:
            row["last_peak_hom"] = peak.group(1)
            row["last_peak_het"] = peak.group(2)

    if row["total_bases"] and row["estimated_genome_size"]:
        total_bases = int(row["total_bases"])
        genome_size = int(row["estimated_genome_size"])
        if genome_size > 0:
            row["coverage_from_bases_and_genome_size"] = f"{total_bases / genome_size:.2f}"

    return row


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract total bases, read count, genome-size estimate, and peak_hom/peak_het from hifiasm logs."
    )
    parser.add_argument("logs", nargs="+", type=Path, help="hifiasm stdout/stderr log files")
    parser.add_argument("-o", "--output", type=Path, help="output TSV path; default stdout")
    args = parser.parse_args()

    fieldnames = [
        "sample",
        "log",
        "total_bases",
        "total_reads",
        "median_read_length",
        "estimated_genome_size",
        "coverage_from_bases_and_genome_size",
        "last_peak_hom",
        "last_peak_het",
    ]

    rows = [parse_log(path) for path in args.logs]

    if args.output:
        handle = args.output.open("w", newline="")
    else:
        import sys

        handle = sys.stdout

    with handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
