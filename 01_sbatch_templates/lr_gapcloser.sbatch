#!/bin/bash
#SBATCH -J lr_gapcloser
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --mem=64G
#SBATCH -t 48:00:00
#SBATCH -o 00_log/lr_gapcloser_%j.out
#SBATCH -e 00_log/lr_gapcloser_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load LR_Gapcloser

: "${scaffolds:?Set scaffolds=10_scaffolding/sample.scaffolds.fa}"
: "${reads_fasta:?Set reads_fasta=03_reads_raw/sample.hifi.fa}"
: "${sample:?Set sample=SampleID}"

platform="${platform:-p}"
outdir="${outdir:-10_scaffolding/gap_filling/lr_gapcloser/${sample}}"

mkdir -p "${outdir}"

LR_Gapcloser.sh \
  -i "${scaffolds}" \
  -l "${reads_fasta}" \
  -s "${platform}" \
  -t "${SLURM_NTASKS}" \
  -o "${outdir}"

echo "Review gapclosed.fasta in the final iteration directory under ${outdir}"
echo "Job ID: ${SLURM_JOBID}"
