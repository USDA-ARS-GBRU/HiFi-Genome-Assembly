#!/bin/bash
#SBATCH -J fcs_gx
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --mem=128G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/fcs_gx_%j.out
#SBATCH -e 00_log/fcs_gx_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

: "${assembly:?Set assembly=15_release/sample.genome.fa}"
: "${sample:?Set sample=SampleID}"
: "${taxid:?Set taxid=NCBI_taxonomy_id}"
: "${fcs_image:?Set fcs_image=/path/to/fcs-gx.sif or load/run FCS another way}"
: "${gx_db:?Set gx_db=/path/to/FCS-GX/database}"

mkdir -p "11_contamination/fcs_gx/${sample}"

# NCBI FCS command syntax and databases can change. Check the current NCBI FCS
# documentation before production use:
# https://github.com/ncbi/fcs
apptainer exec "${fcs_image}" \
  fcs-gx \
  --fasta "${assembly}" \
  --tax-id "${taxid}" \
  --gx-db "${gx_db}" \
  --out-dir "11_contamination/fcs_gx/${sample}" \
  --split-fasta

echo "Job ID: ${SLURM_JOBID}"

