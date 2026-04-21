#!/bin/bash
#SBATCH -J HiFiASM
#SBATCH -p ceres
#SBATCH -A gbru_fy25_fusarium_tr4
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=300G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/06a_hifiasm.out
#SBATCH -e 00_log/06a_hifiasm.err

cd $SLURM_SUBMIT_DIR

module load hifiasm/0.25.0

echo Infile: $infile
echo Sample: $sample
echo Output Directory: $oDir
echo Node: $SLURMD_NODENAME

mkdir -p ${oDir}/${sample}

hifiasm -t 32 -o ${oDir}/${sample}/${sample} $infile

# from Hifiasm FAQ to get contigs in FASTA
# https://hifiasm.readthedocs.io/en/latest/faq.html
for gfa in ${oDir}/${sample}/*.gfa; do
    name=`basename $gfa | rev | cut -d. -f2- | rev`
    echo $gfa $name
    awk '/^S/{print ">"$2;print $3}' $gfa > ${oDir}/${sample}/${name}.fa
done

# copy hap1 and hap2 fasta files to main oDir
cp ${oDir}/${sample}/*.hap?.p_ctg.fa ${oDir}/

# attach the job ID to the log
# check job resource usage with: seff <Jobid>
echo ' '
echo Job ID: $SLURM_JOBID
echo ' '

## Run notes:
