# Project Starter Kit

This page is the compact setup guide for starting a real crop genome assembly project with this protocol.

## Goal

By the end of this page, you should have:

- a project directory
- a first metadata table
- a decision log
- a place for sbatch templates
- a clear first-pass workflow plan

## Create The Working Layout

Use a stable project structure from day one so later QC, curation, annotation, and release files do not get scattered.

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

## Create The First Metadata Files

Start with:

```text
00_metadata/samples.tsv
00_metadata/references.tsv
00_metadata/sequencing_runs.tsv
00_metadata/assembly_decisions.md
00_metadata/release_metadata.md
```

Useful examples:

- `examples/samples.tsv`
- `examples/references.tsv`

## Questions To Answer Immediately

Before running big jobs, write down:

- what biological sample this is
- expected genome size
- ploidy
- whether the material is inbred, heterozygous, clonal, or polyploid
- whether Hi-C, parents, RNA-seq, or Iso-Seq exist
- whether the immediate target is contigs, haplotypes, or chromosome-scale scaffolds

Put the answers in `00_metadata/assembly_decisions.md`.

## Copy The First sbatch Templates

For a normal first-pass HiFi assembly project, start with copies of:

- `01_sbatch_templates/hifiasm.sbatch`
- `01_sbatch_templates/busco.sbatch`
- `01_sbatch_templates/mummer_plot.sbatch`

Put project-specific copies in:

```text
01_sbatch/
```

Do not edit the reusable templates in place.

## Choose The First Reading Path

For most new projects:

1. [Software environments on HPC](setup/environment.md)
2. [Genome profiling before assembly](assembly/genome_profiling.md)
3. [hifiasm assembly workflow](assembly/hifiasm.md)
4. [Assembly metrics and interpretation](qc/assembly_metrics.md)
5. [Dotplots for assembly review](qc/dotplots.md)

## First Deliverables To Produce

Aim to generate these before worrying about scaffolding:

- read QC summary
- genome profiling summary
- first hifiasm assembly
- assembly metrics table
- dotplot set
- contamination review notes

## Common Early Mistakes

- starting assembly before the sample definition is clear
- mixing biological samples under one project prefix
- using cluster module versions without writing them down
- renaming sequences repeatedly across different steps
- jumping into scaffolding before contigs pass basic QC

## Related Pages

- [How to use this protocol in a real project](how_to_use_this_protocol.md)
- [sbatch template index](sbatch_template_index.md)
- [Setup](setup/index.md)
- [Assembly](assembly/index.md)
