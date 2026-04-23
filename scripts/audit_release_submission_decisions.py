#!/usr/bin/env python3
"""Audit release submission decision tables for contradictions and missing readiness."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


REQUIRED_COLUMNS = [
    "package_id",
    "sample_id",
    "assembly_version",
    "assembly_level",
    "submission_target",
    "assembly_fasta",
    "agp_included",
    "annotation_package",
    "bioproject_status",
    "biosample_status",
    "sra_status",
    "release_action",
    "primary_strength",
    "primary_concern",
    "reviewer",
    "notes",
]

ALLOWED_ASSEMBLY_LEVELS = {"contig", "scaffold", "chromosome"}
ALLOWED_SUBMISSION_TARGETS = {
    "assembly_only",
    "annotated_genome",
    "community_database",
    "combined_release",
}
ALLOWED_YES_NO_NA = {"yes", "no", "not_applicable"}
ALLOWED_ANNOTATION = {"yes", "no", "planned"}
ALLOWED_STATUS = {"ready", "pending", "not_applicable"}
ALLOWED_ACTIONS = {"use_for_submission", "comparison_only", "hold", "needs_review"}


def add_issue(
    issues: list[dict[str, str]],
    row_number: int,
    package_id: str,
    severity: str,
    issue: str,
    detail: str,
) -> None:
    issues.append(
        {
            "row_number": str(row_number),
            "package_id": package_id,
            "severity": severity,
            "issue": issue,
            "detail": detail,
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit release submission decision TSV.")
    parser.add_argument("table", type=Path, help="release submission decision TSV")
    parser.add_argument("-o", "--output", type=Path, help="optional TSV issue output")
    args = parser.parse_args()

    issues: list[dict[str, str]] = []
    release_counts: dict[tuple[str, str, str], int] = defaultdict(int)

    with args.table.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = reader.fieldnames or []
        missing = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
        for column in missing:
            add_issue(issues, 0, "", "error", "missing_column", column)

        if not missing:
            for row_number, row in enumerate(reader, start=2):
                package_id = row.get("package_id", "")
                sample_id = row.get("sample_id", "")
                assembly_version = row.get("assembly_version", "")
                submission_target = row.get("submission_target", "")
                key = (sample_id, assembly_version, submission_target)

                for column in REQUIRED_COLUMNS:
                    if not row.get(column, "").strip():
                        add_issue(issues, row_number, package_id, "error", "missing_value", f"{column} is empty")

                assembly_level = row.get("assembly_level", "")
                agp_included = row.get("agp_included", "")
                annotation_package = row.get("annotation_package", "")
                bioproject_status = row.get("bioproject_status", "")
                biosample_status = row.get("biosample_status", "")
                sra_status = row.get("sra_status", "")
                release_action = row.get("release_action", "")

                if assembly_level not in ALLOWED_ASSEMBLY_LEVELS:
                    add_issue(issues, row_number, package_id, "error", "invalid_assembly_level", assembly_level)
                if submission_target not in ALLOWED_SUBMISSION_TARGETS:
                    add_issue(issues, row_number, package_id, "error", "invalid_submission_target", submission_target)
                if agp_included not in ALLOWED_YES_NO_NA:
                    add_issue(issues, row_number, package_id, "error", "invalid_agp_included", agp_included)
                if annotation_package not in ALLOWED_ANNOTATION:
                    add_issue(issues, row_number, package_id, "error", "invalid_annotation_package", annotation_package)
                if bioproject_status not in ALLOWED_STATUS:
                    add_issue(issues, row_number, package_id, "error", "invalid_bioproject_status", bioproject_status)
                if biosample_status not in ALLOWED_STATUS:
                    add_issue(issues, row_number, package_id, "error", "invalid_biosample_status", biosample_status)
                if sra_status not in ALLOWED_STATUS:
                    add_issue(issues, row_number, package_id, "error", "invalid_sra_status", sra_status)
                if release_action not in ALLOWED_ACTIONS:
                    add_issue(issues, row_number, package_id, "error", "invalid_release_action", release_action)

                if release_action == "use_for_submission":
                    release_counts[key] += 1

                if release_action == "use_for_submission" and assembly_level in {"scaffold", "chromosome"} and agp_included != "yes":
                    add_issue(
                        issues,
                        row_number,
                        package_id,
                        "error",
                        "scaffold_or_chromosome_release_missing_agp",
                        f"assembly_level={assembly_level}; agp_included={agp_included}",
                    )

                if release_action == "use_for_submission" and submission_target in {"annotated_genome", "combined_release"} and annotation_package != "yes":
                    add_issue(
                        issues,
                        row_number,
                        package_id,
                        "error",
                        "annotated_release_missing_annotation_package",
                        f"submission_target={submission_target}; annotation_package={annotation_package}",
                    )

                if release_action == "use_for_submission" and bioproject_status != "ready":
                    add_issue(
                        issues,
                        row_number,
                        package_id,
                        "error",
                        "submission_package_bioproject_not_ready",
                        bioproject_status,
                    )

                if release_action == "use_for_submission" and biosample_status != "ready":
                    add_issue(
                        issues,
                        row_number,
                        package_id,
                        "error",
                        "submission_package_biosample_not_ready",
                        biosample_status,
                    )

                if release_action == "use_for_submission" and sra_status == "not_applicable":
                    add_issue(
                        issues,
                        row_number,
                        package_id,
                        "error",
                        "submission_package_sra_not_applicable",
                        "PacBio HiFi crop genome release should track read submission readiness",
                    )

                if release_action == "use_for_submission" and sra_status == "pending":
                    add_issue(
                        issues,
                        row_number,
                        package_id,
                        "warning",
                        "submission_package_sra_pending",
                        "package may still be acceptable, but accession tracking should note pending reads",
                    )

                if release_action != "use_for_submission" and annotation_package == "yes" and submission_target == "assembly_only":
                    add_issue(
                        issues,
                        row_number,
                        package_id,
                        "warning",
                        "annotation_package_present_for_assembly_only_candidate",
                        "verify whether this should instead be tracked as annotated_genome or combined_release",
                    )

    for key, count in release_counts.items():
        if count > 1:
            add_issue(
                issues,
                0,
                "",
                "error",
                "multiple_submission_packages_selected",
                f"sample_id={key[0]}; assembly_version={key[1]}; submission_target={key[2]}; count={count}",
            )

    output = args.output.open("w", newline="") if args.output else sys.stdout
    with output:
        fieldnames = ["row_number", "package_id", "severity", "issue", "detail"]
        writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(issues)

    return 1 if any(issue["severity"] == "error" for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
