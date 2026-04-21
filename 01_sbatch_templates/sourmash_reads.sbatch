#!/bin/bash
#SBATCH -J sourmash_reads
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --mem=32G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/sourmash_reads_%j.out
#SBATCH -e 00_log/sourmash_reads_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load sourmash

: "${reads:?Set reads='03_reads_raw/sample.fastq.gz [more.fastq.gz ...]'}"
: "${sample:?Set sample=SampleID}"
: "${database:?Set database=/path/to/sourmash_database.sig.zip}"

k="${k:-51}"
scaled="${scaled:-1000}"

mkdir -p "11_contamination/sourmash/${sample}"

# shellcheck disable=SC2086
sourmash sketch dna \
  -p "k=${k},scaled=${scaled},abund" \
  -o "11_contamination/sourmash/${sample}/${sample}.k${k}.scaled${scaled}.sig" \
  ${reads}

sourmash search \
  "11_contamination/sourmash/${sample}/${sample}.k${k}.scaled${scaled}.sig" \
  "${database}" \
  --containment \
  --estimate-ani-ci \
  -n 50 \
  -o "11_contamination/sourmash/${sample}/${sample}.sourmash_search.csv"

echo "Job ID: ${SLURM_JOBID}"

