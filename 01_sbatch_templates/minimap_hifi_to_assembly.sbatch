#!/bin/bash
#SBATCH -J map_hifi
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/map_hifi_%j.out
#SBATCH -e 00_log/map_hifi_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load minimap2
module load samtools

: "${assembly:?Set assembly=07_assemblies/sample.primary.fa}"
: "${reads:?Set reads='03_reads_raw/sample.fastq.gz [more.fastq.gz ...]'}"
: "${sample:?Set sample=SampleID}"

mkdir -p 08_stats/read_mapping

# shellcheck disable=SC2086
minimap2 -ax map-hifi -t "${SLURM_NTASKS}" \
  "${assembly}" \
  ${reads} \
  | samtools sort -@ 8 -o "08_stats/read_mapping/${sample}.hifi_to_assembly.bam"

samtools index "08_stats/read_mapping/${sample}.hifi_to_assembly.bam"
samtools coverage "08_stats/read_mapping/${sample}.hifi_to_assembly.bam" \
  > "08_stats/read_mapping/${sample}.hifi_to_assembly.coverage.tsv"

echo "Job ID: ${SLURM_JOBID}"

