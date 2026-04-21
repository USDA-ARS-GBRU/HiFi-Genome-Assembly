#!/bin/bash
#SBATCH -J nucmer_plot
#SBATCH -p ceres
#SBATCH -A gbru_fy25_fusarium_tr4
#SBATCH -N 1
#SBATCH -n 2
#SBATCH --mem=3G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/07c_nucmer_%A_%a.out
#SBATCH -e 00_log/07c_nucmer_%A_%a.err
#SBATCH --array=0-599   # adjust based on jobfile size

cd $SLURM_SUBMIT_DIR
whoami
module load mummer/4.0.0rc1
module load gnuplot/5.4.8

# read parameters from jobfile
line=$(sed -n "$((SLURM_ARRAY_TASK_ID+1))p" nucmer_jobs.txt)
set -- $line
oDir=$1
ref=$2
query=$3
name=$4
mincluster=$5
ai=$6
al=$7

echo Output Directory: $oDir
echo Reference Genome: $ref
echo Query Genome: $query
echo File Name: $name
echo Min Cluster: $mincluster
echo Min Alignment Identity: $ai
echo Min Alignment Length: $al
echo Node: $SLURMD_NODENAME

mkdir -p $oDir/$name

echo Running nucmer >&2
nucmer -t 2 -c $mincluster -p $oDir/$name/$name $ref $query
echo Running delta filter >&2
delta-filter -i $ai -l $al -1 $oDir/$name/$name.delta > $oDir/$name/$name.filter
echo Running show-coords >&2
show-coords -r -c -l $oDir/$name/$name.filter > $oDir/$name/$name.coords
echo Running show-tiling >&2
show-tiling $oDir/$name/$name.filter > $oDir/$name/$name.tiling
echo Running mummerplot postscript >&2
mummerplot -p $oDir/$name/plot_$name -R $ref --postscript --large --layout --fat $oDir/$name/$name.filter

# attach the job ID to the log
# check job resource usage with: seff <Jobid>
echo ' '
echo Job ID: $SLURM_JOBID
echo ' '

## Run notes:
# sbatch 01_sbatch/03d_nucmer_plot_array.sbatch
