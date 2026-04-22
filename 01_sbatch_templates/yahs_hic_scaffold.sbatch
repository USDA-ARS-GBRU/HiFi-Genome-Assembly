#!/bin/bash
#SBATCH -J yahs_hic
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=128G
#SBATCH -t 48:00:00
#SBATCH -o 00_log/yahs_%j.out
#SBATCH -e 00_log/yahs_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load bwa
module load samtools
module load yahs

: "${assembly:?Set assembly=07_assemblies/sample.primary.fa}"
: "${hic_r1:?Set hic_r1=/path/to/HiC_R1.fastq.gz}"
: "${hic_r2:?Set hic_r2=/path/to/HiC_R2.fastq.gz}"
: "${sample:?Set sample=SampleID}"

outdir="${outdir:-10_scaffolding/${sample}/yahs}"

mkdir -p "${outdir}"

bwa 2>&1 | head -n 1 || true
samtools --version | head -n 1
yahs --version || true

bwa index "${assembly}"
samtools faidx "${assembly}"

bwa mem -5SP -t "${SLURM_NTASKS}" \
  "${assembly}" \
  "${hic_r1}" \
  "${hic_r2}" \
  | samtools view -b -@ 8 \
  | samtools sort -@ 8 -o "${outdir}/${sample}.hic.bam"

samtools index "${outdir}/${sample}.hic.bam"

yahs \
  "${assembly}" \
  "${outdir}/${sample}.hic.bam" \
  -o "${outdir}/${sample}.yahs"

samtools flagstat "${outdir}/${sample}.hic.bam" > "${outdir}/${sample}.hic.flagstat.txt"

echo "Job ID: ${SLURM_JOBID}"
