#!/bin/bash
#SBATCH -J braker3
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=256G
#SBATCH -t 96:00:00
#SBATCH -o 00_log/braker3_%j.out
#SBATCH -e 00_log/braker3_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load BRAKER

: "${genome:?Set genome=13_repeats/sample.softmasked.fa}"
: "${species:?Set species=Genus_species_sample}"

outdir="${outdir:-14_genes/braker3/${species}}"
rnaseq_bam="${rnaseq_bam:-}"
proteins="${proteins:-}"

mkdir -p "${outdir}"

args=(
  --genome="${genome}"
  --species="${species}"
  --threads="${SLURM_NTASKS}"
  --gff3
  --workingdir="${outdir}"
)

if [ -n "${rnaseq_bam}" ]; then
  args+=(--bam="${rnaseq_bam}")
fi

if [ -n "${proteins}" ]; then
  args+=(--prot_seq="${proteins}")
fi

braker.pl "${args[@]}"

echo "Job ID: ${SLURM_JOBID}"
