#!/bin/bash
#SBATCH -J busco
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=128G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/busco_%j.out
#SBATCH -e 00_log/busco_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load busco/6.0.0

: "${assembly:?Set assembly=07_assemblies/sample.primary.fa}"
: "${sample:?Set sample=SampleID}"
: "${lineage:?Set lineage=embryophyta_odb12 or a closer lineage}"

mkdir -p 08_stats/busco

busco \
  -i "${assembly}" \
  -m genome \
  -l "${lineage}" \
  -o "${sample}.busco" \
  --out_path 08_stats/busco \
  -c "${SLURM_NTASKS}"

echo "Job ID: ${SLURM_JOBID}"

