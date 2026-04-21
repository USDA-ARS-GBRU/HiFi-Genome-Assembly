#!/bin/bash
#SBATCH -J bam2fastq
#SBATCH -p ceres
#SBATCH -A gbru_lima_collaboration
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=5G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/bam2fastq.out
#SBATCH -e 00_log/bam2fastq.err

cd $SLURM_SUBMIT_DIR

# write message to both stdout and stderr
write_log() { echo; echo ===== "$@" =====; echo; echo >&2; echo ===== "$@" ===== >&2; echo >&2; }

module load bamtools/2.5.2

echo Infile: $infile
echo Sample: $sample
echo Output Directory: $oDir
echo Node: $SLURMD_NODENAME

mkdir -p ${oDir}

bamtools convert -format fastq -in $infile -out ${oDir}/${sample}.fastq

# attach the job ID to the log
# check job resource usage with: seff <Jobid>
write_log "Job ID: $SLURM_JOBID"

## Run notes:
## sbatch -o 00_log/bam2fastq_${sample}.out -e 00_log/bam2fastq_${sample}.err --export infile=bam,sample=sample,oDir=$oDir /project/gbru_lima_collaboration/analysis.roth/01_sbatch/bam2fastq.sbatch