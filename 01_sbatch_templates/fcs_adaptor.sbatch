#!/bin/bash
#SBATCH -J fcs_adaptor
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --mem=32G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/fcs_adaptor_%j.out
#SBATCH -e 00_log/fcs_adaptor_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

: "${assembly:?Set assembly=15_release/sample.genome.fa}"
: "${sample:?Set sample=SampleID}"
: "${fcs_image:?Set fcs_image=/path/to/fcs-adaptor.sif or load/run FCS another way}"

mkdir -p "11_contamination/fcs_adaptor/${sample}"

# NCBI FCS command syntax and databases can change. Check the current NCBI FCS
# documentation before production use:
# https://github.com/ncbi/fcs
apptainer exec "${fcs_image}" \
  fcs-adaptor \
  --fasta-input "${assembly}" \
  --output-dir "11_contamination/fcs_adaptor/${sample}" \
  --euk

echo "Job ID: ${SLURM_JOBID}"

