# PacBio Watchlist

This file records Pacific Biosciences resources that are relevant to PacBio HiFi crop genome assembly, read preparation, QC, and release readiness. Re-check these periodically because PacBio tool recommendations and repository activity change over time.

## Current Repositories to Watch

| Resource | Why it matters |
| --- | --- |
| https://github.com/PacificBiosciences | Organization-level repository list and announcements for PacBio tools. |
| https://github.com/PacificBiosciences/pbtk | PacBio BAM toolkit; includes `pbmerge`, `bam2fastq`, `bam2fasta`, `extracthifi`, `pbindex`, and `zmwfilter`. |
| https://github.com/PacificBiosciences/pbmm2 | PacBio minimap2 wrapper with PacBio-aware presets and native BAM output. Useful for read-to-assembly or assembly-to-reference alignment contexts. |
| https://github.com/PacificBiosciences/HiFi-human-assembly-WDL | Human-focused WDL, but useful for seeing PacBio-maintained de novo assembly workflow structure, reproducibility expectations, resource requests, and output categories. |
| https://github.com/PacificBiosciences/pb-assembly | Legacy PacBio assembly suite; useful historical context for PacBio assembly concepts, coverage language, and FALCON-era workflows. |

## Items to Monitor

- New PacBio repositories or releases mentioning whole-genome assembly, HiFi QC, adapter detection, read sanitation, contamination, or assembly evaluation.
- `pbtk` changes to `bam2fastq`, `pbmerge`, `extracthifi`, and `zmwfilter`.
- `pbmm2` preset changes for CCS/HiFi alignment.
- PacBio workflow changes that affect de novo assembly inputs, resource recommendations, or output metrics.
- Official statements about adapter handling, HiFi read filtering, or assembly QC.

## Current Protocol Implications

- Prefer `pbtk` for PacBio-native BAM merge/conversion when available, because PacBio maintains these utilities.
- Keep generic `bamtools` examples as a fallback for clusters that do not provide `pbtk`.
- Use PacBio-aware alignment tools such as `pbmm2` where native PacBio BAM handling or presets matter; use minimap2 directly when simpler FASTA/FASTQ workflows are enough.
- Treat PacBio human WDL workflows as a source of workflow-design ideas, not crop-specific truth.
- Continue to rely on crop-appropriate assembly evaluation: BUSCO, Merqury, dotplots, Hi-C maps, contamination checks, and release validation.
