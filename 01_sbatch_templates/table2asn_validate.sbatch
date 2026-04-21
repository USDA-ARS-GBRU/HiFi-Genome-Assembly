#!/bin/bash
#SBATCH -J table2asn
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --mem=32G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/table2asn_%j.out
#SBATCH -e 00_log/table2asn_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load table2asn

: "${fasta:?Set fasta=15_release/sample.genome.fa}"
: "${gff:?Set gff=15_release/sample.annotation.gff3}"
: "${template:?Set template=00_metadata/template.sbt}"
: "${sample:?Set sample=SampleID}"

outdir="15_release/ncbi_validation/${sample}"
mkdir -p "${outdir}"

cp "${fasta}" "${outdir}/${sample}.fsa"
cp "${gff}" "${outdir}/${sample}.gff"
cp "${template}" "${outdir}/template.sbt"

cd "${outdir}"

table2asn \
  -M n \
  -J \
  -c w \
  -euk \
  -t template.sbt \
  -i "${sample}.fsa" \
  -f "${sample}.gff" \
  -V vb

echo "Job ID: ${SLURM_JOBID}"
