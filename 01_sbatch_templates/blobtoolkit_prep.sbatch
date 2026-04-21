#!/bin/bash
#SBATCH -J blobtoolkit
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --mem=128G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/blobtoolkit_%j.out
#SBATCH -e 00_log/blobtoolkit_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load blobtoolkit
module load minimap2
module load samtools
module load blast+

: "${assembly:?Set assembly=07_assemblies/sample.primary.fa}"
: "${reads:?Set reads='03_reads_raw/sample.fastq.gz [more.fastq.gz ...]'}"
: "${sample:?Set sample=SampleID}"
: "${taxdump:?Set taxdump=/path/to/ncbi_taxdump}"
: "${blastdb:?Set blastdb=/path/to/nt_or_custom_blast_db}"

outdir="11_contamination/blobtoolkit/${sample}"
mkdir -p "${outdir}"

# shellcheck disable=SC2086
minimap2 -ax map-hifi -t "${SLURM_NTASKS}" \
  "${assembly}" \
  ${reads} \
  | samtools sort -@ 8 -o "${outdir}/${sample}.hifi_to_assembly.bam"

samtools index "${outdir}/${sample}.hifi_to_assembly.bam"

blastn \
  -query "${assembly}" \
  -db "${blastdb}" \
  -outfmt "6 qseqid staxids bitscore std" \
  -max_target_seqs 10 \
  -max_hsps 1 \
  -evalue 1e-25 \
  -num_threads "${SLURM_NTASKS}" \
  -out "${outdir}/${sample}.blastn.tax.tsv"

blobtools create \
  --fasta "${assembly}" \
  --taxid "${taxid:-}" \
  --taxdump "${taxdump}" \
  "${outdir}/${sample}"

blobtools add \
  --cov "${outdir}/${sample}.hifi_to_assembly.bam" \
  --taxrule bestsumorder \
  --hits "${outdir}/${sample}.blastn.tax.tsv" \
  --taxdump "${taxdump}" \
  "${outdir}/${sample}"

blobtools view "${outdir}/${sample}"

echo "Job ID: ${SLURM_JOBID}"

