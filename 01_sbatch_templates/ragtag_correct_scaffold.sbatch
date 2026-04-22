#!/bin/bash
#SBATCH -J ragtag
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=128G
#SBATCH -t 48:00:00
#SBATCH -o 00_log/ragtag_%j.out
#SBATCH -e 00_log/ragtag_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load ragtag

: "${reference:?Set reference=references/close_reference.fa}"
: "${query:?Set query=07_assemblies/sample.primary.fa}"
: "${sample:?Set sample=SampleID}"

mode="${mode:-both}"
outdir="${outdir:-10_scaffolding/ragtag/${sample}}"

mkdir -p "${outdir}"

ragtag.py --version || true

if [ "${mode}" = "correct" ] || [ "${mode}" = "both" ]; then
  ragtag.py correct \
    -t "${SLURM_NTASKS}" \
    -o "${outdir}/correct" \
    "${reference}" \
    "${query}"
fi

if [ "${mode}" = "scaffold" ] || [ "${mode}" = "both" ]; then
  scaffold_query="${query}"
  if [ "${mode}" = "both" ]; then
    scaffold_query="${outdir}/correct/ragtag.correct.fasta"
  fi

  ragtag.py scaffold \
    -t "${SLURM_NTASKS}" \
    -o "${outdir}/scaffold" \
    "${reference}" \
    "${scaffold_query}"
fi

echo "Job ID: ${SLURM_JOBID}"
