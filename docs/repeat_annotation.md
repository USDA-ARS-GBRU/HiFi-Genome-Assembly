# Repeat Annotation Strategy

Repeat annotation is central to crop plant genome work. It affects gene prediction, genome browser tracks, transposable element summaries, and biological interpretation of genome size and structural variation.

## Main Options

| Strategy | Strengths | Tradeoffs | Good use case |
| --- | --- | --- | --- |
| EDTA | Plant-focused, strong LTR/TE classification, convenient end-to-end output | Can be resource-intensive; version dependencies can be delicate | Primary crop genome repeat annotation |
| RepeatModeler2 + RepeatMasker | General de novo repeat discovery plus mature masking workflow | Classification may need curation; less plant-specific as a single workflow | Cross-checking EDTA or annotating nonstandard genomes |
| Curated library plus RepeatMasker | Consistent across related assemblies | Can miss novel repeats | Pan-genome projects with a validated species library |
| Combined EDTA + curated filtering | Best long-term library quality | Requires curation and clear provenance | Reference-grade community release |

## Recommended First Pass

For a new crop genome:

1. Run EDTA on the final or near-final assembly.
2. Run RepeatModeler2 + RepeatMasker as an independent comparison if resources allow.
3. Compare total masked fraction and major repeat classes.
4. Use a soft-masked genome for gene annotation.
5. Save the repeat library, repeat GFF, summary tables, and software versions.

Run repeat annotation after the assembly sequence set is mostly stable. If you remove contaminant contigs, split scaffolds, rename chromosomes, or change the primary/haplotype representation, rerun or remap repeat annotation before releasing tracks.

## EDTA

```bash
sbatch \
  --export genome=07_assemblies/sample.primary.fa,sample=sample,species=others,sensitive=1 \
  01_sbatch/edta.sbatch
```

Use `species=others` unless the crop has a specific EDTA mode that is appropriate. `sensitive=1` is slower but useful for repeat-rich plant genomes.

## RepeatModeler2 + RepeatMasker

```bash
sbatch \
  --export genome=07_assemblies/sample.primary.fa,sample=sample \
  01_sbatch/repeatmodeler_repeatmasker.sbatch
```

This workflow builds a de novo repeat database, runs RepeatModeler with LTR structure discovery, and soft-masks the genome with RepeatMasker.

## Choosing a Release Mask

Use the repeat annotation that is:

- biologically plausible for the species
- well-classified
- reproducible
- compatible with the gene annotation workflow
- documented with tool versions and library provenance

Do not switch repeat libraries after gene annotation without rerunning or validating gene prediction.

For a structured release-mask decision table and reviewer-response language, see `docs/repeat_library_decision_guide.md`.

For annotation, prefer soft masking over hard masking so gene predictors can still use the underlying sequence when evidence supports a model. Hard-masked FASTA can be useful for some downstream searches, but it is usually not the best master genome sequence for a release package.

## Comparing Repeat Runs

Summarize each repeat run in a small table:

```text
sample  method  genome_bp  masked_bp  masked_pct  ltr_pct  dna_te_pct  unclassified_pct  library
```

Compare against related cultivars and species when available. A large change in masked fraction can be real in crop genomes, but it should trigger review of assembly size, haplotig duplication, organellar carryover, and unclassified repeat burden.

## Deliverables

```text
13_repeats/sample.repeat_library.fa
13_repeats/sample.repeatmasker.gff
13_repeats/sample.repeat_summary.tsv
13_repeats/sample.softmasked.fa
13_repeats/sample.repeat_landscape.pdf
```

## Review Questions

- Is the total repeat percentage plausible for the crop?
- Are LTR retrotransposons represented as expected?
- Is the unclassified fraction unusually high?
- Did repeat masking suppress real gene models?
- Are repeat-derived gene predictions being filtered or annotated correctly?
- Are repeat tracks based on the exact FASTA sequence names used for release?
