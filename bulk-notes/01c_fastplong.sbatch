#!/bin/bash
#SBATCH -J fastplong
#SBATCH -p ceres
#SBATCH -A gbru_fy25_fusarium_tr4
#SBATCH -N 1
#SBATCH -n 11
#SBATCH --mem=40G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/01c_fastp.out
#SBATCH -e 00_log/01c_fastp.err

cd $SLURM_SUBMIT_DIR

module load miniconda
source activate binf

echo Infiles: $iFiles
echo Output Directory: $oDir
echo Node: $SLURMD_NODENAME

mkdir -p ${oDir} ${oDir}/00_html ${oDir}/00_json

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
	name=$(basename $filepath)

	if [ ! -s $oDir/$name ]; then
        	(
            	echo "[START]  $name at $(date)"
            	echo "Infile: $name"
            	echo "Outfile: ${oDir}/${name}"
		fastplong -i $filepath -o $oDir/$name -h $oDir/00_html/$name.html -j $oDir/00_json/$name.json -5 -3
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

## Run log:
## sbatch --export iFiles=03a_PacBioHiFi.fastq/*.fastq,oDir=03b_PacBioHiFi.fastq.trim 01_sbatch/01c_fastplong.sbatch
