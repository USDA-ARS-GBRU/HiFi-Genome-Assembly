#!/bin/bash
#SBATCH -J merqury
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=128G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/merqury_%j.out
#SBATCH -e 00_log/merqury_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load merqury
module load meryl

: "${reads:?Set reads='03_reads_raw/sample.fastq.gz [more.fastq.gz ...]'}"
: "${assembly:?Set assembly=07_assemblies/sample.primary.fa}"
: "${sample:?Set sample=SampleID}"

k="${k:-21}"

mkdir -p 05_kmers 08_stats/merqury

# shellcheck disable=SC2086
meryl k="${k}" count threads="${SLURM_NTASKS}" \
  output "05_kmers/${sample}.k${k}.reads.meryl" \
  ${reads}

merqury.sh \
  "05_kmers/${sample}.k${k}.reads.meryl" \
  "${assembly}" \
  "08_stats/merqury/${sample}"

echo "Job ID: ${SLURM_JOBID}"

