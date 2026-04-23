#!/bin/bash
#SBATCH --job-name=quartet_telo_centro
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=24:00:00
#SBATCH --output=logs/%x.%j.out
#SBATCH --error=logs/%x.%j.err

set -euo pipefail

# Purpose:
#   Run quarTeT telomere and centromere exploration for chromosome-completeness review.
#
# Required variables:
#   FASTA    final assembly FASTA
#   OUTDIR   output directory
#
# Optional variables:
#   CLAD     quarTeT telomere clade option; default plant
#
# Example:
#   sbatch --export=FASTA=10_scaffolding/sample.final.fa,OUTDIR=12_telomere_centromere/quartet,CLAD=plant 01_sbatch_templates/quartet_telomere_centromere.sbatch

: "${FASTA:?Set FASTA to final assembly FASTA}"
: "${OUTDIR:?Set OUTDIR to output directory}"
CLAD="${CLAD:-plant}"

mkdir -p "${OUTDIR}" logs

if command -v module >/dev/null 2>&1; then
  module load quartet || true
fi

echo "FASTA=${FASTA}"
echo "OUTDIR=${OUTDIR}"
echo "CLAD=${CLAD}"
quartet.py --help | head -n 5 || true

quartet.py TeloExplorer \
  -i "${FASTA}" \
  -c "${CLAD}" \
  -o "${OUTDIR}/teloexplorer"

quartet.py CentroMiner \
  -i "${FASTA}" \
  -o "${OUTDIR}/centrominer"

echo "quarTeT telomere/centromere review complete: ${OUTDIR}"
