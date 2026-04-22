#!/bin/bash
#SBATCH -J post_correct
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --mem=64G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/post_correction_validation_%j.out
#SBATCH -e 00_log/post_correction_validation_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

: "${corrected_fasta:?Set corrected_fasta=07_assemblies/sample.corrected.fa}"
: "${sample:?Set sample=SampleID}"

original_fasta="${original_fasta:-}"
breaks="${breaks:-}"
split_map="${split_map:-}"
decision_log="${decision_log:-}"
agp="${agp:-}"
reference="${reference:-}"
preset="${preset:-asm20}"
outdir="${outdir:-15_release/post_correction_validation/${sample}}"

mkdir -p "${outdir}"

scripts/validate_fasta.py \
  "${corrected_fasta}" \
  --min-length "${min_length:-200}" \
  -o "${outdir}/${sample}.corrected.fasta_validation.tsv"

scripts/audit_fasta_headers.py \
  "${corrected_fasta}" \
  -o "${outdir}/${sample}.corrected.header_audit.tsv" || true

if [ -n "${original_fasta}" ] && [ -n "${breaks}" ]; then
  scripts/validate_breaks.py \
    --fasta "${original_fasta}" \
    --breaks "${breaks}" \
    -o "${outdir}/${sample}.breaks_validation.tsv"
fi

if [ -n "${split_map}" ] && [ -n "${decision_log}" ]; then
  scripts/summarize_corrections.py \
    --split-map "${split_map}" \
    --decision-log "${decision_log}" \
    -o "${outdir}/${sample}.correction_summary.tsv" \
    --markdown "${outdir}/${sample}.correction_summary.md"
fi

if [ -n "${agp}" ]; then
  scripts/validate_agp.py \
    "${agp}" \
    -o "${outdir}/${sample}.agp_validation.tsv"
fi

if [ -n "${reference}" ]; then
  module load minimap2
  minimap2 \
    -x "${preset}" \
    -c \
    -t "${SLURM_NTASKS}" \
    "${reference}" \
    "${corrected_fasta}" \
    > "${outdir}/${sample}.corrected_vs_reference.${preset}.paf"
fi

echo "Post-correction validation directory: ${outdir}"
echo "Job ID: ${SLURM_JOBID}"
