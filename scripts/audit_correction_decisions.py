#!/usr/bin/env python3
"""Audit correction decision logs for required evidence fields."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


REQUIRED_COLUMNS = {
    "edit_id",
    "sample_id",
    "assembly_version",
    "sequence_id",
    "start_1based",
    "end_1based",
    "proposed_action",
    "final_action",
    "primary_evidence",
    "secondary_evidence",
    "tools_and_versions",
    "reviewer",
    "review_date",
    "downstream_files_regenerated",
    "notes",
}

ALLOWED_ACTIONS = {
    "retain",
    "break",
    "reverse_complement",
    "reorder",
    "remove",
    "mask",
    "submit_separately",
    "rename_only",
}

DESTRUCTIVE_ACTIONS = {"break", "remove", "reverse_complement", "reorder", "mask"}


def nonempty(row: dict[str, str], key: str) -> bool:
    return bool(row.get(key, "").strip())


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a correction decision log for evidence completeness.")
    parser.add_argument("decision_log", type=Path, help="correction decision log TSV")
    parser.add_argument("-o", "--output", type=Path, help="output TSV; default stdout")
    args = parser.parse_args()

    rows = []
    has_error = False

    with args.decision_log.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"decision log missing required columns: {', '.join(sorted(missing))}")

        seen_edit_ids: set[str] = set()
        for row_number, row in enumerate(reader, start=2):
            edit_id = row.get("edit_id", "").strip()
            issues = []

            if not edit_id:
                issues.append("missing_edit_id")
            elif edit_id in seen_edit_ids:
                issues.append("duplicate_edit_id")
            seen_edit_ids.add(edit_id)

            for key in [
                "sample_id",
                "assembly_version",
                "sequence_id",
                "start_1based",
                "end_1based",
                "proposed_action",
                "final_action",
                "primary_evidence",
                "tools_and_versions",
                "reviewer",
                "review_date",
                "notes",
            ]:
                if not nonempty(row, key):
                    issues.append(f"missing_{key}")

            proposed_action = row.get("proposed_action", "").strip()
            final_action = row.get("final_action", "").strip()
            if proposed_action and proposed_action not in ALLOWED_ACTIONS:
                issues.append("invalid_proposed_action")
            if final_action and final_action not in ALLOWED_ACTIONS:
                issues.append("invalid_final_action")

            for key in ["start_1based", "end_1based"]:
                value = row.get(key, "").strip()
                if value:
                    try:
                        parsed = int(value)
                    except ValueError:
                        issues.append(f"noninteger_{key}")
                    else:
                        if parsed < 1:
                            issues.append(f"invalid_{key}")

            if final_action in DESTRUCTIVE_ACTIONS and not nonempty(row, "secondary_evidence"):
                issues.append("destructive_action_missing_secondary_evidence")

            if final_action == "retain" and not nonempty(row, "secondary_evidence"):
                issues.append("retained_decision_missing_secondary_evidence")

            if final_action == proposed_action and final_action in DESTRUCTIVE_ACTIONS:
                regenerated = row.get("downstream_files_regenerated", "").strip().lower()
                if regenerated not in {"yes", "true", "y", "1", "pending"}:
                    issues.append("destructive_action_requires_regenerated_or_pending_downstream_files")

            status = "pass" if not issues else "review"
            if issues:
                has_error = True
            rows.append(
                {
                    "row": row_number,
                    "edit_id": edit_id,
                    "proposed_action": proposed_action,
                    "final_action": final_action,
                    "status": status,
                    "issues": ",".join(issues),
                }
            )

    output = args.output.open("w", newline="") if args.output else sys.stdout
    with output:
        fieldnames = ["row", "edit_id", "proposed_action", "final_action", "status", "issues"]
        writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
