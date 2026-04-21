#!/bin/bash
#SBATCH -J hifiasm
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=300G
#SBATCH -t 48:00:00
#SBATCH -o 00_log/hifiasm_%j.out
#SBATCH -e 00_log/hifiasm_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

# Edit this line for your cluster, or replace it with conda/pixi activation.
module load hifiasm/0.25.0

: "${reads:?Set reads='read1.fastq.gz [read2.fastq.gz ...]'}"
: "${sample:?Set sample=SampleID}"
: "${oDir:?Set oDir=06_hifiasm}"

extra_args="${extra_args:-}"

echo "Reads: ${reads}"
echo "Sample: ${sample}"
echo "Output directory: ${oDir}"
echo "Extra hifiasm args: ${extra_args}"
echo "Node: ${SLURMD_NODENAME}"
hifiasm --version || true

mkdir -p "${oDir}/${sample}" 07_assemblies

# shellcheck disable=SC2086
hifiasm \
  -t "${SLURM_NTASKS}" \
  -o "${oDir}/${sample}/${sample}" \
  ${extra_args} \
  ${reads}

for gfa in "${oDir}/${sample}"/*.gfa; do
  base=$(basename "$gfa" .gfa)
  awk '/^S/{print ">"$2; print $3}' "$gfa" > "07_assemblies/${base}.fa"
done

echo "Job ID: ${SLURM_JOBID}"

