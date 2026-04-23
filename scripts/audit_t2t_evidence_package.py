#!/usr/bin/env python3
"""Audit a T2T completeness evidence table for missing support and overclaims."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


REQUIRED_COLUMNS = [
    "sample_id",
    "assembly_version",
    "sequence_id",
    "length_bp",
    "gap_count",
    "agp_gap_count",
    "left_telomere_status",
    "right_telomere_status",
    "internal_telomere_status",
    "centromere_status",
    "centromere_evidence",
    "hic_status",
    "dotplot_status",
    "difficult_repeat_status",
    "claim_class",
    "review_notes",
]

TELOMERE_STATUSES = {
    "terminal_supported",
    "terminal_missing",
    "terminal_ambiguous",
    "wrong_motif_possible",
    "not_reviewed",
}

INTERNAL_TELOMERE_STATUSES = {
    "none_detected",
    "candidate_interstitial_repeat",
    "possible_misjoin",
    "needs_review",
    "not_reviewed",
}

CENTROMERE_STATUSES = {
    "high_confidence",
    "moderate_confidence",
    "low_confidence",
    "not_detected",
    "not_reviewed",
}

CLAIM_CLASSES = {
    "chromosome_scale",
    "near_gapless",
    "candidate_t2t_chromosome",
    "unresolved",
}


def as_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def add_issue(issues: list[dict[str, str]], row_number: int, sequence_id: str, severity: str, issue: str, detail: str) -> None:
    issues.append(
        {
            "row_number": str(row_number),
            "sequence_id": sequence_id,
            "severity": severity,
            "issue": issue,
            "detail": detail,
        }
    )


def audit_row(row: dict[str, str], row_number: int, issues: list[dict[str, str]]) -> None:
    sequence_id = row.get("sequence_id", "")

    for column in REQUIRED_COLUMNS:
        if not row.get(column, "").strip():
            add_issue(issues, row_number, sequence_id, "error", "missing_value", f"{column} is empty")

    length_bp = as_int(row.get("length_bp", ""))
    gap_count = as_int(row.get("gap_count", ""))
    agp_gap_count = as_int(row.get("agp_gap_count", ""))

    if length_bp is None or length_bp <= 0:
        add_issue(issues, row_number, sequence_id, "error", "invalid_length_bp", row.get("length_bp", ""))
    if gap_count is None or gap_count < 0:
        add_issue(issues, row_number, sequence_id, "error", "invalid_gap_count", row.get("gap_count", ""))
    if agp_gap_count is None or agp_gap_count < 0:
        add_issue(issues, row_number, sequence_id, "error", "invalid_agp_gap_count", row.get("agp_gap_count", ""))

    left_telomere = row.get("left_telomere_status", "")
    right_telomere = row.get("right_telomere_status", "")
    internal_telomere = row.get("internal_telomere_status", "")
    centromere = row.get("centromere_status", "")
    claim = row.get("claim_class", "")

    if left_telomere not in TELOMERE_STATUSES:
        add_issue(issues, row_number, sequence_id, "error", "invalid_left_telomere_status", left_telomere)
    if right_telomere not in TELOMERE_STATUSES:
        add_issue(issues, row_number, sequence_id, "error", "invalid_right_telomere_status", right_telomere)
    if internal_telomere not in INTERNAL_TELOMERE_STATUSES:
        add_issue(issues, row_number, sequence_id, "error", "invalid_internal_telomere_status", internal_telomere)
    if centromere not in CENTROMERE_STATUSES:
        add_issue(issues, row_number, sequence_id, "error", "invalid_centromere_status", centromere)
    if claim not in CLAIM_CLASSES:
        add_issue(issues, row_number, sequence_id, "error", "invalid_claim_class", claim)

    if claim == "candidate_t2t_chromosome":
        if gap_count != 0 or agp_gap_count != 0:
            add_issue(issues, row_number, sequence_id, "error", "candidate_t2t_has_gaps", f"gap_count={gap_count}; agp_gap_count={agp_gap_count}")
        if left_telomere != "terminal_supported" or right_telomere != "terminal_supported":
            add_issue(issues, row_number, sequence_id, "error", "candidate_t2t_missing_terminal_telomere", f"left={left_telomere}; right={right_telomere}")
        if internal_telomere != "none_detected":
            add_issue(issues, row_number, sequence_id, "error", "candidate_t2t_internal_telomere_review", internal_telomere)
        if centromere not in {"high_confidence", "moderate_confidence"}:
            add_issue(issues, row_number, sequence_id, "error", "candidate_t2t_weak_centromere", centromere)
        if "review" in row.get("hic_status", "").lower() or "review" in row.get("dotplot_status", "").lower():
            add_issue(issues, row_number, sequence_id, "error", "candidate_t2t_unresolved_structure_review", f"hic={row.get('hic_status', '')}; dotplot={row.get('dotplot_status', '')}")

    if claim == "near_gapless" and gap_count and gap_count > 0:
        add_issue(issues, row_number, sequence_id, "warning", "near_gapless_retains_gaps", f"gap_count={gap_count}")
    if claim == "chromosome_scale" and left_telomere == "terminal_supported" and right_telomere == "terminal_supported" and gap_count == 0:
        add_issue(issues, row_number, sequence_id, "info", "possible_higher_completeness_class", "review whether near_gapless or candidate_t2t_chromosome is appropriate")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a T2T completeness evidence TSV.")
    parser.add_argument("table", type=Path, help="T2T completeness evidence TSV")
    parser.add_argument("-o", "--output", type=Path, help="issue TSV output")
    args = parser.parse_args()

    issues: list[dict[str, str]] = []
    with args.table.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        for column in missing_columns:
            add_issue(issues, 0, "", "error", "missing_column", column)
        if not missing_columns:
            for row_number, row in enumerate(reader, start=2):
                audit_row(row, row_number, issues)

    output = args.output.open("w", newline="") if args.output else sys.stdout
    with output:
        fieldnames = ["row_number", "sequence_id", "severity", "issue", "detail"]
        writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(issues)

    return 1 if any(issue["severity"] == "error" for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
