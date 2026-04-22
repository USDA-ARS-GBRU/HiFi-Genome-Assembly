#!/usr/bin/env python3
"""Summarize curated assembly corrections from split maps and decision logs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(rows: list[dict[str, str]], path: Path) -> None:
    fieldnames = [
        "source_id",
        "new_segments",
        "split_count",
        "source_span",
        "decision_edit_ids",
        "final_actions",
        "primary_evidence",
        "secondary_evidence",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]], path: Path) -> None:
    with path.open("w") as handle:
        handle.write("# Correction Summary\n\n")
        if not rows:
            handle.write("No corrected sequences were reported.\n")
            return
        handle.write("| Source ID | New segments | Split count | Evidence |\n")
        handle.write("| --- | --- | --- | --- |\n")
        for row in rows:
            evidence = "; ".join(part for part in [row["primary_evidence"], row["secondary_evidence"]] if part)
            handle.write(f"| {row['source_id']} | {row['new_segments']} | {row['split_count']} | {evidence} |\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize curated correction outputs.")
    parser.add_argument("--split-map", type=Path, required=True, help="map TSV from split_fasta_at_breaks.py")
    parser.add_argument("--decision-log", type=Path, help="optional correction decision log TSV")
    parser.add_argument("-o", "--output", type=Path, required=True, help="output summary TSV")
    parser.add_argument("--markdown", type=Path, help="optional Markdown summary")
    args = parser.parse_args()

    split_rows = read_tsv(args.split_map)
    decisions = read_tsv(args.decision_log) if args.decision_log else []

    decisions_by_seq: dict[str, list[dict[str, str]]] = {}
    for row in decisions:
        decisions_by_seq.setdefault(row.get("sequence_id", ""), []).append(row)

    grouped: dict[str, list[dict[str, str]]] = {}
    for row in split_rows:
        grouped.setdefault(row["source_id"], []).append(row)

    summary = []
    for source_id, rows in sorted(grouped.items()):
        split_rows_for_source = [row for row in rows if row.get("split") == "yes"]
        if not split_rows_for_source:
            continue
        decisions_for_source = decisions_by_seq.get(source_id, [])
        summary.append(
            {
                "source_id": source_id,
                "new_segments": ",".join(row["new_id"] for row in rows),
                "split_count": str(max(0, len(rows) - 1)),
                "source_span": f"{rows[0]['source_start_1based']}-{rows[-1]['source_end_1based']}",
                "decision_edit_ids": ",".join(row.get("edit_id", "") for row in decisions_for_source),
                "final_actions": ",".join(row.get("final_action", "") for row in decisions_for_source),
                "primary_evidence": "; ".join(row.get("primary_evidence", "") for row in decisions_for_source if row.get("primary_evidence", "")),
                "secondary_evidence": "; ".join(row.get("secondary_evidence", "") for row in decisions_for_source if row.get("secondary_evidence", "")),
            }
        )

    write_tsv(summary, args.output)
    if args.markdown:
        write_markdown(summary, args.markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
