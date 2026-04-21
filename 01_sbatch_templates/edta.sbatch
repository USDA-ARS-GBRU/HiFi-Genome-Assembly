#!/bin/bash
#SBATCH -J edta
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=256G
#SBATCH -t 72:00:00
#SBATCH -o 00_log/edta_%j.out
#SBATCH -e 00_log/edta_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load EDTA

: "${genome:?Set genome=07_assemblies/sample.primary.fa}"
: "${sample:?Set sample=SampleID}"

species="${species:-others}"
sensitive="${sensitive:-1}"

mkdir -p "13_repeats/edta/${sample}"
cp "${genome}" "13_repeats/edta/${sample}/${sample}.fa"

cd "13_repeats/edta/${sample}"

EDTA.pl \
  --genome "${sample}.fa" \
  --species "${species}" \
  --step all \
  --sensitive "${sensitive}" \
  --anno 1 \
  --threads "${SLURM_NTASKS}"

echo "Job ID: ${SLURM_JOBID}"

