#!/bin/bash
#SBATCH -J mummer
#SBATCH -p ceres
#SBATCH -A gbru_lima_collaboration
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --mem=300G
#SBATCH -t 48:00:00
#SBATCH -o 00_log/mummer.out
#SBATCH -e 00_log/mummer.err

cd $SLURM_SUBMIT_DIR

# write message to both stdout and stderr
write_log() { echo; echo ===== "$@" =====; echo; echo >&2; echo ===== "$@" ===== >&2; echo >&2; }

module load mummer/4.0.0rc1
module load gnuplot/5.4.8

echo Output Directory: $oDir
echo Reference Genome: $ref
echo Query Genome: $query
echo File Name: $name
echo Min Cluster: $mincluster
echo Min Alignment Identity: $ai
echo Min Alignment Length: $al
echo Node: $SLURMD_NODENAME

mkdir -p $oDir

# Step 01
write_log 'Running Step 01: nucmer'
nucmer -t 16 -c $mincluster -p $oDir/$name $ref $query

# Step 02
write_log 'Running Step 02: show-tiling'
show-tiling -v 50 -i 85 -l 50000 -g -1 $oDir/$name.delta > $oDir/$name.tiling

# Step 03
write_log 'Running Step 03: delta filter'
delta-filter -i $ai -l $al -1 $oDir/$name.delta > $oDir/$name.filter

# Step 04
write_log 'Running Step 04: show-coords'
show-coords -r -c -l $oDir/$name.filter > $oDir/$name.coords

# Step 05
write_log 'Running Step 05: mummerplot postscript'
mummerplot -p $oDir/plot_$name -R $ref --postscript --large --layout --fat $oDir/$name.filter

# attach the job ID to the log
# check job resource usage with: seff <Jobid>
echo ' '
echo Job ID: $SLURM_JOBID
echo ' '

## Run notes:
## sbatch -o 00_log/mumplot_${name}.out -e 00_log/mumplot_${name}.err --export oDir=outputdirectory,ref=refGenome,query=$f,name=$name,al=10000,ai=90,mincluster=100 /project/gbru_lima_collaboration/analysis.roth/01_sbatch/mummer_plot.sbatch