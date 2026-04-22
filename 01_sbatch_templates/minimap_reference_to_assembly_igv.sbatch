#!/bin/bash
#SBATCH -J ref_to_asm
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=96G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/minimap_reference_to_assembly_%j.out
#SBATCH -e 00_log/minimap_reference_to_assembly_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load minimap2
module load samtools

: "${assembly:?Set assembly=07_assemblies/sample.primary.fa}"
: "${reference:?Set reference=references/reference.fa}"
: "${sample:?Set sample=reference_to_sample}"

preset="${preset:-asm20}"
outdir="${outdir:-09_dotplots/igv_reference_to_assembly}"

mkdir -p "${outdir}"

minimap2 --version
samtools --version | head -n 1

samtools faidx "${assembly}"

minimap2 \
  -ax "${preset}" \
  -t "${SLURM_NTASKS}" \
  "${assembly}" \
  "${reference}" \
  | samtools sort -@ "${SLURM_NTASKS}" -o "${outdir}/${sample}.${preset}.bam"

samtools index "${outdir}/${sample}.${preset}.bam"

echo "BAM: ${outdir}/${sample}.${preset}.bam"
echo "Open the assembly FASTA as the IGV genome, then load this BAM."
echo "Job ID: ${SLURM_JOBID}"
