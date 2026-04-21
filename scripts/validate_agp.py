#!/usr/bin/env python3
"""Validate basic AGP 2.0 structure and coordinate consistency."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


COMPONENT_TYPES = {"A", "D", "F", "G", "O", "P", "W"}
GAP_TYPES = {"N", "U"}
VALID_GAP_KINDS = {
    "scaffold",
    "contig",
    "centromere",
    "short_arm",
    "heterochromatin",
    "telomere",
    "repeat",
    "clone",
    "fragment",
    "contamination",
}
VALID_LINKAGE = {"yes", "no"}


def parse_int(value: str):
    try:
        return int(value)
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate basic AGP columns, coordinates, and component/gap rows.")
    parser.add_argument("agp", type=Path, help="input AGP file")
    parser.add_argument("-o", "--output", type=Path, help="optional TSV report path")
    args = parser.parse_args()

    issues = []
    previous_by_object = {}
    row_count = 0

    with args.agp.open() as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            row_count += 1
            fields = stripped.split("\t")
            if len(fields) != 9:
                issues.append(("ERROR", "column_count", str(line_number), "", f"expected 9 columns, found {len(fields)}"))
                continue

            obj, obj_start_s, obj_end_s, part_s, row_type = fields[:5]
            obj_start = parse_int(obj_start_s)
            obj_end = parse_int(obj_end_s)
            part = parse_int(part_s)

            if obj_start is None or obj_end is None or part is None:
                issues.append(("ERROR", "non_integer_coordinate", str(line_number), obj, "object start/end and part number must be integers"))
                continue
            if obj_start < 1 or obj_end < obj_start:
                issues.append(("ERROR", "invalid_object_interval", str(line_number), obj, "object coordinates must be 1-based and start <= end"))

            previous = previous_by_object.get(obj)
            if previous:
                previous_end, previous_part = previous
                if obj_start != previous_end + 1:
                    issues.append(("ERROR", "non_contiguous_object", str(line_number), obj, f"object start {obj_start} does not follow previous end {previous_end}"))
                if part != previous_part + 1:
                    issues.append(("ERROR", "part_number", str(line_number), obj, f"part {part} does not follow previous part {previous_part}"))
            elif obj_start != 1:
                issues.append(("WARN", "object_does_not_start_at_1", str(line_number), obj, "first row for object should usually start at 1"))
            previous_by_object[obj] = (obj_end, part)

            if row_type in COMPONENT_TYPES:
                comp_start = parse_int(fields[6])
                comp_end = parse_int(fields[7])
                orientation = fields[8]
                if not fields[5]:
                    issues.append(("ERROR", "missing_component_id", str(line_number), obj, "component row requires component ID"))
                if comp_start is None or comp_end is None or comp_start < 1 or comp_end < comp_start:
                    issues.append(("ERROR", "invalid_component_interval", str(line_number), obj, "component coordinates must be valid integers"))
                if orientation not in {"+", "-", "?", "0", "na"}:
                    issues.append(("ERROR", "invalid_orientation", str(line_number), obj, f"unexpected orientation {orientation}"))
                if comp_start is not None and comp_end is not None:
                    object_span = obj_end - obj_start + 1
                    component_span = comp_end - comp_start + 1
                    if object_span != component_span:
                        issues.append(("ERROR", "span_mismatch", str(line_number), obj, f"object span {object_span} != component span {component_span}"))
            elif row_type in GAP_TYPES:
                gap_length = parse_int(fields[5])
                gap_kind = fields[6]
                linkage = fields[7]
                if gap_length is None or gap_length < 1:
                    issues.append(("ERROR", "invalid_gap_length", str(line_number), obj, "gap length must be a positive integer"))
                if gap_kind not in VALID_GAP_KINDS:
                    issues.append(("WARN", "unusual_gap_type", str(line_number), obj, f"gap type {gap_kind} is not a common AGP gap type"))
                if linkage not in VALID_LINKAGE:
                    issues.append(("ERROR", "invalid_linkage", str(line_number), obj, "linkage must be yes or no"))
                if gap_length is not None and (obj_end - obj_start + 1) != gap_length:
                    issues.append(("ERROR", "gap_span_mismatch", str(line_number), obj, "object span does not match gap length"))
            else:
                issues.append(("ERROR", "invalid_row_type", str(line_number), obj, f"unexpected row type {row_type}"))

    summary = [
        ("INFO", "rows_checked", "", "", str(row_count)),
        ("INFO", "objects_checked", "", "", str(len(previous_by_object))),
    ]
    rows = summary + issues

    handle = args.output.open("w") if args.output else sys.stdout
    with handle:
        handle.write("level\tcheck\tline\tobject\tmessage\n")
        for row in rows:
            handle.write("\t".join(row) + "\n")

    return 1 if any(level == "ERROR" for level, *_ in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())

