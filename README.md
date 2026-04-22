# PacBio HiFi Genome Assembly for Crop Plants

> [!NOTE]
> This repository is under active development. Suggestions, corrections, teaching examples, and issue reports are welcome through GitHub Issues or pull requests.

This repository is a modular, beginner-friendly, peer-review-oriented protocol for assembling crop plant genomes from PacBio HiFi reads, evaluating assembly quality, preparing annotation tracks, and getting the final product ready for public release through NCBI/INSDC and related community databases.

The protocol is designed as a practical representation of contemporary crop plant genome assembly work. It emphasizes transparent decisions, independent quality evidence, reproducible HPC execution, and release products that can withstand manuscript review, database validation, and reuse by breeding and genomics communities.

The protocol is intentionally written as a longform guide. A beginning bioinformatics graduate student should be able to follow the logic, not just copy commands.

## Guiding Principles

Plant genome assembly is not one command. Crop genomes often have large transposable element loads, recent duplications, residual heterozygosity, polyploidy, wild introgressions, organellar carryover, and reference-bias traps. The goal is not only to create a FASTA file; the goal is to produce an assembly that is biologically credible, computationally defensible, and ready for reuse.

This workflow favors:

- PacBio HiFi reads as the core assembly data.
- hifiasm as the default assembler.
- Optional Hi-C, trio, optical map, genetic map, or reference-guided scaffolding when appropriate.
- Multiple independent quality checks instead of one magic score.
- Conservative correction: break clear misassemblies, but do not erase real structural variation just because it disagrees with a reference.
- Reproducible HPC execution using modules, conda/mamba, pixi, containers, or direct installs.
- Clear logs, sample sheets, and release-ready metadata from the beginning.

## Table of Contents

