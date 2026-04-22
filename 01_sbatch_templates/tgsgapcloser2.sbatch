#!/bin/bash
#SBATCH -J tgsgapcloser
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=128G
#SBATCH -t 72:00:00
#SBATCH -o 00_log/tgsgapcloser_%j.out
#SBATCH -e 00_log/tgsgapcloser_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load TGS-GapCloser2

: "${scaffolds:?Set scaffolds=10_scaffolding/sample.scaffolds.fa}"
: "${reads_fasta:?Set reads_fasta=03_reads_raw/sample.hifi.fa}"
: "${sample:?Set sample=SampleID}"

tgstype="${tgstype:-hifi}"
outdir="${outdir:-10_scaffolding/gap_filling/tgsgapcloser2/${sample}}"
prefix="${outdir}/${sample}"

mkdir -p "${outdir}"

tgsgapcloser2 \
  --scaff "${scaffolds}" \
  --reads "${reads_fasta}" \
  --output "${prefix}" \
  --tgstype "${tgstype}" \
  --thread "${SLURM_NTASKS}" \
  --ne

echo "Review ${prefix}.scaff_seq and ${prefix}.gap_fill_details"
echo "Job ID: ${SLURM_JOBID}"
