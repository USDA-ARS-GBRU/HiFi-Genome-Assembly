#!/bin/bash
#SBATCH -J ragtag
#SBATCH -p ceres
#SBATCH -A gbru_fy25_fusarium_tr4
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=128G
#SBATCH -t 48:00:00
#SBATCH -o 00_log/07_ragtag.out
#SBATCH -e 00_log/07_ragtag.err

cd $SLURM_SUBMIT_DIR

module load ragtag/2.1.0

echo Output Directory: $oDir
echo Reference Genome: $refG
echo Query Genome: $queryG
echo File Name: $name
echo Ref Name: $refName

mkdir -p $oDir/$name.$refName

# initial ragtag command
# ragtag.py scaffold -t 50 -C -r -o $oDir/$name $refG $queryG

# run ragtag (match -t to --cpus-per-task)
# For PacBio HiFi reads I don't think we want to run the correction step as inversions and rearrangements
# are likely real and supported by the high quality long read assemblies.
#ragtag.py correct -t 32 --mm2-params "-x asm5 -t 32" --remove-small --min-aln 10000 -o $oDir/$name-$refName.correct $refG $queryG
ragtag.py scaffold -t 32 -C -r -f 1000 --remove-small $refG $queryG -o $oDir/$name.$refName


# attach the job ID to the log
# check job resource usage with: seff <Jobid>
echo ' '
echo Job ID: $SLURM_JOBID
echo ' '

seff $SLURM_JOBID

## Run notes:
# for f in 03_fastq/04e_fa/*.fa; do n=`basename $f | cut -d. -f1`; sbatch -o 00_log/RagTag_${n}.out -e 00_log/RagTag_${n}.err --export oDir=05_RagTag_Scaffolds,refG=04_refGenomes/Pawnee/GCF_018687715.1_C.illinoinensisPawnee_v1_genomic.fna,queryG=$f,name=$n 01_sbatch/ragtag.sbatch; done
