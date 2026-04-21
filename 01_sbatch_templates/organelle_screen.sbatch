#!/bin/bash
#SBATCH -J organelle_screen
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --mem=32G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/organelle_screen_%j.out
#SBATCH -e 00_log/organelle_screen_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load minimap2
module load samtools

: "${assembly:?Set assembly=07_assemblies/sample.primary.fa}"
: "${organelle_refs:?Set organelle_refs=references/organelle_refs.fa}"
: "${sample:?Set sample=SampleID}"

mkdir -p "11_contamination/organelle/${sample}"

minimap2 -x asm5 -t "${SLURM_NTASKS}" \
  "${organelle_refs}" \
  "${assembly}" \
  > "11_contamination/organelle/${sample}/${sample}.assembly_vs_organelle_refs.paf"

awk 'BEGIN{OFS="\t"} {print $1,$2,$3,$4,$5,$6,$10,$11,$12}' \
  "11_contamination/organelle/${sample}/${sample}.assembly_vs_organelle_refs.paf" \
  > "11_contamination/organelle/${sample}/${sample}.organelle_hits.summary.tsv"

echo "Job ID: ${SLURM_JOBID}"

