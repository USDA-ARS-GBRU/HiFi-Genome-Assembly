#!/bin/bash
#SBATCH -J fastqc
#SBATCH -p ceres
#SBATCH -A gbru_fy25_fusarium_tr4
#SBATCH -N 1
#SBATCH -n 11
#SBATCH --mem=20G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/01b_fastqc.out
#SBATCH -e 00_log/01b_fastqc.err

cd $SLURM_SUBMIT_DIR

module load fastqc/0.12.1

echo Infiles: $iFiles
echo Output Directory: $oDir
echo Node: $SLURMD_NODENAME

mkdir -p ${oDir}

fastqc -t 11 -o $oDir $iFiles

# attach the job ID to the log
# check job resource usage with: seff <Jobid>
echo ' '
echo Job ID: $SLURM_JOBID
echo ' '

## Run log:
## sbatch -o 00_log/01b_fastqc_pre.out -e 00_log/01b_fastqc_pre.err --export iFiles=03a_PacBioHiFi.fastq/*.fastq,oDir=03a_PacBioHiFi.fastq/00_fastqc 01_sbatch/01b_fastqc.sbatch
## sbatch -o 00_log/01d_fastqc_post.out -e 00_log/01d_fastqc_post.err --export iFiles=03b_PacBioHiFi.fastq.trim/*.fastq,oDir=03b_PacBioHiFi.fastq.trim/00_fastqc 01_sbatch/01b_fastqc.sbatch
