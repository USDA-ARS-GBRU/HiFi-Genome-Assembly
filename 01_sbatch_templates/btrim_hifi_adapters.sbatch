#!/bin/bash
#SBATCH -J btrim_hifi
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --mem=40G
#SBATCH -t 12:00:00
#SBATCH -o 00_log/btrim_hifi_%j.out
#SBATCH -e 00_log/btrim_hifi_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

: "${iFiles:?Set iFiles='03_reads_raw/*.fastq.gz'}"
: "${oDir:?Set oDir=04_reads_qc/btrim}"
: "${btrim_bin:?Set btrim_bin=/path/to/btrim}"
: "${patterns:?Set patterns=/path/to/btrim_patterns.txt}"

max_jobs="${max_jobs:-8}"
edit_distance="${edit_distance:-3}"

mkdir -p "${oDir}/adapter_detected" "${oDir}/adapter_free" "${oDir}/summary"

declare -A running_jobs

check_jobs() {
  for file in "${!running_jobs[@]}"; do
    pid="${running_jobs[$file]}"
    if ! kill -0 "$pid" 2>/dev/null; then
      unset 'running_jobs[$file]'
    fi
  done
}

for filepath in ${iFiles}; do
  name=$(basename "$filepath")
  prefix=${name%.fastq.gz}
  prefix=${prefix%.fq.gz}
  prefix=${prefix%.fastq}
  prefix=${prefix%.fq}

  if [ ! -s "${oDir}/adapter_free/${prefix}.adapter_free.fastq.gz" ]; then
    (
      echo "[START] ${name} at $(date)"
      "${btrim_bin}" \
        -p "${patterns}" \
        -t "${filepath}" \
        -o "${oDir}/adapter_detected/${prefix}.adapter_detected.fastq" \
        -K "${oDir}/adapter_free/${prefix}.adapter_free.fastq" \
        -3 \
        -e 0 \
        -v "${edit_distance}" \
        -s "${oDir}/summary/${prefix}.btrim_summary.txt" \
        > "${oDir}/summary/${prefix}.btrim_stdout.txt"

      gzip --fast "${oDir}/adapter_free/${prefix}.adapter_free.fastq"
      gzip --fast "${oDir}/adapter_detected/${prefix}.adapter_detected.fastq"
      echo "[FINISH] ${name} at $(date)"
    ) &
    running_jobs["$filepath"]=$!
  fi

  while [ "${#running_jobs[@]}" -ge "$max_jobs" ]; do
    sleep 30
    check_jobs
  done
done

wait

echo "Job ID: ${SLURM_JOBID}"

