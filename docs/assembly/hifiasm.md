# hifiasm Assembly Workflow

Use this page when you are ready to turn PacBio HiFi reads into a first assembly that can survive downstream QC and review.

For most crop projects, hifiasm is the default starting point because it gives a strong first-pass assembly without forcing early complexity. The hard part is not only running the assembler. The hard part is choosing which outputs to carry forward and documenting why.

## Goal

Use hifiasm to build a high-quality PacBio HiFi contig assembly, then preserve enough logs and metadata to explain the assembly choice during review.

## Inputs

```text
03_reads_raw/sample.hifi.fastq.gz
examples/samples.tsv
```

Optional inputs:

- Hi-C reads for integrated hifiasm Hi-C mode or later scaffolding.
- Trio parental reads for trio-binned haplotype assemblies.
- Expected genome size from flow cytometry, k-mer spectra, or prior references.

## Default Primary Assembly

```bash
hifiasm \
  -o 07_assemblies/sample.asm \
  -t 48 \
  03_reads_raw/sample.hifi.fastq.gz \
  2> 00_log/sample.hifiasm.err
```

Typical first-pass products:

```text
sample.asm.bp.p_ctg.gfa
sample.asm.bp.hap1.p_ctg.gfa
sample.asm.bp.hap2.p_ctg.gfa
sample.hifiasm.err
```

Convert selected GFA outputs to FASTA, capture tool versions, and keep the original GFA files.

Do not throw away alternate or haplotype-resolved outputs immediately. Even if the primary assembly becomes the release candidate, the other outputs can explain why BUSCO duplication, k-mer behavior, or structural differences look the way they do.

## Parameter Logic

| Choice | Starting point | Reasoning |
| --- | --- | --- |
| threads | 32-64 on HPC | hifiasm scales well, but memory and I/O still matter |
| primary output | `bp.p_ctg` | common release candidate for a collapsed primary assembly |
| haplotype outputs | `hap1/hap2` | useful for heterozygous or phased analyses |
| Hi-C mode | project-specific | can improve phasing but does not replace post-assembly review |
| purging | conservative | over-purging can remove real haplotypes, paralogs, or introgressions |

## Review After Assembly

Before scaffolding or release:

- summarize FASTA statistics
- run BUSCO and Merqury
- inspect hifiasm log peaks
- compare primary/haplotype outputs
- screen contamination and organelles
- generate dotplots for structural review
- record the assembly choice in the decision log

## Before You Move On

Before leaving the assembly stage, make sure you can answer:

- why this output is the preferred assembly candidate
- whether haplotype-resolved outputs are being kept, excluded, or submitted separately
- whether the assembly size matches the genome-profiling expectations closely enough to trust the next stage
- whether obvious contamination or organellar carryover is already visible

## Related Pages

- `docs/assembly_decision_log_template.md`
- `docs/assembly/genome_profiling.md`
- `docs/v0.4_curation_index.md`
- `docs/yahs_hic_workflow.md`
- `docs/scaffolding/index.md`
