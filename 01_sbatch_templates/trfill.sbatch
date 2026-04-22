#!/bin/bash
#SBATCH -J trfill
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=256G
#SBATCH -t 96:00:00
#SBATCH -o 00_log/trfill_%j.out
#SBATCH -e 00_log/trfill_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load TRFill

: "${config:?Set config=00_metadata/trfill.haploid.config.txt}"
: "${sample:?Set sample=SampleID}"

outdir="${outdir:-10_scaffolding/gap_filling/trfill/${sample}}"
reads_format="${reads_format:-HiFi}"
phase_flag="${phase_flag:-}"
hic_flag="${hic_flag:-}"

mkdir -p "${outdir}"

trfill \
  -t "${SLURM_NTASKS}" \
  -o "${outdir}" \
  -f "${reads_format}" \
  ${phase_flag} \
  ${hic_flag} \
  -c "${config}"

echo "Review ${outdir}/final_result and TRFill logs"
echo "Job ID: ${SLURM_JOBID}"
