#!/usr/bin/env python3
"""Audit public-facing release metadata for internal consistency."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


REQUIRED_CFF_KEYS = [
    "cff-version",
    "message",
    "title",
    "version",
    "date-released",
    "repository-code",
    "url",
    "license",
    "authors",
    "abstract",
    "keywords",
]

REQUIRED_PUBLIC_FILES = [
    "README.md",
    "VERSION",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CITATION.cff",
    "LICENSE",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/docs_improvement.md",
    ".github/ISSUE_TEMPLATE/workflow_tool_suggestion.md",
    ".github/pull_request_template.md",
    "docs/release/v0.5_review_checklist.md",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text()


def simple_cff_values(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^([A-Za-z0-9_.-]+):\s*(.*)$", line)
        if not match:
            continue
        key, raw_value = match.groups()
        values[key] = raw_value.strip().strip('"')
    return values


def add_row(rows: list[dict[str, str]], check: str, status: str, detail: str) -> None:
    rows.append({"check": check, "status": status, "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser(description="Check public release metadata consistency.")
    parser.add_argument("-o", "--output", type=Path, help="optional TSV output")
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    failed = False

    for path_text in REQUIRED_PUBLIC_FILES:
        path = Path(path_text)
        ok = path.exists() and path.stat().st_size > 0
        detail = "present" if ok else "missing or empty"
        add_row(rows, f"required_file:{path_text}", "pass" if ok else "fail", detail)
        failed = failed or not ok

    version_path = Path("VERSION")
    citation_path = Path("CITATION.cff")
    license_path = Path("LICENSE")
    readme_path = Path("README.md")

    if version_path.exists() and citation_path.exists():
        version = read_text(version_path).strip()
        cff_text = read_text(citation_path)
        cff = simple_cff_values(cff_text)

        for key in REQUIRED_CFF_KEYS:
            ok = key in cff_text
            add_row(rows, f"citation_key:{key}", "pass" if ok else "fail", "present" if ok else "missing")
            failed = failed or not ok

        cff_version = cff.get("version", "")
        ok = cff_version == version
        add_row(rows, "citation_version_matches_VERSION", "pass" if ok else "fail", f"CITATION={cff_version}; VERSION={version}")
        failed = failed or not ok

        date_value = cff.get("date-released", "")
        ok = bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_value))
        add_row(rows, "citation_date_format", "pass" if ok else "fail", date_value or "missing")
        failed = failed or not ok

        repo_url = cff.get("repository-code", "")
        ok = repo_url.startswith("https://github.com/USDA-ARS-GBRU/HiFi-Genome-Assembly")
        add_row(rows, "citation_repository_url", "pass" if ok else "fail", repo_url or "missing")
        failed = failed or not ok

    if citation_path.exists() and license_path.exists():
        cff = simple_cff_values(read_text(citation_path))
        license_text = read_text(license_path)
        first_line = license_text.splitlines()[0] if license_text else "missing"
        cff_license = cff.get("license", "")
        ok = cff_license == "MIT" and first_line == "MIT License"
        add_row(rows, "license_consistency", "pass" if ok else "fail", f"CITATION={cff_license}; LICENSE first line={first_line}")
        failed = failed or not ok

    if readme_path.exists():
        readme = read_text(readme_path)
        for expected in ["CITATION.cff", "LICENSE", "CONTRIBUTING.md", "docs/status.md"]:
            ok = expected in readme
            add_row(rows, f"readme_mentions:{expected}", "pass" if ok else "fail", "mentioned" if ok else "not mentioned")
            failed = failed or not ok

    handle = args.output.open("w", newline="") if args.output else sys.stdout
    with handle:
        fieldnames = ["check", "status", "detail"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
