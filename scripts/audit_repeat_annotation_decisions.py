#!/usr/bin/env python3
"""Audit repeat annotation decision tables for missing support and contradictions."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


REQUIRED_COLUMNS = [
    "decision_id",
    "sample_id",
    "assembly_version",
    "candidate_method",
    "candidate_outputs",
    "masked_percent",
    "unclassified_percent",
    "primary_strength",
    "primary_concern",
    "final_action",
    "gene_annotation_input",
    "reviewer",
    "notes",
]

ALLOWED_ACTIONS = {"use_for_release", "comparison_only", "reject", "needs_review"}
ALLOWED_GENE_INPUT = {"yes", "no"}


def as_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def add_issue(
    issues: list[dict[str, str]],
    row_number: int,
    decision_id: str,
    severity: str,
    issue: str,
    detail: str,
) -> None:
    issues.append(
        {
            "row_number": str(row_number),
            "decision_id": decision_id,
            "severity": severity,
            "issue": issue,
            "detail": detail,
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit repeat annotation decision TSV.")
    parser.add_argument("table", type=Path, help="repeat annotation decision TSV")
    parser.add_argument("-o", "--output", type=Path, help="optional TSV issue output")
    args = parser.parse_args()

    issues: list[dict[str, str]] = []
    release_counts: dict[tuple[str, str], int] = defaultdict(int)
    gene_input_counts: dict[tuple[str, str], int] = defaultdict(int)

    with args.table.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = reader.fieldnames or []
        missing = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
        for column in missing:
            add_issue(issues, 0, "", "error", "missing_column", column)
        if not missing:
            for row_number, row in enumerate(reader, start=2):
                decision_id = row.get("decision_id", "")
                sample_id = row.get("sample_id", "")
                assembly_version = row.get("assembly_version", "")
                key = (sample_id, assembly_version)

                for column in REQUIRED_COLUMNS:
                    if not row.get(column, "").strip():
                        add_issue(issues, row_number, decision_id, "error", "missing_value", f"{column} is empty")

                action = row.get("final_action", "")
                gene_input = row.get("gene_annotation_input", "")
                masked = as_float(row.get("masked_percent", ""))
                unclassified = as_float(row.get("unclassified_percent", ""))

                if action not in ALLOWED_ACTIONS:
                    add_issue(issues, row_number, decision_id, "error", "invalid_final_action", action)
                if gene_input not in ALLOWED_GENE_INPUT:
                    add_issue(issues, row_number, decision_id, "error", "invalid_gene_annotation_input", gene_input)
                if masked is None or masked < 0 or masked > 100:
                    add_issue(issues, row_number, decision_id, "error", "invalid_masked_percent", row.get("masked_percent", ""))
                if unclassified is None or unclassified < 0 or unclassified > 100:
                    add_issue(issues, row_number, decision_id, "error", "invalid_unclassified_percent", row.get("unclassified_percent", ""))

                if action == "use_for_release":
                    release_counts[key] += 1
                if gene_input == "yes":
                    gene_input_counts[key] += 1
                    if action != "use_for_release":
                        add_issue(
                            issues,
                            row_number,
                            decision_id,
                            "error",
                            "gene_annotation_input_without_release_action",
                            f"final_action={action}",
                        )

                if action == "use_for_release" and gene_input != "yes":
                    add_issue(
                        issues,
                        row_number,
                        decision_id,
                        "warning",
                        "release_mask_not_marked_for_gene_annotation",
                        "release candidate is not flagged as gene annotation input",
                    )

    for key, count in release_counts.items():
        if count > 1:
            add_issue(issues, 0, "", "error", "multiple_release_masks", f"sample_id={key[0]}; assembly_version={key[1]}; count={count}")
    for key, count in gene_input_counts.items():
        if count > 1:
            add_issue(issues, 0, "", "error", "multiple_gene_annotation_inputs", f"sample_id={key[0]}; assembly_version={key[1]}; count={count}")

    output = args.output.open("w", newline="") if args.output else sys.stdout
    with output:
        fieldnames = ["row_number", "decision_id", "severity", "issue", "detail"]
        writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(issues)

    return 1 if any(issue["severity"] == "error" for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
