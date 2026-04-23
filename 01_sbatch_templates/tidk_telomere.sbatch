#!/bin/bash
#SBATCH --job-name=tidk_telomere
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x.%j.out
#SBATCH --error=logs/%x.%j.err

set -euo pipefail

# Purpose:
#   Identify terminal and internal telomeric repeat signal with tidk.
#
# Required variables:
#   FASTA    final assembly FASTA
#   OUTDIR   output directory
#
# Optional variables:
#   MOTIF    telomere motif for known-motif search; default plant motif TTTAGGG
#
# Example:
#   sbatch --export=FASTA=10_scaffolding/sample.final.fa,OUTDIR=12_telomere_centromere/tidk,MOTIF=TTTAGGG 01_sbatch_templates/tidk_telomere.sbatch

: "${FASTA:?Set FASTA to final assembly FASTA}"
: "${OUTDIR:?Set OUTDIR to output directory}"
MOTIF="${MOTIF:-TTTAGGG}"

mkdir -p "${OUTDIR}" logs

if command -v module >/dev/null 2>&1; then
  module load tidk || true
fi

echo "FASTA=${FASTA}"
echo "OUTDIR=${OUTDIR}"
echo "MOTIF=${MOTIF}"
tidk --version || true

# Known-motif search. Confirm the expected motif for the crop lineage before interpreting output.
tidk search \
  --string "${MOTIF}" \
  --output "${OUTDIR}/known_${MOTIF}" \
  "${FASTA}"

# De novo exploration can help when the expected plant motif is absent or uncertain.
# Review de novo results manually before changing the motif used for release summaries.
tidk explore \
  --output "${OUTDIR}/denovo" \
  "${FASTA}"

echo "tidk telomere review complete: ${OUTDIR}"
