#!/bin/bash
#SBATCH -J nucmer_plot
#SBATCH -p ceres
#SBATCH -A gbru_fy25_fusarium_tr4
#SBATCH -N 1
#SBATCH -n 2
#SBATCH --mem=3G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/07c_nucmer.out
#SBATCH -e 00_log/07c_nucmer.err

cd $SLURM_SUBMIT_DIR
whoami
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

if [ ! -d $oDir ]; then mkdir $oDir; fi

echo Running nucmer >&2
nucmer -t 2 -c $mincluster -p $oDir/$name $ref $query
echo Running delta filter >&2
delta-filter -i $ai -l $al -1 $oDir/$name.delta > $oDir/$name.filter
echo Running show-coords >&2
show-coords -r -c -l $oDir/$name.filter > $oDir/$name.coords
echo Running show-tiling >&2
show-tiling $oDir/$name.filter > $oDir/$name.tiling
echo Running mummerplot postscript >&2
mummerplot -p $oDir/plot_$name -R $ref --postscript --large --layout --fat $oDir/$name.filter


# attach the job ID to the log
# check job resource usage with: seff <Jobid>
echo ' '
echo Job ID: $SLURM_JOBID
echo ' '

## Run notes:
## for f in 07c_NucmerPlots/*.fna; do name=`basename $f _genomic.fna`; echo $name; sbatch -o 00_log/07c_nucplot_C058-${name}.out -e 00_log/07c_nucplot_C058-${name}.err --export oDir=07c_NucmerPlots/01_C058,ref=07a_SelectedGenomes/Fusarium_purpurascens_GCA_040822135.1_ASM4082213v1_genomic.fna,query=$f,name=$name,al=1000,ai=90,mincluster=100 01_sbatch/03c_nucmer_plot.sbatch; done
## for f in 07c_NucmerPlots/*.fna; do name=`basename $f _genomic.fna`; echo $name; sbatch -o 00_log/07c_nucplot_FOII5-${name}.out -e 00_log/07c_nucplot_FOII5-${name}.err --export oDir=07c_NucmerPlots,ref=07a_SelectedGenomes/Fusarium_odoratissimum_GCA_000260195.2_FO_II5_V1_genomic.fna,query=$f,name=$name,al=10000,ai=95,mincluster=100 01_sbatch/03c_nucmer_plot.sbatch; done
## for f in 07c_NucmerPlots/*.fna; do name=`basename $f _genomic.fna`; echo $name; sbatch -o 00_log/07c_nucplot_II5-${name}.out -e 00_log/07c_nucplot_II5-${name}.err --export oDir=07c_NucmerPlots/03_II5,ref=07a_SelectedGenomes/Fusarium_oxysporum_GCA_031834405.1_ASM3183440v1_genomic.fna,query=$f,name=$name,al=1000,ai=90,mincluster=100 01_sbatch/03c_nucmer_plot.sbatch; done
## for f in 07c_NucmerPlots/*.fna; do name=`basename $f _genomic.fna`; echo $name; sbatch -o 00_log/07c_nucplot_CR1-${name}.out -e 00_log/07c_nucplot_CR1-${name}.err --export oDir=07c_NucmerPlots/03_CR1,ref=07a_SelectedGenomes/Fusarium_phialophorum_GCA_040822225.1_ASM4082222v1_genomic.fna,query=$f,name=$name,al=1000,ai=90,mincluster=100 01_sbatch/03c_nucmer_plot.sbatch; done
