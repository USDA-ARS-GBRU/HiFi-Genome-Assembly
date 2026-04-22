#!/bin/bash
#SBATCH -J 3d_dna
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=128G
#SBATCH -t 72:00:00
#SBATCH -o 00_log/3d_dna_%j.out
#SBATCH -e 00_log/3d_dna_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load 3d-dna

: "${assembly:?Set assembly=07_assemblies/sample.primary.fa}"
: "${merged_nodups:?Set merged_nodups=10_scaffolding/sample/juicer/aligned/merged_nodups.txt}"
: "${sample:?Set sample=SampleID}"

outdir="${outdir:-10_scaffolding/${sample}/3d_dna}"
repeat_coverage="${repeat_coverage:-2}"
extra_args="${extra_args:-}"

mkdir -p "${outdir}"

run-asm-pipeline.sh --version || true

cp "${assembly}" "${outdir}/${sample}.input.fa"
cp "${merged_nodups}" "${outdir}/${sample}.merged_nodups.txt"

cd "${outdir}"

run-asm-pipeline.sh \
  --editor-repeat-coverage "${repeat_coverage}" \
  ${extra_args} \
  "${sample}.input.fa" \
  "${sample}.merged_nodups.txt"

echo "Review generated .hic and .assembly files in Juicebox/JBAT before release."
echo "Job ID: ${SLURM_JOBID}"
