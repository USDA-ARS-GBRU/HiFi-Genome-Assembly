#!/bin/bash
#SBATCH -J liftoff
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/liftoff_%j.out
#SBATCH -e 00_log/liftoff_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load liftoff

: "${target_genome:?Set target_genome=13_repeats/sample.softmasked.fa}"
: "${reference_genome:?Set reference_genome=references/reference.fa}"
: "${reference_gff:?Set reference_gff=references/reference.gff3}"
: "${sample:?Set sample=SampleID}"

outdir="14_genes/liftoff/${sample}"
mkdir -p "${outdir}"

liftoff \
  -g "${reference_gff}" \
  -o "${outdir}/${sample}.liftoff.gff3" \
  -u "${outdir}/${sample}.liftoff.unmapped.txt" \
  -p "${SLURM_NTASKS}" \
  "${target_genome}" \
  "${reference_genome}"

echo "Job ID: ${SLURM_JOBID}"
