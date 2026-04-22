#!/usr/bin/env python3
"""Summarize AGP component and gap structure by assembled object."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


def parse_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize AGP component/gap structure.")
    parser.add_argument("agp", type=Path, help="AGP file")
    parser.add_argument("-o", "--output", type=Path, required=True, help="object-level summary TSV")
    args = parser.parse_args()

    objects: dict[str, dict[str, object]] = {}
    issues: dict[str, list[str]] = defaultdict(list)

    with args.agp.open() as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) != 9:
                object_id = fields[0] if fields else "unknown"
                issues[object_id].append(f"line_{line_number}:column_count_{len(fields)}")
                continue

            object_id, object_beg_raw, object_end_raw, part_raw, component_type = fields[:5]
            object_beg = parse_int(object_beg_raw)
            object_end = parse_int(object_end_raw)
            part_number = parse_int(part_raw)
            if object_id not in objects:
                objects[object_id] = {
                    "object": object_id,
                    "object_length": 0,
                    "part_count": 0,
                    "component_count": 0,
                    "gap_count": 0,
                    "gap_bp": 0,
                    "component_types": Counter(),
                    "gap_types": Counter(),
                    "linkage_evidence": Counter(),
                    "unoriented_components": 0,
                    "last_end": 0,
                    "last_part": 0,
                }

            row = objects[object_id]
            if object_beg is None or object_end is None or part_number is None:
                issues[object_id].append(f"line_{line_number}:noninteger_coordinate_or_part")
                continue
            if object_beg != int(row["last_end"]) + 1:
                issues[object_id].append(f"line_{line_number}:nonsequential_object_coordinates")
            if part_number != int(row["last_part"]) + 1:
                issues[object_id].append(f"line_{line_number}:nonsequential_part_number")
            if object_end < object_beg:
                issues[object_id].append(f"line_{line_number}:end_before_start")

            row["object_length"] = max(int(row["object_length"]), object_end)
            row["part_count"] = int(row["part_count"]) + 1
            row["last_end"] = object_end
            row["last_part"] = part_number

            if component_type in {"N", "U"}:
                gap_length = parse_int(fields[5])
                row["gap_count"] = int(row["gap_count"]) + 1
                row["gap_bp"] = int(row["gap_bp"]) + (gap_length or 0)
                row["gap_types"][fields[6]] += 1
                row["linkage_evidence"][fields[8]] += 1
                if component_type == "U" and gap_length != 100:
                    issues[object_id].append(f"line_{line_number}:unknown_gap_not_100bp")
            else:
                row["component_count"] = int(row["component_count"]) + 1
                row["component_types"][component_type] += 1
                if fields[8] in {"0", "?"}:
                    row["unoriented_components"] = int(row["unoriented_components"]) + 1

    with args.output.open("w", newline="") as handle:
        fieldnames = [
            "object",
            "object_length",
            "part_count",
            "component_count",
            "gap_count",
            "gap_bp",
            "component_types",
            "gap_types",
            "linkage_evidence",
            "unoriented_components",
            "issues",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for object_id in sorted(objects):
            row = objects[object_id]
            writer.writerow(
                {
                    "object": object_id,
                    "object_length": row["object_length"],
                    "part_count": row["part_count"],
                    "component_count": row["component_count"],
                    "gap_count": row["gap_count"],
                    "gap_bp": row["gap_bp"],
                    "component_types": ";".join(f"{k}:{v}" for k, v in sorted(row["component_types"].items())),
                    "gap_types": ";".join(f"{k}:{v}" for k, v in sorted(row["gap_types"].items())),
                    "linkage_evidence": ";".join(f"{k}:{v}" for k, v in sorted(row["linkage_evidence"].items())),
                    "unoriented_components": row["unoriented_components"],
                    "issues": ";".join(issues.get(object_id, [])) or "pass",
                }
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
