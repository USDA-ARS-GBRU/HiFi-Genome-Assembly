#!/bin/bash
#SBATCH -J asm_stats
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --mem=8G
#SBATCH -t 04:00:00
#SBATCH -o 00_log/asm_stats_%j.out
#SBATCH -e 00_log/asm_stats_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load seqkit
module load bbtools

: "${assemblies:?Set assemblies='07_assemblies/*.fa'}"

mkdir -p 08_stats

# shellcheck disable=SC2086
seqkit stats -a ${assemblies} > 08_stats/seqkit_assembly_stats.tsv

# shellcheck disable=SC2086
for fa in ${assemblies}; do
  name=$(basename "$fa")
  name=${name%.fa}
  stats.sh in="$fa" format=3 -Xmx4g > "08_stats/${name}.bbtools_stats.txt"
done

echo "Job ID: ${SLURM_JOBID}"

