#!/usr/bin/env python3
"""Run basic release bundle checks for FASTA, optional AGP, and manifest."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run_check(command: list[str]) -> int:
    print("Running:", " ".join(command), file=sys.stderr)
    return subprocess.run(command, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run FASTA, AGP, and manifest audits for a release bundle.")
    parser.add_argument("--fasta", required=True, type=Path, help="final assembly FASTA")
    parser.add_argument("--manifest", required=True, type=Path, help="release manifest TSV")
    parser.add_argument("--agp", type=Path, help="optional AGP file")
    parser.add_argument("--min-length", type=int, default=200)
    parser.add_argument("--out-dir", type=Path, default=Path("15_release/validation"))
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    script_dir = Path(__file__).resolve().parent

    checks = [
        [
            sys.executable,
            str(script_dir / "validate_fasta.py"),
            str(args.fasta),
            "--min-length",
            str(args.min_length),
            "-o",
            str(args.out_dir / "fasta_validation.tsv"),
        ],
        [
            sys.executable,
            str(script_dir / "audit_fasta_headers.py"),
            str(args.fasta),
            "-o",
            str(args.out_dir / "fasta_header_audit.tsv"),
        ],
        [
            sys.executable,
            str(script_dir / "audit_release_manifest.py"),
            str(args.manifest),
            "--base-dir",
            ".",
            "-o",
            str(args.out_dir / "manifest_audit.tsv"),
        ],
    ]

    if args.agp:
        checks.append(
            [
                sys.executable,
                str(script_dir / "validate_agp.py"),
                str(args.agp),
                "-o",
                str(args.out_dir / "agp_validation.tsv"),
            ]
        )

    exit_code = 0
    for command in checks:
        exit_code = max(exit_code, run_check(command))

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
