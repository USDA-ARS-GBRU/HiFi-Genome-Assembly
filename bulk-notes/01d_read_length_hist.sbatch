#!/bin/bash
#SBATCH -J readLenHist
#SBATCH -p ceres
#SBATCH -A gbru_fy25_fusarium_tr4
#SBATCH -N 1
#SBATCH -n 11
#SBATCH --mem=5G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/01d_readLenHist.out
#SBATCH -e 00_log/01d_readLenHist.err

cd $SLURM_SUBMIT_DIR

# loads python env for histogram script
module load miniconda
source activate sandbox
# set histogram script path
plotHist='02_scripts/fastq_length_hist.py'

echo Infiles: $iFiles
echo Genome Length: $GL
echo Output Directory: $oDir
echo Node: $SLURMD_NODENAME

mkdir -p ${oDir}/00_lenHist

max_jobs=11
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
	name=`echo $filepath | cut -d/ -f2 | cut -d. -f1`

        if [ ! -s $oDir/00_lenHist/$name ]; then
                (
                echo "[START]  $name at $(date)"
                echo "Infile: $name"
                echo "Outfile: ${oDir}/${name}"
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
## sbatch --export iFiles=03b_PacBioHiFi.fastq.trim/*.fastq,oDir=03b_PacBioHiFi.fastq.trim,GL=46 01_sbatch/01d_read_length_hist.sbatch
