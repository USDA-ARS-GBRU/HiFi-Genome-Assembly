#!/bin/bash
#SBATCH -J maker
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=256G
#SBATCH -t 96:00:00
#SBATCH -o 00_log/maker_%j.out
#SBATCH -e 00_log/maker_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load maker

: "${control_dir:?Set control_dir=14_genes/maker/control_files}"

outdir="${outdir:-14_genes/maker/run}"
mkdir -p "${outdir}"

cp "${control_dir}"/maker_*_ctl "${outdir}/"
cd "${outdir}"

maker -base maker_run -fix_nucleotides

gff3_merge -d maker_run.maker.output/maker_run_master_datastore_index.log > maker_run.all.gff3
fasta_merge -d maker_run.maker.output/maker_run_master_datastore_index.log

echo "Job ID: ${SLURM_JOBID}"