1. [Workflow Overview](#workflow-overview)
2. [Project Layout](#project-layout)
3. [Software Setup](#software-setup)
4. [Input Data and Metadata](#input-data-and-metadata)
5. [Step 0: Choose Assembly Strategy](#step-0-choose-assembly-strategy)
6. [Step 1: Prepare Reads](#step-1-prepare-reads)
7. [Step 2: Estimate Genome Properties](#step-2-estimate-genome-properties)
8. [Step 3: Assemble with hifiasm](#step-3-assemble-with-hifiasm)
9. [Step 4: Convert and Organize hifiasm Outputs](#step-4-convert-and-organize-hifiasm-outputs)
10. [Step 5: Assembly Statistics](#step-5-assembly-statistics)
11. [Step 6: Reference and Self Alignment Dotplots](#step-6-reference-and-self-alignment-dotplots)
12. [Step 7: Haplotigs, Duplications, and Ploidy](#step-7-haplotigs-duplications-and-ploidy)
13. [Step 8: Misassembly Review and Correction](#step-8-misassembly-review-and-correction)
14. [Step 9: Chromosome-Scale Scaffolding](#step-9-chromosome-scale-scaffolding)
15. [Step 10: Telomeres, Centromeres, and Gap Status](#step-10-telomeres-centromeres-and-gap-status)
16. [Step 11: Contamination Screening](#step-11-contamination-screening)
17. [Step 12: Repeat Annotation and Masking](#step-12-repeat-annotation-and-masking)
18. [Step 13: Gene Annotation](#step-13-gene-annotation)
19. [Step 14: Final Quality Metrics](#step-14-final-quality-metrics)
20. [Step 15: NCBI and Community Database Release](#step-15-ncbi-and-community-database-release)
21. [Example sbatch Scripts](#example-sbatch-scripts)
22. [Development Roadmap](#development-roadmap)
23. [Key References and Tool Links](#key-references-and-tool-links)

## Current Version

Current roadmap version: **v0.3.0-dev**. See `VERSION` and `CHANGELOG.md`. v0.3 is still active, its release-readiness foundation is mostly in place, and early v0.4 curation material has started.

Completed baseline:

- **v0.1 Assembly Core**: longform protocol, reusable sbatch templates, starter metadata, hifiasm log parsing, and FASTA filtering/renaming helpers.
- **v0.2 QC Dashboard**: peer-review QC/report templates, release checklist, methods text template, release manifest, dashboard aggregation, and quick dashboard plotting.

Current focus:

- **v0.3 to v0.4 transition**: maintain validation/release helpers while starting dotplot and misassembly curation examples.

## Workflow Overview

The recommended first-pass workflow is:

```text
sample metadata
  -> raw PacBio HiFi BAM/FASTQ
  -> read QC and length/coverage summaries
  -> k-mer profiling with meryl/jellyfish + GenomeScope/Smudgeplot
  -> hifiasm assembly
  -> GFA to FASTA conversion
  -> contiguity stats + BUSCO + Merqury QV/completeness
  -> dotplots against reference and close assemblies
  -> contamination checks with BlobToolKit, sourmash, FCS, and adapter/vector screens
  -> optional correction and purging
  -> optional Hi-C or reference-guided scaffolding
  -> telomere/centromere/repeat/gene annotation
  -> final FASTA, AGP, GFF3, metadata, and NCBI submission package
```

For many diploid, inbred crop cultivars, the practical v0.1 target is a high-quality primary contig assembly. For a v1.0 release, the target should usually be chromosome-scale, QC-screened, repeat-annotated, and ready for GenBank, SRA, BioProject, BioSample, and organism-specific community databases.

## Project Layout

Create a new analysis directory for each species or project. The exact paths will vary by cluster, but keep the conceptual structure stable.

```bash
mkdir -p \
  00_metadata \
  00_log \
  01_sbatch \
  02_scripts \
  03_reads_raw \
  04_reads_qc \
  05_kmers \
  06_hifiasm \
  07_assemblies \
  08_stats \
  09_dotplots \
  10_scaffolding \
  11_contamination \
  12_telomere_centromere \
  13_repeats \
  14_genes \
  15_release
```

Use scratch for heavy intermediate files. hifiasm creates large `.bin`, `.gfa`, and overlap files. Do not run large crop assemblies from slow network storage unless your cluster explicitly recommends it.

Recommended metadata files:

```text
00_metadata/samples.tsv
00_metadata/references.tsv
00_metadata/sequencing_runs.tsv
00_metadata/assembly_decisions.md
00_metadata/release_metadata.md
```

Minimum `samples.tsv` columns:

```text
sample_id cultivar species taxon_id ploidy expected_genome_size_bp hifi_reads hic_read1 hic_read2 notes
```

Starter templates are available in:

```text
examples/samples.tsv
examples/references.tsv
```

Starter helper scripts are available in:

```text
scripts/collect_qc_dashboard.py
scripts/audit_fasta_headers.py
scripts/audit_gff3_fasta_ids.py
scripts/audit_release_manifest.py
scripts/check_release_bundle.py
scripts/extract_hifiasm_log_metrics.py
scripts/filter_rename_fasta.py
scripts/plot_qc_dashboard.py
scripts/split_fasta_at_breaks.py
scripts/summarize_corrections.py
scripts/summarize_organelle_hits.py
scripts/validate_breaks.py
scripts/validate_agp.py
scripts/validate_fasta.py
```

Example usage:

```bash
scripts/extract_hifiasm_log_metrics.py 00_log/hifiasm_*.err -o 08_stats/hifiasm_log_metrics.tsv

scripts/collect_qc_dashboard.py \
  --seqkit 08_stats/seqkit_assembly_stats.tsv \
  --hifiasm-logs 00_log/hifiasm_*.err \
  --busco 08_stats/busco/*/short_summary*.txt \
  --quast 08_stats/quast*/report.tsv \
  --bbtools 08_stats/*.bbtools_stats.txt \
  --fcs-adaptor 11_contamination/*fcs_adaptor*.txt \
  --fcs-gx 11_contamination/*fcs_gx*.txt \
  --telomere-summary examples/telomere_summary.tsv \
  --repeat-summary examples/repeat_summary.tsv \
  --annotation-summary examples/annotation_summary.tsv \
  -o 08_stats/assembly_qc_dashboard.tsv

scripts/plot_qc_dashboard.py \
  -i 08_stats/assembly_qc_dashboard.tsv \
  -o 08_stats/qc_plots

scripts/filter_rename_fasta.py \
  -i 07_assemblies/sample.primary.fa \
  -o 15_release/sample.filtered_renamed.fa \
  --min-length 200 \
  --prefix SampleID \
  --map 15_release/sample.filtered_renamed.id_map.tsv

scripts/validate_fasta.py \
  15_release/sample.filtered_renamed.fa \
  --min-length 200 \
  -o 15_release/sample.fasta_validation.tsv

scripts/validate_agp.py \
  15_release/sample.agp \
  -o 15_release/sample.agp_validation.tsv

scripts/check_release_bundle.py \
  --fasta 15_release/sample.filtered_renamed.fa \
  --agp 15_release/sample.agp \
  --manifest examples/release_manifest.tsv \
  --out-dir 15_release/validation

scripts/audit_gff3_fasta_ids.py \
  --fasta examples/annotation_validation/toy_genome.fsa \
  --gff3 examples/annotation_validation/toy_annotation.gff3 \
  -o /tmp/toy_annotation_id_audit.tsv

scripts/split_fasta_at_breaks.py \
  --fasta examples/toy/toy_assembly.fa \
  --breaks examples/toy/toy_breaks.tsv \
  -o /tmp/toy_split.fa \
  --map /tmp/toy_split.map.tsv

scripts/validate_breaks.py \
  --fasta examples/toy/toy_assembly.fa \
  --breaks examples/toy/toy_breaks.tsv \
  -o /tmp/toy_breaks_validation.tsv

scripts/summarize_corrections.py \
  --split-map /tmp/toy_split.map.tsv \
  --decision-log examples/toy/toy_correction_decisions.tsv \
  -o /tmp/toy_correction_summary.tsv \
  --markdown /tmp/toy_correction_summary.md
```

Review and release templates are available in:

```text
docs/assembly_decision_log_template.md
docs/agp_after_splitting.md
docs/annotation_validation_examples.md
docs/contamination_workflow.md
docs/correction_decision_log_template.md
docs/correction_report_examples.md
docs/dotplot_misassembly_curation.md
docs/dotplot_figures.md
docs/gene_annotation.md
docs/manual_correction_workflow.md
docs/ncbi_metadata_templates.md
docs/ncbi_submission.md
docs/organelle_workflow.md
docs/paf_dotplot_options.md
docs/pacbio_watchlist.md
docs/qc_figures.md
docs/qc_report_template.md
docs/ragtag_workflow.md
docs/repeat_annotation.md
docs/release_checklist.md
docs/review_standards.md
docs/tool_version_policy.md
docs/methods_text_template.md
examples/accession_tracking.tsv
examples/annotation_validation/
examples/dotplot_decisions.tsv
examples/release_manifest.tsv
examples/release_bundle/
examples/contamination_decisions.tsv
examples/btrim_patterns.example.txt
```

## Software Setup

No single installation method works everywhere. The protocol supports four styles: HPC modules, conda/mamba, pixi, and direct install or containers. See `docs/tool_version_policy.md` for the minimum version and command-capture expectations for review-quality releases.

### Option A: HPC Modules

Use modules when your cluster maintains current versions.

```bash
module avail hifiasm
module avail seqkit
module avail mummer
module avail busco
module avail samtools
module avail minimap2
```

Load the versions you used into every job log:

```bash
module load hifiasm/0.25.0
module load seqkit/2.4.0
module load mummer/4.0.0rc1
module load gnuplot/5.4.8

hifiasm --version
seqkit version
nucmer --version
```

### Option B: Conda or Mamba

Use mamba when possible; it resolves complex bioinformatics environments much faster than conda.

```bash
mamba create -n hifi-assembly -c conda-forge -c bioconda \
  hifiasm \
  seqkit \
  samtools \
  minimap2 \
  mummer4 \
  gnuplot \
  fastqc \
  fastp \
  filtlong \
  jellyfish \
  genomescope2 \
  busco \
  quast \
  merqury \
  purge_dups \
  ragtag \
  yahs \
  bwa \
  bedtools \
  blast \
  sourmash \
  python=3.11
```

For plant annotation work, use a separate environment or container. Repeat and gene annotation tools can have difficult dependencies.

```bash
mamba create -n plant-annotation -c conda-forge -c bioconda \
  edta \
  repeatmodeler \
  repeatmasker \
  braker3 \
  maker \
  augustus \
  genemark-et \
  liftoff \
  gffread \
  agat \
  busco \
  miniprot \
  diamond \
  trnascan-se \
  barrnap
```

### Option C: Pixi

Pixi is useful when you want a project-local, lockable environment.

```bash
pixi init
pixi add -c conda-forge -c bioconda hifiasm seqkit samtools minimap2 mummer4 gnuplot busco quast
pixi run hifiasm --version
```

### Option D: Direct Install or Containers

Some tools are easiest as binaries or containers:

- hifiasm can be compiled directly from GitHub.
- NCBI FCS commonly runs through Singularity/Apptainer or Docker.
- EDTA, BRAKER3, and MAKER may be more stable in containers on some systems.

Always record the exact command, version, and container digest if available.

## Input Data and Metadata

PacBio HiFi data may arrive as:

- `.bam` files from the sequencing facility.
- `.fastq.gz` files exported from SMRT Link or a collaborator.
- Multiple read files per sample, sometimes split by SMRT Cell, barcode, or sequencing run.

Do not merge everything blindly. First answer:

- Which files belong to the same biological sample?
- Are barcodes unique?
- Are there obvious low-yield runs that should be excluded?
- Are there multiple genotypes under one project?
- Is the material inbred, heterozygous, clonally propagated, or polyploid?
- Is organellar DNA expected to be high?
- Is Hi-C available from the same genotype and tissue?

For crop plants, write these answers in `00_metadata/assembly_decisions.md`. Future users need to know why a primary assembly, phased haplotypes, or chromosome-level scaffold was chosen.

## Step 0: Choose Assembly Strategy

### Common Strategies

| Data and biology | Recommended strategy | Why |
| --- | --- | --- |
| Inbred diploid cultivar, HiFi only | hifiasm primary assembly | Usually clean and simple; primary contigs are easy to use downstream. |
| Heterozygous diploid, HiFi only | hifiasm primary + alternate or partially phased outputs | Preserves more allelic sequence; check for duplicated haplotigs. |
| Heterozygous diploid with Hi-C | hifiasm Hi-C integrated phasing, then scaffold haplotypes | Produces more haplotype-resolved assemblies, but requires careful validation. |
| Trio or known parents available | hifiasm trio mode | Strongest phasing when parental short reads are available. |
| Polyploid crop | start with hifiasm, inspect k-mers, consider subgenome-aware workflows | Polyploid peaks and homeologs complicate "haploid" reference assumptions. |
| Crop with close reference and no Hi-C | hifiasm contigs plus conservative RagTag scaffold/correct review | Useful, but can introduce reference bias. |
| T2T goal | HiFi + ONT ultra-long + Hi-C/optical maps/manual curation | HiFi alone may not span long satellites and centromeres. |

### hifiasm Output Choices

hifiasm outputs graphs in GFA format. Depending on mode, you may see:

- `*.bp.p_ctg.gfa`: primary contigs.
- `*.bp.a_ctg.gfa`: alternate contigs.
- `*.bp.hap1.p_ctg.gfa` and `*.bp.hap2.p_ctg.gfa`: haplotype-resolved contigs.

For inbred crops, the primary contig assembly is often the practical starting point. For heterozygous or clonally propagated crops, do not discard haplotype assemblies until you compare size, BUSCO duplication, Merqury spectra, and dotplots.

### Parameter Philosophy

Start with hifiasm defaults unless you have a clear biological reason to change them. hifiasm defaults are strong for HiFi reads. Premature parameter tuning often causes more trouble than it solves.

Parameters worth understanding:

- `-t`: threads.
- `-o`: output prefix.
- `-l0`: disables haplotig purging; useful to test highly inbred or odd k-mer cases, but not always better.
- `--hom-cov`: manually sets homozygous coverage when hifiasm mis-detects the peak.
- `--h1/--h2`: paired-end Hi-C reads for integrated phasing.
- trio mode options: use when parental reads are available.

## Step 1: Prepare Reads

### Convert BAM to FASTQ

If reads arrive as BAM:

```bash
module load bamtools/2.5.2

bamtools convert \
  -format fastq \
  -in raw/sample.subreads_or_hifi.bam \
  -out 03_reads_raw/sample.fastq
```

For many files, use a sample sheet rather than hand-written loops once this repo matures. For now, a simple loop is acceptable:

```bash
for bam in ../RawData/*/*.bam; do
  sample=$(basename "$(dirname "$bam")")
  file=$(basename "$bam" .bam)
  sbatch \
    -o 00_log/bam2fastq_${sample}_${file}.out \
    -e 00_log/bam2fastq_${sample}_${file}.err \
    --export infile="$bam",sample="$file",oDir="03_reads_raw/$sample" \
    01_sbatch/bam2fastq.sbatch
done
```

### Read QC

Run basic stats first:

```bash
seqkit stats -a 03_reads_raw/*.fastq.gz > 04_reads_qc/seqkit_raw_stats.tsv
```

FastQC can be useful, but remember that it was designed around short-read assumptions. Warnings are not automatically failures for HiFi reads.

```bash
fastqc -t 8 -o 04_reads_qc/fastqc_raw 03_reads_raw/*.fastq.gz
```

Useful QC outputs:

- total bases per sample
- read count
- read N50
- mean/median read length
- longest read
- estimated coverage
- read length histogram
- adapter/vector hits
- contamination sketch results

### Adapter Trimming

PacBio HiFi reads should already be high quality. Avoid aggressive trimming unless you have evidence of adapters or bad run-specific artifacts.

Possible tools:

- `fastplong` for long-read adapter/quality cleanup.
- `btrim` for explicit adapter-pattern screening/removal when a validated long-read-capable build and adapter pattern file are available.
- `HiFiAdapterFilt` for PacBio HiFi adapter contamination.
- `cutadapt` for known adapter sequences.
- NCBI FCS-adaptor on the assembly before submission.

Empirically test trimming before applying it project-wide. In many HiFi plant projects, raw HiFi reads already assemble well; unnecessary trimming can reduce total read length, remove informative terminal sequence, and occasionally reduce contiguity. A defensible approach is to compare raw and trimmed assemblies for one representative sample, then choose the strategy supported by assembly size, contiguity, BUSCO, Merqury, and dotplot evidence.

Example:

```bash
fastplong \
  -i 03_reads_raw/sample.fastq.gz \
  -o 04_reads_qc/sample.fastplong.fastq.gz \
  -h 04_reads_qc/sample.fastplong.html \
  -j 04_reads_qc/sample.fastplong.json \
  -5 -3
```

### btrim Option for HiFi Adapter Screening

`btrim` is a fast adapter and quality trimming program originally described by Kong (2011). It can be used as an optional HiFi read sanitation step when you have a build that supports the read lengths in your data and a validated PacBio adapter pattern file. In this workflow, the most conservative btrim use is to separate reads with detected adapter sequence from reads with no detected adapter sequence, then assemble the adapter-free reads and compare against the raw-read assembly.

Important btrim logic:

- `-p patterns.txt`: adapter pattern pairs.
- `-t reads.fastq.gz`: query reads.
- `-o reads_adapter_detected.fastq`: reads where adapter sequence was detected and trimmed.
- `-K reads_adapter_free.fastq`: reads with no detected adapter; these are the conservative passing reads for assembly.
- `-3`: search/trim the 3-prime end.
- `-e 0`: trim to the first base after detection.
- `-v 3`: allow a small edit distance to the adapter pattern; tune only with evidence.
- `-s summary.txt`: write summary counts.

Example:

```bash
sbatch \
  --export iFiles="03_reads_raw/*.fastq.gz",oDir=04_reads_qc/btrim,btrim_bin=/path/to/btrim,patterns=examples/btrim_patterns.example.txt,edit_distance=3 \
  01_sbatch/btrim_hifi_adapters.sbatch
```

Interpretation:

- If very few reads are flagged, compare raw and adapter-free assemblies before changing the production workflow.
- If many reads are flagged, inspect the btrim summary, BLAST/locate adapter motifs, and run FCS-adaptor on the downstream assembly.
- Do not assume btrim replaces FCS-adaptor; NCBI screening still matters for release.
- Record the btrim binary/source, compile settings, pattern file, and command in `00_metadata/tool_versions.tsv` and the assembly decision log.

### Coverage Calculation

Coverage is:

```text
coverage = total HiFi bases / expected haploid genome size
```

For example:

```text
30 Gb HiFi reads / 1.0 Gb genome = 30x
```

Target coverage depends on genome size, heterozygosity, and budget, but 25-40x HiFi is often a practical minimum for many diploid plant assemblies, while 40-80x is common for robust crop projects. Very high coverage can help, but can also increase compute cost and make heterozygosity/polyploid signals more complex.

## Step 2: Estimate Genome Properties

Before assembly, estimate genome size, heterozygosity, repeats, and ploidy signal from k-mers.

### meryl + GenomeScope

Merqury uses `meryl`, so using meryl early makes sense.

```bash
meryl k=21 count output 05_kmers/sample.k21.meryl 03_reads_raw/sample.fastq.gz
meryl histogram 05_kmers/sample.k21.meryl > 05_kmers/sample.k21.hist
```

Upload the histogram to GenomeScope 2.0 or run a local GenomeScope installation.

Record:

- estimated genome size
- heterozygosity
- repeat content
- main k-mer peak
- whether the model fit looks believable

For polyploid crops, also use Smudgeplot when ploidy or subgenome structure is uncertain.

### Standardized Heterozygosity from Haplotype Assemblies

When high-quality haplotype-level assemblies are available for the same individual, use the USDA-ARS-GBRU [StandardizedHeterozygosityEvaluation](https://github.com/USDA-ARS-GBRU/StandardizedHeterozygosityEvaluation) approach as an optional standardized estimate of percent heterozygosity.

Conceptual workflow:

1. Align haplotype assembly 1 and haplotype assembly 2 with MUMmer `nucmer`.
2. Extract non-repetitive SNPs with `show-snps -Clr`.
3. Count SNP records, excluding the `show-snps` header lines.
4. Divide the SNP count by organism genome size.
5. Multiply by 100 to report percent heterozygosity.

Example:

```bash
module load mummer

ref=07_assemblies/sample.hap1.fa
query=07_assemblies/sample.hap2.fa
out=05_kmers/sample.hap1_vs_hap2
genome_size=1000000000

nucmer --prefix="${out}" "${ref}" "${query}"
show-snps -Clr "${out}.delta" > "${out}.nonrepeat.snps"

total_lines=$(wc -l < "${out}.nonrepeat.snps")
snp_count=$((total_lines - 5))
awk -v snps="${snp_count}" -v genome="${genome_size}" \
  'BEGIN { printf "percent_heterozygosity\t%.6f\n", (snps / genome) * 100 }'
```

Use this estimate with care:

- It requires reliable haplotype assemblies from the same individual.
- It measures SNP differences captured between assembled haplotypes, not all possible heterozygous variation.
- It is most comparable across projects when the same alignment, SNP extraction, repeat handling, and genome-size assumptions are used.
- It complements k-mer approaches such as GenomeScope/Smudgeplot, which estimate heterozygosity directly from reads before assembly.

### Jellyfish Alternative

```bash
jellyfish count -C -m 21 -s 10G -t 32 \
  -o 05_kmers/sample.jf \
  <(zcat 03_reads_raw/sample.fastq.gz)

jellyfish histo -t 32 05_kmers/sample.jf > 05_kmers/sample.jf.hist
```

### Interpreting hifiasm Coverage Peaks

hifiasm logs do not usually print a friendly "coverage = X" line. Instead, inspect:

```bash
grep -E "collected|genome size|peak_hom|peak_het|peak" 00_log/hifiasm_sample.err
```

Useful values:

- total collected bases
- estimated genome size
- `peak_hom`
- `peak_het`

For highly inbred lines, a strong homozygous peak and weak/no heterozygous peak is expected. For heterozygous diploids, a heterozygous peak near half the homozygous peak can be normal. For polyploids, multiple peaks may represent allele dosage and homeologous structure.

## Step 3: Assemble with hifiasm

### Basic HiFi-Only Assembly

```bash
hifiasm \
  -t 32 \
  -o 06_hifiasm/sample/sample \
  03_reads_raw/sample.fastq.gz \
  2> 00_log/hifiasm_sample.err
```

If a sample has multiple FASTQ files:

```bash
hifiasm \
  -t 32 \
  -o 06_hifiasm/sample/sample \
  03_reads_raw/sample_run1.fastq.gz \
  03_reads_raw/sample_run2.fastq.gz \
  2> 00_log/hifiasm_sample.err
```

### Hi-C Integrated hifiasm Assembly

Use this when Hi-C reads are from the same individual/genotype and you want phased assemblies.

```bash
hifiasm \
  -t 48 \
  -o 06_hifiasm/sample_hic/sample_hic \
  --h1 hic_R1.fastq.gz \
  --h2 hic_R2.fastq.gz \
  03_reads_raw/sample.fastq.gz \
  2> 00_log/hifiasm_sample_hic.err
```

hifiasm does not perform final chromosome scaffolding. After Hi-C integrated phasing, use a scaffolder such as YaHS, SALSA2, or 3D-DNA/Juicer on the haplotype contigs.

### Inbred or Odd Samples: Test `-l0`

For inbred/homozygous genomes, hifiasm documentation notes that `-l0` disables purging. This can be useful as a diagnostic, not necessarily as the final assembly.

```bash
hifiasm \
  -t 32 \
  -l0 \
  -o 06_hifiasm/sample_l0/sample_l0 \
  03_reads_raw/sample.fastq.gz \
  2> 00_log/hifiasm_sample_l0.err
```

Compare default and `-l0` assemblies using assembly size, contig count, BUSCO duplication, Merqury spectra, and dotplots.

### Memory and Runtime

For crop plants, start conservatively:

| Genome size | Initial hifiasm request |
| --- | --- |
| < 500 Mb | 16-32 CPUs, 64-128G |
| 500 Mb - 1.5 Gb | 32 CPUs, 128-300G |
| 1.5 - 5 Gb | 32-64 CPUs, 300-750G |
| > 5 Gb or polyploid | 64+ CPUs, highmem node, test subset first |

These are starting points, not guarantees. Always inspect `seff`, `sacct`, or your cluster's accounting tools after jobs finish.

## Step 4: Convert and Organize hifiasm Outputs

hifiasm emits GFA. Convert GFA segment records to FASTA:

```bash
for gfa in 06_hifiasm/sample/*.gfa; do
  name=$(basename "$gfa" .gfa)
  awk '/^S/{print ">"$2; print $3}' "$gfa" > "07_assemblies/${name}.fa"
done
```

Recommended naming:

```text
07_assemblies/sample.primary.fa
07_assemblies/sample.alternate.fa
07_assemblies/sample.hap1.fa
07_assemblies/sample.hap2.fa
```

Keep raw hifiasm outputs in `06_hifiasm/`. Keep renamed, analysis-ready FASTA files in `07_assemblies/`.

## Step 5: Assembly Statistics

Run at least two stat tools because they report slightly different summaries.

### seqkit

```bash
seqkit stats -a 07_assemblies/*.fa > 08_stats/seqkit_assembly_stats.tsv
```

### BBTools stats.sh

```bash
stats.sh in=07_assemblies/sample.primary.fa format=3 -Xmx4g > 08_stats/sample.primary.bbtools_stats.txt
```

### QUAST

QUAST is useful for N50, NG50 if genome size is known, misassembly signals against a reference, and general reporting.

```bash
quast.py \
  -t 16 \
  -o 08_stats/quast_sample \
  --large \
  --est-ref-size 1000000000 \
  07_assemblies/sample.primary.fa
```

If a close reference exists:

```bash
quast.py \
  -t 16 \
  -o 08_stats/quast_sample_ref \
  -r references/close_reference.fa \
  --large \
  07_assemblies/sample.primary.fa
```

Do not let reference-based QUAST scores override biological evidence. A crop accession may contain real inversions, introgressions, or presence/absence variation.

## Step 6: Reference and Self Alignment Dotplots

Dotplots are one of the best ways to teach assembly judgment. They reveal collinearity, inversions, duplicated haplotigs, translocations, and potential misjoins.

### MUMmer/nucmer Dotplot

```bash
nucmer \
  -t 16 \
  -c 100 \
  -p 09_dotplots/ref_vs_sample \
  references/close_reference.fa \
  07_assemblies/sample.primary.fa

delta-filter \
  -i 90 \
  -l 10000 \
  -1 \
  09_dotplots/ref_vs_sample.delta \
  > 09_dotplots/ref_vs_sample.filter

show-coords -r -c -l \
  09_dotplots/ref_vs_sample.filter \
  > 09_dotplots/ref_vs_sample.coords

mummerplot \
  -p 09_dotplots/ref_vs_sample.plot \
  -R references/close_reference.fa \
  --postscript \
  --large \
  --layout \
  --fat \
  09_dotplots/ref_vs_sample.filter
```

Parameter logic:

- `-c 100`: minimum cluster length. Good first pass for whole-genome alignments.
- `-i 90`: keep alignments >= 90% identity. Use higher for very close cultivars.
- `-l 10000`: ignore tiny alignments; helps reduce repeat noise in plant genomes.
- `-1`: keep a best one-to-one alignment chain; cleaner for visual inspection.

For divergent species, reduce identity or use minimap2 `-x asm10`/`asm20` and dotplot with `pafr`, `plotsr`, or custom scripts.

### How to Read MUMmer Plots

In common MUMmer plot coloring:

- Forward/same-orientation alignments form positive-slope diagonals.
- Reverse-orientation alignments form negative-slope diagonals and may indicate inversions.
- Long clean diagonals indicate collinearity.
- Broken diagonals can indicate contig breaks, real structural variation, or misassembly.
- Dense clusters often represent repeats, centromeres, segmental duplications, or over-alignment.

Do not automatically "fix" every difference from the reference. Aggressive reference-guided correction can make dotplots look cleaner while introducing excessive breaks or erasing real cultivar-specific structural variation. Treat a cleaner reference-alignment plot as one line of evidence, not as proof that the assembly is more biologically accurate.

## Step 7: Haplotigs, Duplications, and Ploidy

Signs of haplotig duplication:

- assembly size much larger than expected
- BUSCO duplicated score high
- primary assembly contains many short alternate-like contigs
- k-mer spectra show assembly-only duplications
- dotplot shows parallel duplicate alignments

Tools:

- hifiasm built-in purging/default behavior
- purge_dups
- purge_haplotigs
- Merqury spectra-cn plots
- BUSCO duplication
- coverage mapping of HiFi reads back to assembly

### Map HiFi Reads Back

```bash
minimap2 -ax map-hifi -t 32 \
  07_assemblies/sample.primary.fa \
  03_reads_raw/sample.fastq.gz \
  | samtools sort -@ 8 -o 08_stats/sample.hifi_to_assembly.bam

samtools index 08_stats/sample.hifi_to_assembly.bam
samtools coverage 08_stats/sample.hifi_to_assembly.bam > 08_stats/sample.hifi_coverage.tsv
```

Coverage interpretation:

- Contigs at half expected coverage may be haplotigs in a primary assembly.
- Contigs at very high coverage may be collapsed repeats or organellar sequence.
- Contigs with very low coverage may be contamination, assembly artifacts, or rare organellar fragments.

### Purge Duplicates Carefully

If purging is needed:

```bash
minimap2 -x map-hifi -t 32 sample.fa reads.fastq.gz | gzip -c > sample.paf.gz
pbcstat sample.paf.gz
calcuts PB.stat > cutoffs 2> calcuts.log
split_fa sample.fa > sample.split
minimap2 -xasm5 -DP -t 32 sample.split sample.split | gzip -c > sample.split.self.paf.gz
purge_dups -2 -T cutoffs -c PB.base.cov sample.split.self.paf.gz > dups.bed
get_seqs -e dups.bed sample.fa
```

Treat purged outputs as candidates. Re-run BUSCO, Merqury, and dotplots before accepting.

## Step 8: Misassembly Review and Correction

Misassembly correction should be conservative and evidence-based.

Evidence types:

- MUMmer/minimap whole-genome alignments
- HiFi read mapping across suspected breakpoints
- Hi-C contact map
- optical map or Bionano map
- genetic map
- agreement across related assemblies
- telomere/centromere orientation
- coverage changes

### RagTag Correct and Scaffold

RagTag is useful but can introduce reference bias. Use it as a candidate generator, not an oracle.

Reference-guided correction:

```bash
ragtag.py correct \
  -t 32 \
  --mm2-params "-x asm5 -t 32" \
  --remove-small \
  --min-aln 10000 \
  -o 10_scaffolding/sample.ragtag_correct \
  references/close_reference.fa \
  07_assemblies/sample.primary.fa
```

Reference-guided scaffolding:

```bash
ragtag.py scaffold \
  -t 32 \
  -C \
  -r \
  -f 1000 \
  --remove-small \
  -o 10_scaffolding/sample.ragtag_scaffold \
  references/close_reference.fa \
  07_assemblies/sample.primary.fa
```

Notes from the soybean work:

- Default correction made very clean dotplots but introduced too many breaks.
- `--inter` and larger break thresholds reduced break count but missed some intra-chromosomal issues.
- Read validation helped but still required manual review.
- Some "errors" may be real structural variation.

### Manual Breaks

If a contig must be manually split:

1. Define the breakpoint with coordinates and evidence.
2. Save the original contig ID and coordinates.
3. Split with a scripted, reproducible command.
4. Add an entry to `00_metadata/assembly_decisions.md`.
5. Re-run stats, BUSCO, Merqury, dotplots, and contamination checks.

Never edit FASTA manually in a text editor for a release assembly.

## Step 9: Chromosome-Scale Scaffolding

Contig assemblies are useful; chromosome-level assemblies are often expected for crop references.

### Hi-C Scaffolding

Recommended current tools:

- YaHS: fast, accurate, widely used in recent large-genome workflows.
- 3D-DNA + Juicebox/JBAT: strong visual curation ecosystem.
- SALSA2: older but still used.
- ALLHiC: useful for polyploids in some contexts.

Generic YaHS workflow:

```bash
bwa index 07_assemblies/sample.primary.fa

bwa mem -5SP -t 32 \
  07_assemblies/sample.primary.fa \
  hic_R1.fastq.gz hic_R2.fastq.gz \
  | samtools view -b -@ 8 \
  | samtools sort -@ 8 -o 10_scaffolding/sample.hic.bam

samtools index 10_scaffolding/sample.hic.bam

yahs \
  07_assemblies/sample.primary.fa \
  10_scaffolding/sample.hic.bam \
  -o 10_scaffolding/sample.yahs
```

Convert YaHS outputs to `.hic` for Juicebox review using the YaHS helper scripts and Juicer tools. Review contact maps for:

- strong chromosome blocks
- off-diagonal translocation signals
- sudden coverage/contact drops
- contig orientation errors
- small unplaced contigs that should remain unplaced

### Reference-Guided Scaffolding

Use when Hi-C is absent and a close, high-quality reference exists. Be explicit that it is reference-guided.

Risks:

- real inversions may be forced into reference orientation
- introgressions may be misplaced
- presence/absence regions may be collapsed or orphaned
- cultivar-specific chromosome structure may be hidden

### Genetic Map or Optical Map

Use when available, especially for crops with strong breeding maps. These data can validate chromosome order independently of sequence similarity.

## Step 10: Telomeres, Centromeres, and Gap Status

Telomere and centromere annotation helps answer whether chromosomes are complete and correctly oriented.

### Telomeres

Most plants use the canonical telomeric repeat `TTTAGGG/CCCTAAA`, but exceptions exist. Confirm the expected repeat for your lineage.

Tools:

- tidk: identifies telomeric repeats in reads or assemblies and can find motifs de novo.
- quarTeT: T2T-oriented toolkit with telomere and centromere modules.
- seqkit locate: quick known-motif scan.

Known motif scan:

```bash
seqkit locate \
  -i \
  -p TTTAGGG \
  07_assemblies/sample.primary.fa \
  > 12_telomere_centromere/sample.TTTAGGG.locations.tsv
```

tidk known-repeat scan:

```bash
tidk search \
  --string TTTAGGG \
  --output 12_telomere_centromere/sample.tidk \
  07_assemblies/sample.primary.fa
```

Interpretation:

- Telomere signal at both ends of a chromosome-scale scaffold supports completeness.
- Signal at one end means one telomere captured.
- Internal telomere signal can indicate a misjoin, nested chromosome fusion, true interstitial telomeric repeat, or untrimmed artifact.

### Centromeres

Plant centromeres are repeat-rich and lineage-specific. There may be no simple universal motif.

Tools and strategies:

- quarTeT CentroMiner/CentroMatcher.
- Tandem Repeat Finder.
- RepeatModeler/EDTA repeat landscapes.
- Hi-C contact map patterns.
- CENH3 ChIP-seq if available.

Record centromere evidence as a track, not as absolute truth unless you have experimental support.

### Gaps

For scaffolded assemblies, distinguish:

- real unresolved gaps represented by Ns
- RagTag/YaHS scaffold gaps
- unknown-size gaps
- telomere-to-telomere chromosomes with no gaps

NCBI submission may require AGP information and correct gap feature handling for annotated scaffolds.

## Step 11: Contamination Screening

Contamination checks should happen before and after assembly.

### Read-Level Screening

Useful tools:

- sourmash sketches against NCBI or custom databases
- Kraken2/Centrifuge for taxonomic classification
- GC/tetranucleotide plots
- read mapping to organelle genomes

sourmash example:

```bash
sourmash sketch dna \
  -p k=51,scaled=1000,abund \
  -o 11_contamination/sample.k51.sig \
  03_reads_raw/sample.fastq.gz

sourmash search \
  11_contamination/sample.k51.sig \
  ncbi-euks-plants-2025.01.dna.k=51.sig.zip \
  --containment \
  --estimate-ani-ci \
  -n 20 \
  -o 11_contamination/sample.sourmash_search.csv
```

### Assembly-Level Screening

Recommended:

- NCBI FCS-adaptor for adapters/vectors.
- NCBI FCS-GX for foreign organism contamination.
- BlobToolKit for interactive GC/coverage/taxonomy review.
- BLAST against organelle, vector, bacterial, fungal, and human databases if needed.

NCBI now recommends running FCS before genome submission. FCS includes adaptor/vector screening and cross-species contamination screening.

### BlobToolKit Conceptual Workflow

BlobToolKit works best with:

- assembly FASTA
- read coverage BAM
- taxonomic hits
- BUSCO results

The output helps identify contigs with unusual GC, coverage, or taxonomy. For plant genomes, likely categories include:

- chloroplast contigs
- mitochondrial contigs
- bacteria/fungi/endophytes
- adapters/vectors
- low-coverage assembly artifacts
- true horizontally transferred or symbiotic sequence, which requires careful interpretation

## Step 12: Repeat Annotation and Masking

Repeat annotation is essential for crop plants. Transposable elements can dominate plant genomes and strongly affect gene prediction.

### Recommended Strategy

1. Build a de novo repeat library.
2. Classify transposable elements.
3. Combine de novo library with curated databases where appropriate.
4. Soft-mask the genome for gene annotation.
5. Produce repeat summary tables and GFF/BED tracks.

### EDTA

EDTA is plant-friendly and widely used for de novo TE annotation.

```bash
EDTA.pl \
  --genome 07_assemblies/sample.primary.fa \
  --species others \
  --step all \
  --sensitive 1 \
  --anno 1 \
  --threads 32
```

Parameter logic:

- `--species others`: use when not maize/rice-specific.
- `--sensitive 1`: slower but better for complex plant genomes.
- `--anno 1`: produces whole-genome TE annotation after library construction.

### RepeatModeler2 + RepeatMasker

RepeatModeler2 is a strong general de novo repeat library builder.

```bash
BuildDatabase \
  -name sample_repeatdb \
  07_assemblies/sample.primary.fa

RepeatModeler \
  -database sample_repeatdb \
  -threads 32 \
  -LTRStruct

RepeatMasker \
  -pa 32 \
  -lib sample_repeatdb-families.fa \
  -xsmall \
  -gff \
  07_assemblies/sample.primary.fa
```

Use soft masking (`-xsmall`) for gene annotation so repeats are lowercase rather than replaced by Ns.

### Repeat Deliverables

Save:

```text
13_repeats/sample.repeat_library.fa
13_repeats/sample.repeatmasker.gff
13_repeats/sample.repeat_summary.tsv
13_repeats/sample.softmasked.fa
```

## Step 13: Gene Annotation

Genome annotation quality depends on evidence. The best crop annotations combine:

- soft-masked genome
- RNA-seq from diverse tissues/conditions
- Iso-Seq full-length transcripts if available
- proteins from closely related species
- curated community gene models when available
- ab initio prediction

### Annotation Strategy Options

| Situation | Recommended tools |
| --- | --- |
| Closely related annotated reference exists | Liftoff + evidence cleanup, then BRAKER/MAKER support |
| RNA-seq and proteins available | BRAKER3 or MAKER |
| Iso-Seq available | collapse transcripts, align with minimap2/GMAP, feed into MAKER/BRAKER |
| Need fast first pass | BRAKER3 with proteins from OrthoDB/related species |
| Community annotation release | MAKER/Braker + manual QC + functional annotation |

### Liftoff

Use for annotation transfer between closely related cultivars/species.

```bash
liftoff \
  -g reference.gff3 \
  -o 14_genes/sample.liftoff.gff3 \
  -p 16 \
  13_repeats/sample.softmasked.fa \
  reference.fa
```

Liftoff is not a replacement for de novo annotation when the genome is structurally divergent, but it is very useful for crop pan-genome projects and cultivar comparisons.

### BRAKER3

BRAKER3 can use RNA-seq and protein evidence.

```bash
braker.pl \
  --genome=13_repeats/sample.softmasked.fa \
  --bam=rnaseq_alignments.bam \
  --prot_seq=related_species_proteins.fa \
  --species=sample_species_name \
  --threads=32 \
  --gff3 \
  --workingdir=14_genes/braker3_sample
```

### MAKER

MAKER is flexible and good for integrating many evidence types, though setup is more involved.

Typical inputs:

- genome FASTA
- repeat library
- protein evidence
- transcript evidence
- SNAP/AUGUSTUS training outputs

### Functional Annotation

After gene prediction:

- InterProScan for protein domains.
- eggNOG-mapper for orthology/function.
- DIAMOND BLASTP against curated plant protein sets.
- tRNAscan-SE for tRNAs.
- barrnap or RNAmmer-style tools for rRNAs.
- BUSCO on predicted proteins.

### Annotation QC

Check:

- number of genes
- number of transcripts per gene
- BUSCO protein score
- AED/QI if using MAKER
- gene length and exon count distributions
- internal stop codons
- partial genes
- contamination-derived genes
- TE-derived overprediction
- NCBI table2asn validation errors

## Step 14: Final Quality Metrics

No single metric proves an assembly is good. Report a dashboard.

### Required Dashboard

| Category | Metrics |
| --- | --- |
| Input reads | total bases, read N50, estimated coverage, k-mer profile |
| Contiguity | total length, contig/scaffold count, N50, L50, largest contig/scaffold |
| Completeness | BUSCO genome score with lineage |
| Base accuracy | Merqury QV and k-mer completeness |
| Structural quality | dotplots, Hi-C map, Inspector/read support if used |
| Duplication | BUSCO duplicated, Merqury spectra-cn, purge report |
| Contamination | FCS-adaptor, FCS-GX, BlobToolKit/sourmash |
| Organelle handling | chloroplast/mitochondrial contigs identified or excluded |
| Telomeres | terminal telomere count per chromosome |
| Annotation | repeat %, gene count, BUSCO protein score, functional annotation rate |

### BUSCO

Use the closest appropriate plant lineage. For broad plant assemblies, `embryophyta_odb12` is often useful; for legumes or grasses, use a closer lineage if available.

```bash
busco \
  -i 07_assemblies/sample.primary.fa \
  -m genome \
  -l embryophyta_odb12 \
  -o sample.primary.busco \
  --out_path 08_stats/busco \
  -c 32
```

Interpretation:

- High complete single-copy BUSCOs support completeness.
- High duplicated BUSCOs may reflect biology (polyploidy, recent duplication) or assembly redundancy.
- Missing BUSCOs may indicate real gene loss, fragmented assembly, contamination filtering mistakes, or wrong lineage.

### Merqury

Merqury estimates QV and completeness from read k-mers without needing a reference.

```bash
meryl k=21 count output 05_kmers/sample.reads.meryl 03_reads_raw/sample.fastq.gz

merqury.sh \
  05_kmers/sample.reads.meryl \
  07_assemblies/sample.primary.fa \
  08_stats/merqury_sample
```

For phased assemblies:

```bash
merqury.sh \
  05_kmers/sample.reads.meryl \
  07_assemblies/sample.hap1.fa \
  07_assemblies/sample.hap2.fa \
  08_stats/merqury_sample_haps
```

### Inspector

Inspector maps long reads back to the assembly and reports structural and small-scale errors. Use it when you need read-supported error localization.

```bash
inspector.py \
  -c 07_assemblies/sample.primary.fa \
  -r 03_reads_raw/sample.fastq.gz \
  -o 08_stats/inspector_sample \
  -t 32
```

### Final Acceptance Checklist

Before release:

- Assembly size is plausible given k-mer and known genome size.
- No obvious unreviewed chimeric contigs in dotplots.
- Hi-C map is clean if scaffolding was done.
- BUSCO is high for the crop lineage.
- Merqury QV and completeness are acceptable.
- Contamination screens are clean or documented.
- Organellar contigs are handled intentionally.
- FASTA headers are NCBI-safe and stable.
- Scaffold/chromosome names are consistent across FASTA, AGP, GFF3, and reports.
- All manual edits are documented and reproducible.

## Step 15: NCBI and Community Database Release

Public release is part of the assembly workflow, not an afterthought.

### NCBI Submission Objects

You will usually need:

- BioProject
- BioSample
- SRA read submission
- Genome assembly submission
- Annotation submission if submitting annotated genome records

NCBI accepts unannotated eukaryotic genome FASTA submissions. Annotation is optional, but if included it must follow NCBI feature table or GenBank-specific GFF requirements and pass validation.

### Prepare FASTA

NCBI requirements and practical rules:

- FASTA format.
- Stable sequence IDs.
- Avoid spaces and special characters in sequence IDs.
- Each sequence should be at least 200 bp.
- Do not randomly concatenate sequences.
- Include organelles with the genome submission only when they are part of the assembly submission plan; otherwise submit standalone organelles appropriately.
- If using chromosome scaffolds built from contigs, prepare AGP.

Example header style:

```text
>chr01 [organism=Glycine max] [cultivar=ExampleCultivar]
```

For WGS contigs/scaffolds, a simpler stable ID may be better:

```text
>SampleID_chr01
>SampleID_unplaced_000001
```

### AGP

If scaffolds/chromosomes are built from contigs with gaps, provide AGP when required.

Validate AGP:

```bash
agp_validate sample.agp
```

Make sure:

- FASTA scaffold IDs match AGP object IDs.
- Contig IDs match AGP component IDs.
- Gap sizes and linkage evidence are valid.

### NCBI FCS

Run NCBI FCS before submission:

- FCS-adaptor for vector/adaptor contamination.
- FCS-GX for cross-species contamination.

Follow the current NCBI FCS GitHub/wiki instructions because databases and wrapper commands change.

### table2asn

If submitting annotation:

```bash
table2asn \
  -M n \
  -J \
  -c w \
  -euk \
  -t template.sbt \
  -i genome.fsa \
  -f genome.gff \
  -V vb
```

Check:

- `.val` validation report
- discrepancy report
- internal stop codons
- missing locus tags
- invalid products
- genes crossing gaps
- feature coordinates after scaffold renaming

### Community Databases

Crop genomes often also belong in community databases:

- Phytozome/JGI when appropriate.
- SoyBase, MaizeGDB, Gramene, Legume Information System, CottonGen, Sol Genomics Network, or crop-specific portals.
- Figshare/Zenodo/USDA repositories for intermediate files and browser tracks.
- NCBI Assembly and SRA as the archival source.

Release package:

```text
15_release/sample.genome.fa.gz
15_release/sample.genome.fa.gz.fai
15_release/sample.agp
15_release/sample.annotation.gff3.gz
15_release/sample.proteins.fa.gz
15_release/sample.transcripts.fa.gz
15_release/sample.repeats.gff3.gz
15_release/sample.repeat_library.fa.gz
15_release/sample.busco_summary.txt
15_release/sample.merqury_report/
15_release/sample.contamination_reports/
15_release/sample.assembly_methods.md
15_release/sample.metadata.tsv
```

## Example sbatch Scripts

Reusable versions of these scripts live in `01_sbatch_templates/`. Copy the templates into a project-specific `01_sbatch/` directory and edit partition, account, memory, walltime, and module names for your cluster.

```bash
mkdir -p 01_sbatch
cp 01_sbatch_templates/*.sbatch 01_sbatch/
```

### BAM to FASTQ

```bash
#!/bin/bash
#SBATCH -J bam2fastq
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=8G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/bam2fastq_%j.out
#SBATCH -e 00_log/bam2fastq_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load bamtools/2.5.2

echo "Input BAM: ${infile}"
echo "Sample: ${sample}"
echo "Output directory: ${oDir}"
echo "Node: ${SLURMD_NODENAME}"

mkdir -p "${oDir}"

bamtools convert \
  -format fastq \
  -in "${infile}" \
  -out "${oDir}/${sample}.fastq"

echo "Job ID: ${SLURM_JOBID}"
```

Submit:

```bash
sbatch \
  --export infile=raw/sample.bam,sample=sample,oDir=03_reads_raw \
  01_sbatch/bam2fastq.sbatch
```

### hifiasm

```bash
#!/bin/bash
#SBATCH -J hifiasm
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=300G
#SBATCH -t 48:00:00
#SBATCH -o 00_log/hifiasm_%j.out
#SBATCH -e 00_log/hifiasm_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load hifiasm/0.25.0

echo "Reads: ${reads}"
echo "Sample: ${sample}"
echo "Output directory: ${oDir}"
echo "Node: ${SLURMD_NODENAME}"
hifiasm --version || true

mkdir -p "${oDir}/${sample}" 07_assemblies

hifiasm \
  -t "${SLURM_NTASKS}" \
  -o "${oDir}/${sample}/${sample}" \
  ${reads}

for gfa in "${oDir}/${sample}"/*.gfa; do
  base=$(basename "$gfa" .gfa)
  awk '/^S/{print ">"$2; print $3}' "$gfa" > "07_assemblies/${base}.fa"
done

echo "Job ID: ${SLURM_JOBID}"
```

Submit one file:

```bash
sbatch \
  --export reads="03_reads_raw/sample.fastq.gz",sample=sample,oDir=06_hifiasm \
  01_sbatch/hifiasm.sbatch
```

Submit two files for the same sample:

```bash
sbatch \
  --export reads="03_reads_raw/sample_run1.fastq.gz 03_reads_raw/sample_run2.fastq.gz",sample=sample,oDir=06_hifiasm \
  01_sbatch/hifiasm.sbatch
```

### Assembly Stats

```bash
#!/bin/bash
#SBATCH -J asm_stats
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --mem=8G
#SBATCH -t 04:00:00
#SBATCH -o 00_log/asm_stats_%j.out
#SBATCH -e 00_log/asm_stats_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load seqkit
module load bbtools

mkdir -p 08_stats

seqkit stats -a ${assemblies} > 08_stats/seqkit_assembly_stats.tsv

for fa in ${assemblies}; do
  name=$(basename "$fa" .fa)
  stats.sh in="$fa" format=3 -Xmx4g > "08_stats/${name}.bbtools_stats.txt"
done
```

### MUMmer Dotplot

```bash
#!/bin/bash
#SBATCH -J mummer
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/mummer_%j.out
#SBATCH -e 00_log/mummer_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load mummer/4.0.0rc1
module load gnuplot/5.4.8

mkdir -p "${oDir}"

nucmer \
  -t "${SLURM_NTASKS}" \
  -c "${mincluster}" \
  -p "${oDir}/${name}" \
  "${ref}" \
  "${query}"

delta-filter \
  -i "${identity}" \
  -l "${minlen}" \
  -1 \
  "${oDir}/${name}.delta" \
  > "${oDir}/${name}.filter"

show-coords -r -c -l \
  "${oDir}/${name}.filter" \
  > "${oDir}/${name}.coords"

show-tiling \
  "${oDir}/${name}.filter" \
  > "${oDir}/${name}.tiling"

mummerplot \
  -p "${oDir}/plot_${name}" \
  -R "${ref}" \
  --postscript \
  --large \
  --layout \
  --fat \
  "${oDir}/${name}.filter"
```

Submit:

```bash
sbatch \
  --export oDir=09_dotplots,ref=references/ref.fa,query=07_assemblies/sample.primary.fa,name=ref_vs_sample,mincluster=100,identity=90,minlen=10000 \
  01_sbatch/mummer_plot.sbatch
```

### BUSCO

```bash
#!/bin/bash
#SBATCH -J busco
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem=128G
#SBATCH -t 24:00:00
#SBATCH -o 00_log/busco_%j.out
#SBATCH -e 00_log/busco_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

module load busco/6.0.0

mkdir -p 08_stats/busco

busco \
  -i "${assembly}" \
  -m genome \
  -l "${lineage}" \
  -o "${sample}.busco" \
  --out_path 08_stats/busco \
  -c "${SLURM_NTASKS}"
```

Submit:

```bash
sbatch \
  --export assembly=07_assemblies/sample.primary.fa,sample=sample,lineage=embryophyta_odb12 \
  01_sbatch/busco.sbatch
```

## Development Roadmap

### v0.1: Assembly Core

Status: **complete baseline**.

Goal: a usable protocol for HiFi-only primary assemblies.

- Establish a coherent, standalone README for crop plant PacBio HiFi assemblies.
- Add reusable sbatch examples for BAM-to-FASTQ, hifiasm, stats, BUSCO, dotplots.
- Add sample metadata templates.
- Add a small helper script to parse hifiasm logs for k-mer peaks and collected bases.
- Add a FASTA filtering/renaming helper.
- Document raw-vs-trimmed comparison logic.
- Document primary/hap1/hap2 output interpretation.

### v0.2: QC Dashboard

Status: **complete baseline, continuing refinement**.

Goal: standardized assembly quality reports.

- Maintain `scripts/collect_qc_dashboard.py` as the central metric aggregator for seqkit, BBTools, BUSCO, QUAST, Merqury, hifiasm logs, FCS, and project-specific telomere/repeat/annotation summaries.
- Maintain `docs/qc_report_template.md` as the per-assembly peer-review report template.
- Maintain `docs/release_checklist.md`, `docs/methods_text_template.md`, and `examples/release_manifest.tsv` for release preparation.
- Add example plots for read length, assembly length, BUSCO, and Merqury QV.
- Add guidance for interpreting problematic k-mer profiles.

### v0.3: Validation, Contamination, and Organelle Handling

Status: **active, mostly complete baseline**.

Goal: prevent release problems and make validation reproducible.

- Maintain FASTA validation helper.
- Maintain AGP validation helper.
- Maintain assembly decision log template.
- Maintain tool-version policy.
- Maintain StandardizedHeterozygosityEvaluation option for haplotype-level assemblies.
- Maintain toy dataset and GitHub Actions helper validation.
- Maintain FCS-adaptor and FCS-GX examples.
- Maintain organelle detection/removal decision workflow.
- Maintain assembly review standards.
- Maintain BlobToolKit workflow.
- Maintain sourmash read-screening template.
- Maintain contamination decision TSV template.
- Maintain organelle PAF hit summarizer.
- Maintain decision tree for remove, mask, retain, split, or submit separately.
- Maintain NCBI-oriented FASTA header, manifest, and release bundle helper scripts.
- Maintain btrim, PacBio-watch, and QC-figure guidance.
- Remaining before formal v0.4 focus: final review pass across validation, annotation, and release-readiness sections while continuing dotplot and misassembly curation work.

### v0.4: Dotplot and Misassembly Curation

Status: **started during v0.3.0-dev**.

Goal: make structural review teachable and reproducible.

- Add MUMmer/minimap2 dotplot workflows.
- Add example interpretations for clean, inverted, translocated, duplicated, and chimeric patterns.
- Maintain dotplot and misassembly curation guide.
- Maintain example dotplot decision cases.
- Maintain manual-break helper script.
- Maintain correction decision log template.
- Maintain dotplot figure guide.
- Maintain RagTag correct/scaffold comparison workflow.
- Maintain manual reference-to-assembly IGV correction workflow.
- Maintain minimap2 PAF dotplot options.
- Maintain correction summary helper and AGP-after-splitting guidance.

### v0.5: Scaffolding

Goal: chromosome-scale assemblies with clear evidence.

- Add YaHS Hi-C scaffolding workflow.
- Add 3D-DNA/Juicebox visual curation workflow.
- Add RagTag reference-guided scaffold workflow with reference-bias warnings.
- Add AGP generation and validation notes.
- Add Hi-C contact map QC checklist.

### v0.6: Telomere, Centromere, and T2T Readiness

Goal: track chromosome completeness.

- Add tidk examples for known and de novo telomere motifs.
- Add quarTeT telomere/centromere examples.
- Add terminal telomere summary script.
- Add gap summary script.
- Add T2T readiness checklist for projects with ultra-long ONT or optical maps.

### v0.7: Repeat Annotation

Status: **started in v0.3, full refinement planned for v0.7**.

Goal: crop-appropriate repeat libraries and soft-masked genomes.

- Add EDTA workflow.
- Add RepeatModeler2 + RepeatMasker workflow.
- Add repeat landscape summary.
- Add softmasked FASTA output standard.
- Add repeat GFF/BED track preparation.
- Maintain EDTA and RepeatModeler2/RepeatMasker sbatch templates.
- Maintain repeat annotation strategy guide.

### v0.8: Gene Annotation

Status: **started in v0.3, full refinement planned for v0.8**.

Goal: evidence-based gene models.

- Add Liftoff workflow for cultivar-to-cultivar transfer.
- Add BRAKER3 workflow with RNA-seq/protein evidence.
- Add MAKER workflow for projects needing full evidence integration.
- Maintain Liftoff, BRAKER3, and MAKER sbatch templates.
- Maintain gene annotation strategy guide.
- Add functional annotation examples.
- Add annotation QC dashboard.

### v0.9: NCBI Release Candidate

Goal: submission-ready assemblies.

- Add FASTA header validation.
- Add AGP validation.
- Maintain release bundle checker.
- Maintain manifest audit helper.
- Maintain table2asn validation example.
- Maintain NCBI submission and annotation validation guide.
- Add BioProject/BioSample/SRA checklist.
- Refine release manifest template.
- Add methods text template for manuscripts and NCBI structured comments.

### v1.0: Stable Public Protocol

Goal: polished GitHub release for USDA-ARS-GBRU crop genome assembly projects.

- Complete end-to-end README.
- Provide tested sbatch scripts in `01_sbatch_templates/`.
- Provide helper scripts in `scripts/`.
- Provide example metadata in `examples/`.
- Provide a minimal test dataset or toy workflow where licensing permits.
- Add GitHub Actions or local lint checks for scripts.
- Add versioned release notes.
- Add citation and contribution guidelines.

## Key References and Tool Links

Assembly:

- hifiasm documentation: https://hifiasm.readthedocs.io/
- hifiasm paper: https://www.nature.com/articles/s41592-020-01056-5
- hifiasm GitHub: https://github.com/chhylp123/hifiasm
- PacBio GitHub organization: https://github.com/PacificBiosciences
- PacBio pbtk: https://github.com/PacificBiosciences/pbtk
- PacBio pbmm2: https://github.com/PacificBiosciences/pbmm2
- PacBio HiFi human assembly WDL: https://github.com/PacificBiosciences/HiFi-human-assembly-WDL

Genome profiling and quality:

- GenomeScope 2.0 and Smudgeplot: https://www.nature.com/articles/s41467-020-14998-3
- USDA-ARS-GBRU StandardizedHeterozygosityEvaluation: https://github.com/USDA-ARS-GBRU/StandardizedHeterozygosityEvaluation
- Merqury paper: https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02134-9
- BUSCO user guide: https://busco.ezlab.org/busco_userguide
- Inspector paper: https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02527-4

Scaffolding and structural review:

- YaHS paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC9848053/
- RagTag GitHub: https://github.com/malonge/RagTag
- MUMmer4 GitHub: https://github.com/mummer4/mummer
- minimap2: https://github.com/lh3/minimap2

Telomere and centromere:

- tidk paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11814493/
- tidk GitHub: https://github.com/tolkit/telomeric-identifier
- quarTeT paper: https://pubmed.ncbi.nlm.nih.gov/37560017/
- quarTeT GitHub: https://github.com/aaranyue/quarTeT

Contamination:

- NCBI FCS documentation: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/data-processing/policies-annotation/quality/contamination/fcs-contamination/
- NCBI FCS GitHub: https://github.com/ncbi/fcs
- VecScreen/UniVec: https://www.ncbi.nlm.nih.gov/tools/vecscreen/
- btrim paper: https://doi.org/10.1016/j.ygeno.2011.05.009
- HiFiAdapterFilt paper: https://doi.org/10.1186/s12864-022-08375-1
- BlobToolKit paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC7144090/

Repeat annotation:

- EDTA GitHub: https://github.com/oushujun/EDTA
- RepeatModeler2 paper: https://pubmed.ncbi.nlm.nih.gov/32300014/
- RepeatMasker: https://www.repeatmasker.org/

Gene annotation:

- BRAKER: https://github.com/Gaius-Augustus/BRAKER
- MAKER paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC2134774/
- MAKER2 paper: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-12-491
- Liftoff: https://github.com/agshumate/Liftoff

NCBI submission:

- Genome submission portal: https://submit.ncbi.nlm.nih.gov/about/genome/
- Eukaryotic genome submission guide: https://www.ncbi.nlm.nih.gov/genbank/eukaryotic_genome_submission/
- Eukaryotic annotation guide: https://www.ncbi.nlm.nih.gov/genbank/eukaryotic_genome_submission_annotation/
- Submitting eukaryotic genome data: https://www.ncbi.nlm.nih.gov/genbank/eukaryotic_submission/
