#!/usr/bin/env python3
"""Create a Markdown post-correction report from curation TSV outputs."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path


def read_tsv(path: Path | None) -> list[dict[str, str]]:
    if path is None:
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def link(path: Path | None) -> str:
    return str(path) if path else "not provided"


def write_table(handle, headers: list[str], rows: list[dict[str, str]]) -> None:
    handle.write("| " + " | ".join(headers) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
    if not rows:
        handle.write("| " + " | ".join(["none"] + [""] * (len(headers) - 1)) + " |\n")
        return
    for row in rows:
        handle.write("| " + " | ".join(row.get(header, "") for header in headers) + " |\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Markdown report for an assembly correction round.")
    parser.add_argument("--sample", required=True, help="sample or assembly name")
    parser.add_argument("--version", default="0.5.0-dev", help="protocol or assembly version")
    parser.add_argument("--decision-log", type=Path, required=True, help="correction decision log TSV")
    parser.add_argument("--decision-audit", type=Path, help="audit_correction_decisions.py output TSV")
    parser.add_argument("--correction-summary", type=Path, help="summarize_corrections.py output TSV")
    parser.add_argument("--split-map", type=Path, help="split_fasta_at_breaks.py map TSV")
    parser.add_argument("--fasta-comparison", type=Path, help="compare_fasta_stats.py output TSV")
    parser.add_argument("--break-validation", type=Path, help="validate_breaks.py output TSV")
    parser.add_argument("--fasta-validation", type=Path, help="validate_fasta.py output TSV")
    parser.add_argument("--agp-validation", type=Path, help="validate_agp.py output TSV")
    parser.add_argument("-o", "--output", type=Path, required=True, help="output Markdown report")
    args = parser.parse_args()

    decisions = read_tsv(args.decision_log)
    audit_rows = read_tsv(args.decision_audit)
    correction_rows = read_tsv(args.correction_summary)
    fasta_comparison_rows = read_tsv(args.fasta_comparison)
    action_counts = Counter(row.get("final_action", "") for row in decisions)
    accepted = [row for row in decisions if row.get("proposed_action") == row.get("final_action") and row.get("final_action") != "retain"]
    rejected = [row for row in decisions if row.get("final_action") == "retain"]
    audit_status = "pass" if audit_rows and all(row.get("status") == "pass" for row in audit_rows) else "review"
    if not audit_rows:
        audit_status = "not provided"

    with args.output.open("w") as handle:
        handle.write("# Post-Correction Report\n\n")
        handle.write("## Assembly and Version\n\n")
        handle.write(f"- sample_id: {args.sample}\n")
        handle.write(f"- roadmap_or_assembly_version: {args.version}\n")
        handle.write(f"- report_date: {date.today().isoformat()}\n")
        handle.write(f"- decision_log: {args.decision_log}\n")
        handle.write(f"- decision_audit_status: {audit_status}\n\n")

        handle.write("## Correction Summary\n\n")
        handle.write(f"- number_of_candidate_edits: {len(decisions)}\n")
        handle.write(f"- number_accepted: {len(accepted)}\n")
        handle.write(f"- number_rejected_or_retained: {len(rejected)}\n")
        for action, count in sorted(action_counts.items()):
            handle.write(f"- final_action_{action or 'blank'}: {count}\n")
        handle.write("\n")

        handle.write("## Accepted Edits\n\n")
        write_table(handle, ["edit_id", "sequence_id", "final_action", "primary_evidence", "secondary_evidence"], accepted)
        handle.write("\n")

        handle.write("## Rejected or Retained Candidate Edits\n\n")
        write_table(handle, ["edit_id", "sequence_id", "proposed_action", "final_action", "notes"], rejected)
        handle.write("\n")

        handle.write("## Split/Correction Products\n\n")
        handle.write(f"- split_map: {link(args.split_map)}\n")
        handle.write(f"- correction_summary: {link(args.correction_summary)}\n")
        handle.write(f"- fasta_comparison: {link(args.fasta_comparison)}\n")
        if correction_rows:
            handle.write("\n")
            write_table(handle, ["source_id", "new_segments", "split_count", "primary_evidence", "secondary_evidence"], correction_rows)
        handle.write("\n")

        handle.write("## FASTA Stat Changes\n\n")
        write_table(handle, ["metric", "before", "after", "delta"], fasta_comparison_rows)
        handle.write("\n")

        handle.write("## Validation Files\n\n")
        handle.write(f"- break_validation: {link(args.break_validation)}\n")
        handle.write(f"- fasta_validation: {link(args.fasta_validation)}\n")
        handle.write(f"- agp_validation: {link(args.agp_validation)}\n\n")

        handle.write("## Release Decision\n\n")
        handle.write("```text\n")
        handle.write("ready_for_release: review_required\n")
        handle.write("blocking_items: review validation outputs and regenerated downstream files\n")
        handle.write("nonblocking_caveats:\n")
        handle.write("next_review_date:\n")
        handle.write("```\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
