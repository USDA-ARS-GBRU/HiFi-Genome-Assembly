#!/bin/bash
#SBATCH -J HiFiASM
#SBATCH -p ceres
#SBATCH -A gbru_lima_collaboration
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=100G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/hifiasm.out
#SBATCH -e 00_log/hifiasm.err

cd $SLURM_SUBMIT_DIR

# write message to both stdout and stderr
write_log() { echo; echo ===== "$@" =====; echo; echo >&2; echo ===== "$@" ===== >&2; echo >&2; }

module load hifiasm/0.25.0

echo Infile: $infile
echo Sample: $sample
echo Output Directory: $oDir
echo Node: $SLURMD_NODENAME

mkdir -p ${oDir}/${sample}

hifiasm -t 32 -o ${oDir}/${sample}/${sample} $infile $infile2 

write_log 'hifiasm finished. Generating fasta file.'
# from Hifiasm FAQ to get contigs in FASTA
# https://hifiasm.readthedocs.io/en/latest/faq.html
for gfa in ${oDir}/${sample}/*.gfa; do
    name=`basename $gfa | rev | cut -d. -f2- | rev`
    write_log "GFA: $gfa | Name: $name"
    awk '/^S/{print ">"$2;print $3}' $gfa > ${oDir}/${sample}/${name}.fa
done

write_log 'fasta files generated. copying files.'
# copy hap1 and hap2 fasta files to main oDir
cp ${oDir}/${sample}/*.hap?.p_ctg.fa ${oDir}/

# attach the job ID to the log
# check job resource usage with: seff <Jobid>
write_log "Job ID: $SLURM_JOBID"

## Run notes:
## sbatch -o 00_log/hifiasm_${sample}.out -e 00_log/hifiasm_${sample}.err --export infile=pacbio,sample=sample,oDir=$oDir /project/gbru_lima_collaboration/analysis.roth/01_sbatch/hifiasm.sbatch