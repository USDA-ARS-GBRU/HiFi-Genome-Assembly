#!/bin/bash
#SBATCH -J bam2fastq
#SBATCH -p ceres
#SBATCH -A gbru_fy25_fusarium_tr4
#SBATCH -N 1
#SBATCH -n 5
#SBATCH --mem=5G
#SBATCH -t 24:00:00
#SBATCH -o analysis.roth/00_log/01a_bam2fastq.out
#SBATCH -e analysis.roth/00_log/01a_bam2fastq.err

cd $SLURM_SUBMIT_DIR

# bamtools to convert bam file to fastq file
module load bamtools/2.5.2
# loads python env for histogram script
module load miniconda
source activate sandbox
# set histogram script path
plotHist='analysis.roth/02_scripts/fastq_length_hist.py'

echo Infiles: $iFiles
echo Genome Length: $GL
echo Output Directory: $oDir
echo Node: $SLURMD_NODENAME

mkdir -p ${oDir}/00_lenHist

max_jobs=5
declare -A running_jobs

# Function to check for finished jobs and update running list
check_jobs() {
    for file in "${!running_jobs[@]}"; do
        pid="${running_jobs[$file]}"
        if ! kill -0 "$pid" 2>/dev/null; then
            unset 'running_jobs[$file]'
        fi
    done
}

for filepath in $iFiles; do
        # Extract base info
	fx=`echo $filepath | cut -d/ -f1 | cut -d_ -f2`
	sx=`echo $filepath | cut -d. -f1 | cut -d_ -f5`
	bc=`echo $filepath | cut -d. -f3`
	name="$fx-$sx-$bc"

        if [ ! -s $oDir/$name ]; then
                (
                echo "[START]  $name at $(date)"
                echo "Infile: $name"
                echo "Outfile: ${oDir}/${name}"
		bamtools convert -format fastq -in $filepath -out ${oDir}/${name}.fastq
		python $plotHist -i ${oDir}/${name}.fastq -o ${oDir}/00_lenHist/${name}.pdf -gl $GL
                echo "[FINISH] $name at $(date)"
                ) &

                pid=$!
                running_jobs["$filepath"]=$pid
        fi

	while [ "${#running_jobs[@]}" -ge "$max_jobs" ]; do
                sleep 60
                check_jobs
        done

done

wait

# attach the job ID to the log
# check job resource usage with: seff <Jobid>
echo ' '
echo Job ID: $SLURM_JOBID
echo ' '

## Run notes:
## sbatch --export iFiles=Fusarium_F*/*.bam,oDir=analysis.roth/03a_PacBioHiFi.fastq,GL=46 analysis.roth/01_sbatch/01a_convert_bam_fastq.sbatch
