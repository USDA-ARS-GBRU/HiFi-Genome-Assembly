#!/bin/bash
#SBATCH -J bam2fastq
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=8G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/bam2fastq_%j.out
#SBATCH -e 00_log/bam2fastq_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

# Edit this line for your cluster if bamtools is provided as a module.
module load bamtools/2.5.2

: "${infile:?Set infile=/path/to/input.bam}"
: "${sample:?Set sample=SampleID}"
: "${oDir:?Set oDir=03_reads_raw}"

echo "Input BAM: ${infile}"
echo "Sample: ${sample}"
echo "Output directory: ${oDir}"
echo "Node: ${SLURMD_NODENAME}"

mkdir -p "${oDir}"

bamtools convert \
  -format fastq \
  -in "${infile}" \
  -out "${oDir}/${sample}.fastq"

echo "Job ID: ${SLURM_JOBID}"

