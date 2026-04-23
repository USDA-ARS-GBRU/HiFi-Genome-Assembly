#!/usr/bin/env python3
"""Report focused documentation coverage for README workflow steps."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED = [
    ("Step 0", "Choose Assembly Strategy", "docs/assembly/index.md"),
    ("Step 1", "Prepare Reads", "docs/assembly/prepare_reads.md"),
    ("Step 2", "Estimate Genome Properties", "docs/assembly/genome_profiling.md"),
    ("Step 3", "Assemble with hifiasm", "docs/assembly/hifiasm.md"),
    ("Step 4", "Convert and Organize hifiasm Outputs", "docs/assembly/hifiasm.md"),
    ("Step 5", "Assembly Statistics", "docs/qc/assembly_metrics.md"),
    ("Step 6", "Reference and Self Alignment Dotplots", "docs/qc/dotplots.md"),
    ("Step 7", "Haplotigs, Duplications, and Ploidy", "docs/assembly/genome_profiling.md"),
    ("Step 8", "Misassembly Review and Correction", "docs/curation/index.md"),
    ("Step 9", "Chromosome-Scale Scaffolding", "docs/scaffolding/hic_scaffolding.md"),
    ("Step 9B", "Gap Filling", "docs/gap_filling_workflow.md"),
    ("Step 10", "Telomeres, Centromeres, and Gap Status", "docs/t2t_readiness_checklist.md"),
    ("Step 11", "Contamination Screening", "docs/qc/contamination.md"),
    ("Step 12", "Repeat Annotation and Masking", "docs/annotation/repeats.md"),
    ("Step 13", "Gene Annotation", "docs/annotation/genes.md"),
    ("Step 14", "Final Quality Metrics", "docs/qc/assembly_metrics.md"),
    ("Step 15", "NCBI and Community Database Release", "docs/release/ncbi_submission.md"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check focused docs coverage for README steps.")
    parser.add_argument("-o", "--output", type=Path, required=True, help="output TSV")
    args = parser.parse_args()

    missing = False
    with args.output.open("w", newline="") as handle:
        fieldnames = ["step", "title", "doc", "exists", "status"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for step, title, doc in REQUIRED:
            exists = Path(doc).exists()
            if not exists:
                missing = True
            writer.writerow(
                {
                    "step": step,
                    "title": title,
                    "doc": doc,
                    "exists": "yes" if exists else "no",
                    "status": "covered" if exists else "missing",
                }
            )
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
