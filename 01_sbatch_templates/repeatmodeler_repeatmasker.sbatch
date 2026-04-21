#!/bin/bash
#SBATCH -J repeatmodeler
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=256G
#SBATCH -t 72:00:00
#SBATCH -o 00_log/repeatmodeler_%j.out
#SBATCH -e 00_log/repeatmodeler_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load RepeatModeler
module load RepeatMasker

: "${genome:?Set genome=07_assemblies/sample.primary.fa}"
: "${sample:?Set sample=SampleID}"

outdir="13_repeats/repeatmodeler/${sample}"
mkdir -p "${outdir}"
cp "${genome}" "${outdir}/${sample}.fa"

cd "${outdir}"

BuildDatabase \
  -name "${sample}.repeatdb" \
  "${sample}.fa"

RepeatModeler \
  -database "${sample}.repeatdb" \
  -threads "${SLURM_NTASKS}" \
  -LTRStruct

families=$(find . -name "consensi.fa.classified" | head -n 1)
if [ -z "${families}" ]; then
  echo "ERROR: could not find consensi.fa.classified" >&2
  exit 1
fi

RepeatMasker \
  -pa "${SLURM_NTASKS}" \
  -lib "${families}" \
  -xsmall \
  -gff \
  "${sample}.fa"

echo "Job ID: ${SLURM_JOBID}"

