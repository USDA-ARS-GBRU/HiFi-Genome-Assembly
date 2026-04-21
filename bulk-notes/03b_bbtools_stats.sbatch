#!/bin/bash
#SBATCH -J stats
#SBATCH -p ceres
#SBATCH -A gbru_fy25_fusarium_tr4
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=1G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/bbtools_stats.out
#SBATCH -e 00_log/bbtools_stats.err

cd $SLURM_SUBMIT_DIR

module load bbtools/39.01

echo inDir: $inDir
echo outFile: $fout

for f in ${inDir}/*.fa; do echo $f; echo ' '; stats.sh in=${f} format=3 -Xmx1g; echo ' '; echo ' '; done > $fout

# attach the job ID to the log
# check job resource usage with: seff <Jobid>
echo ' '
echo Job ID: $SLURM_JOBID
echo ' '

## Run notes:
# sbatch --export inDir=04e_fa ../01_sbatch/bbtools_stats.sbatch
