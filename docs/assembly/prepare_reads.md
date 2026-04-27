# Prepare PacBio HiFi Reads

Read preparation should preserve the high accuracy and long-read structure of PacBio HiFi data. The default posture is conservative: inspect reads, document inputs, and avoid trimming unless there is evidence that trimming improves the assembly.

## Inputs

Common input formats:

```text
raw PacBio HiFi BAM
FASTQ or FASTQ.gz
sample sheet with read paths
```

Record the source instrument run, movie/cell identifiers if available, sample ID, cultivar, and any demultiplexing or CCS filtering already performed by the sequencing provider.

## BAM to FASTQ

If reads arrive as BAM, convert to FASTQ before workflows that expect FASTQ:

```bash
module load bamtools/2.5.2

bamtools convert \
  -format fastq \
  -in raw/sample.hifi.bam \
  -out 03_reads_raw/sample.fastq
```

PacBio-native options such as `pbtk` tools may be preferable when available on the cluster. Capture the command and version either way.

## Basic Read QC

Start with simple metrics:

```bash
seqkit stats -a 03_reads_raw/*.fastq.gz > 04_reads_qc/seqkit_raw_stats.tsv
```

Useful review outputs:

- total bases per sample
- read count
- read N50
- mean and median read length
- longest read
- estimated coverage
- read length histogram
- adapter/vector screening results
- contamination sketch results

FastQC can be informative, but many warnings assume short-read data and should not be treated as automatic failures for HiFi reads.

## Coverage

Estimate coverage as:

```text
coverage = total HiFi bases / expected haploid genome size
```

For many diploid crop assemblies, 25-40x HiFi is a practical lower range and 40-80x is common for robust projects. Polyploidy, heterozygosity, repeats, and budget can shift the target.

## Adapter and Artifact Screening

PacBio HiFi reads are normally high quality. Aggressive trimming can remove useful terminal sequence and reduce contiguity, so compare raw and filtered assemblies before applying trimming across a project.

Options:

| Tool | Use | Caution | Decision point |
| --- | --- | --- |
| fastplong | long-read adapter/quality cleanup | validate that assembly metrics improve | comparison-only unless it fixes a documented issue |
| btrim | explicit adapter-pattern screening/removal | use validated pattern files and long-read-capable build | useful for conservative adapter-free vs raw comparison |
| HiFiAdapterFilt | PacBio HiFi adapter contamination | designed for HiFi adapter artifacts; still inspect outputs | good choice when adapter contamination is suspected in reads |
| cutadapt | known adapter sequences | avoid broad trimming without evidence | only for known motifs with clear rationale |
| NCBI FCS-adaptor | adapter/vector screening for release candidates | assembly-level release screen; does not replace read-level review | required-style release evidence, not a read-prep shortcut |

HiFiAdapterFilt is especially relevant because published evaluations found adapter sequence in many public CCS datasets and showed downstream assembly artifacts. Use it as a targeted sanitation tool, then compare the filtered assembly against the raw-read assembly.

## btrim Conservative Mode

The most conservative `btrim` use is to separate reads with detected adapter sequence from reads with no detected adapter sequence, assemble the adapter-free reads, and compare against the raw-read assembly.

Important arguments:

| Argument | Meaning |
| --- | --- |
| `-p patterns.txt` | adapter pattern pairs |
| `-t reads.fastq.gz` | query reads |
| `-o reads_adapter_detected.fastq` | reads where adapter sequence was detected and trimmed |
| `-K reads_adapter_free.fastq` | reads with no detected adapter |
| `-3` | search/trim 3-prime end |
| `-e 0` | trim to first base after detection |
| `-v 3` | small edit distance to adapter pattern |
| `-s summary.txt` | summary counts |

Template:

```bash
sbatch \
  --export iFiles="03_reads_raw/*.fastq.gz",oDir=04_reads_qc/btrim,btrim_bin=/path/to/btrim,patterns=examples/btrim_patterns.example.txt,edit_distance=3 \
  01_sbatch/btrim_hifi_adapters.sbatch
```

Interpretation:

- If very few reads are flagged, compare raw and adapter-free assemblies before changing the workflow.
- If many reads are flagged, inspect the btrim summary and independently verify adapter motifs.
- Do not assume btrim replaces FCS-adaptor for release screening.
- Record the btrim binary/source, pattern file, edit distance, and command in the decision log.

## Read-Filtering Evidence Package

If any reads are removed or trimmed, keep:

- raw read statistics
- filtered read statistics
- number and percentage of reads affected
- adapter/vector motif source
- tool version and database or pattern file
- raw-read hifiasm assembly metrics
- filtered-read hifiasm assembly metrics
- BUSCO/Merqury comparison
- contamination/adaptor screening comparison

Filtering should make the assembly more defensible, not merely smaller or cleaner-looking.

## Decision Rule

Use raw HiFi reads unless filtering clearly improves the assembly or removes a documented artifact. Any filtering choice should be backed by before/after assembly metrics, BUSCO/Merqury results, dotplots, and contamination/adaptor review.
