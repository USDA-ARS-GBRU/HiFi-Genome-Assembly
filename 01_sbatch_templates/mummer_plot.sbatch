#!/bin/bash
#SBATCH -J mummer
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/mummer_%j.out
#SBATCH -e 00_log/mummer_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load mummer/4.0.0rc1
module load gnuplot/5.4.8

: "${oDir:?Set oDir=09_dotplots}"
: "${ref:?Set ref=/path/to/reference.fa}"
: "${query:?Set query=/path/to/query.fa}"
: "${name:?Set name=ref_vs_query}"

mincluster="${mincluster:-100}"
identity="${identity:-90}"
minlen="${minlen:-10000}"

echo "Output directory: ${oDir}"
echo "Reference: ${ref}"
echo "Query: ${query}"
echo "Name: ${name}"
echo "Minimum cluster: ${mincluster}"
echo "Minimum identity: ${identity}"
echo "Minimum length: ${minlen}"
echo "Node: ${SLURMD_NODENAME}"

mkdir -p "${oDir}"

nucmer \
  -t "${SLURM_NTASKS}" \
  -c "${mincluster}" \
  -p "${oDir}/${name}" \
  "${ref}" \
  "${query}"

delta-filter \
  -i "${identity}" \
  -l "${minlen}" \
  -1 \
  "${oDir}/${name}.delta" \
  > "${oDir}/${name}.filter"

show-coords -r -c -l \
  "${oDir}/${name}.filter" \
  > "${oDir}/${name}.coords"

show-tiling \
  "${oDir}/${name}.filter" \
  > "${oDir}/${name}.tiling"

mummerplot \
  -p "${oDir}/plot_${name}" \
  -R "${ref}" \
  --postscript \
  --large \
  --layout \
  --fat \
  "${oDir}/${name}.filter"

echo "Job ID: ${SLURM_JOBID}"

