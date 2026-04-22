#!/bin/bash
#SBATCH -J asm_paf
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/minimap_assembly_paf_%j.out
#SBATCH -e 00_log/minimap_assembly_paf_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load minimap2

: "${target:?Set target=references/reference.fa}"
: "${query:?Set query=07_assemblies/sample.primary.fa}"
: "${sample:?Set sample=sample_vs_reference}"

preset="${preset:-asm20}"
outdir="${outdir:-09_dotplots/paf}"

mkdir -p "${outdir}"

minimap2 --version

minimap2 \
  -x "${preset}" \
  -c \
  -t "${SLURM_NTASKS}" \
  "${target}" \
  "${query}" \
  > "${outdir}/${sample}.${preset}.paf"

echo "PAF: ${outdir}/${sample}.${preset}.paf"
echo "Job ID: ${SLURM_JOBID}"
