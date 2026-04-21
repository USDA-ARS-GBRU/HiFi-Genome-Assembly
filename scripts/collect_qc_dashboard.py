#!/usr/bin/env python3
"""Collect first-pass assembly QC metrics into one TSV dashboard.

The script is intentionally permissive. It reads files when they exist and
leaves unknown values blank, which lets a project grow from v0.1 assembly
metrics into a fuller v1.0 release dashboard.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


BUSCO_RE = {
    "busco_complete": re.compile(r"C:([\d.]+)%"),
    "busco_single": re.compile(r"S:([\d.]+)%"),
    "busco_duplicated": re.compile(r"D:([\d.]+)%"),
    "busco_fragmented": re.compile(r"F:([\d.]+)%"),
    "busco_missing": re.compile(r"M:([\d.]+)%"),
    "busco_n": re.compile(r"n:(\d+)"),
}

HIFIASM_BASES_RE = re.compile(r"collected\s+([\d,]+)\s+bases\s+in\s+([\d,]+)\s+reads")
HIFIASM_GENOME_RE = re.compile(r"estimated genome size:\s*([\d,]+)")
HIFIASM_PEAK_RE = re.compile(r"peak_hom:\s*(-?\d+);\s*peak_het:\s*(-?\d+)")


FIELDS = [
    "sample",
    "assembly",
    "assembly_num_seqs",
    "assembly_sum_len",
    "assembly_min_len",
    "assembly_avg_len",
    "assembly_max_len",
    "hifiasm_total_bases",
    "hifiasm_total_reads",
    "hifiasm_estimated_genome_size",
    "hifiasm_coverage_from_bases",
    "hifiasm_last_peak_hom",
    "hifiasm_last_peak_het",
    "busco_lineage",
    "busco_complete",
    "busco_single",
    "busco_duplicated",
    "busco_fragmented",
    "busco_missing",
    "busco_n",
    "quast_contigs",
    "quast_total_length",
    "quast_largest_contig",
    "quast_n50",
    "quast_l50",
    "quast_gc",
    "merqury_qv",
    "merqury_error_rate",
    "merqury_completeness",
]


def empty_row(sample: str) -> dict[str, str]:
    row = {field: "" for field in FIELDS}
    row["sample"] = sample
    return row


def clean_int(value: str) -> str:
    return value.replace(",", "")


def sample_from_path(path: Path) -> str:
    name = path.name
    for suffix in [
        ".primary.fa",
        ".fa",
        ".fasta",
        ".fna",
        ".fastq.gz",
        ".fq.gz",
        ".err",
        ".out",
        ".txt",
        ".tsv",
        ".json",
    ]:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem


def parse_seqkit(path: Path) -> dict[str, dict[str, str]]:
    if not path or not path.exists():
        return {}

    with path.open(newline="") as handle:
        first = handle.readline()
        handle.seek(0)
        delimiter = "\t" if "\t" in first else None
        reader = csv.DictReader(handle, delimiter=delimiter)
        rows = {}
        for raw in reader:
            file_value = raw.get("file") or raw.get("File") or raw.get("filename") or ""
            if not file_value:
                continue
            sample = sample_from_path(Path(file_value))
            rows[sample] = {
                "assembly": file_value,
                "assembly_num_seqs": raw.get("num_seqs", ""),
                "assembly_sum_len": raw.get("sum_len", ""),
                "assembly_min_len": raw.get("min_len", ""),
                "assembly_avg_len": raw.get("avg_len", ""),
                "assembly_max_len": raw.get("max_len", ""),
            }
        return rows


def parse_hifiasm_logs(paths: list[Path]) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for path in paths:
        if not path.exists():
            continue
        sample = sample_from_path(path)
        row: dict[str, str] = {}
        text = path.read_text(errors="replace")
        for line in text.splitlines():
            bases = HIFIASM_BASES_RE.search(line)
            if bases:
                row["hifiasm_total_bases"] = clean_int(bases.group(1))
                row["hifiasm_total_reads"] = clean_int(bases.group(2))

            genome = HIFIASM_GENOME_RE.search(line)
            if genome:
                row["hifiasm_estimated_genome_size"] = clean_int(genome.group(1))

            peak = HIFIASM_PEAK_RE.search(line)
            if peak:
                row["hifiasm_last_peak_hom"] = peak.group(1)
                row["hifiasm_last_peak_het"] = peak.group(2)

        if row.get("hifiasm_total_bases") and row.get("hifiasm_estimated_genome_size"):
            genome_size = int(row["hifiasm_estimated_genome_size"])
            if genome_size > 0:
                row["hifiasm_coverage_from_bases"] = f"{int(row['hifiasm_total_bases']) / genome_size:.2f}"
        rows[sample] = row
    return rows


def parse_busco(paths: list[Path]) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for path in paths:
        if not path.exists():
            continue
        sample = sample_from_path(path)
        row: dict[str, str] = {}

        if path.suffix == ".json":
            try:
                data = json.loads(path.read_text())
            except json.JSONDecodeError:
                data = {}
            results = data.get("results", {})
            lineage = data.get("lineage_dataset", {}).get("name", "") or data.get("lineage_dataset", "")
            row["busco_lineage"] = str(lineage)
            for key, out_key in [
                ("Complete percentage", "busco_complete"),
                ("Single copy percentage", "busco_single"),
                ("Multi copy percentage", "busco_duplicated"),
                ("Fragmented percentage", "busco_fragmented"),
                ("Missing percentage", "busco_missing"),
                ("n_markers", "busco_n"),
            ]:
                if key in results:
                    row[out_key] = str(results[key])
        else:
            text = path.read_text(errors="replace")
            for line in text.splitlines():
                if "lineage dataset" in line.lower() or "dataset" in line.lower():
                    maybe = line.strip().split()
                    if maybe:
                        row.setdefault("busco_lineage", maybe[-1])
                if "C:" in line and "S:" in line and "D:" in line:
                    for field, pattern in BUSCO_RE.items():
                        match = pattern.search(line)
                        if match:
                            row[field] = match.group(1)
        rows[sample] = row
    return rows


def parse_quast(paths: list[Path]) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    label_map = {
        "# contigs": "quast_contigs",
        "Total length": "quast_total_length",
        "Largest contig": "quast_largest_contig",
        "N50": "quast_n50",
        "L50": "quast_l50",
        "GC (%)": "quast_gc",
    }

    for path in paths:
        if not path.exists():
            continue
        with path.open(newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            header = next(reader, [])
            if len(header) < 2:
                continue
            sample_names = [sample_from_path(Path(value)) for value in header[1:]]
            for sample in sample_names:
                rows.setdefault(sample, {})
            for values in reader:
                if not values:
                    continue
                key = label_map.get(values[0])
                if not key:
                    continue
                for sample, value in zip(sample_names, values[1:]):
                    rows[sample][key] = value
    return rows


def parse_merqury(paths: list[Path]) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for path in paths:
        if not path.exists():
            continue
        sample = sample_from_path(path)
        row = rows.setdefault(sample, {})
        text = path.read_text(errors="replace")
        for line in text.splitlines():
            parts = line.strip().split()
            if not parts:
                continue
            lower = line.lower()
            if "qv" in lower and not row.get("merqury_qv"):
                for part in reversed(parts):
                    try:
                        float(part)
                    except ValueError:
                        continue
                    row["merqury_qv"] = part
                    break
            if "error" in lower and not row.get("merqury_error_rate"):
                for part in reversed(parts):
                    try:
                        float(part)
                    except ValueError:
                        continue
                    row["merqury_error_rate"] = part
                    break
            if "completeness" in lower and not row.get("merqury_completeness"):
                for part in reversed(parts):
                    try:
                        float(part.rstrip("%"))
                    except ValueError:
                        continue
                    row["merqury_completeness"] = part.rstrip("%")
                    break
    return rows


def merge_rows(*tables: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    samples = sorted({sample for table in tables for sample in table})
    merged = []
    for sample in samples:
        row = empty_row(sample)
        for table in tables:
            row.update(table.get(sample, {}))
        merged.append(row)
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect assembly QC outputs into one TSV dashboard.")
    parser.add_argument("--seqkit", type=Path, help="seqkit stats TSV, e.g. 08_stats/seqkit_assembly_stats.tsv")
    parser.add_argument("--hifiasm-logs", nargs="*", type=Path, default=[], help="hifiasm log files")
    parser.add_argument("--busco", nargs="*", type=Path, default=[], help="BUSCO short_summary txt/json files")
    parser.add_argument("--quast", nargs="*", type=Path, default=[], help="QUAST report.tsv files")
    parser.add_argument("--merqury", nargs="*", type=Path, default=[], help="Merqury text reports, if available")
    parser.add_argument("-o", "--output", required=True, type=Path, help="output dashboard TSV")
    args = parser.parse_args()

    rows = merge_rows(
        parse_seqkit(args.seqkit) if args.seqkit else {},
        parse_hifiasm_logs(args.hifiasm_logs),
        parse_busco(args.busco),
        parse_quast(args.quast),
        parse_merqury(args.merqury),
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
