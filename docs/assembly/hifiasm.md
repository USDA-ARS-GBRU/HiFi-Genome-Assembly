# hifiasm Assembly Workflow

This page is the first focused extraction from the longform README into the future web documentation structure. The README remains the canonical guide during development.

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

## Related Pages

- `docs/assembly_decision_log_template.md`
- `docs/v0.4_curation_index.md`
- `docs/yahs_hic_workflow.md`
- `docs/scaffolding/index.md`
