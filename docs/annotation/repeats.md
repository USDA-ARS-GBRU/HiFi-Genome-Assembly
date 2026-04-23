# Repeat Annotation and Masking

Repeat annotation is central to crop plant genome work. Transposable elements can dominate plant genomes and affect genome size, gene prediction, structural variant interpretation, and browser tracks.

## Main Strategies

| Strategy | Best use | Caution |
| --- | --- | --- |
| EDTA | plant-focused de novo transposable element annotation | resource-intensive; version dependencies matter |
| RepeatModeler2 + RepeatMasker | general de novo library building and masking | classification may need curation |
| curated library + RepeatMasker | consistent pangenome or breeding-project annotation | may miss novel repeats |
| combined EDTA + curated filtering | reference-grade species library | requires careful provenance and curation |

## Recommended First Pass

1. Run EDTA on the final or near-final assembly.
2. Run RepeatModeler2 + RepeatMasker as an independent comparison when resources allow.
3. Compare total masked fraction and major repeat classes.
4. Use a soft-masked genome for gene annotation.
5. Archive the repeat library, repeat GFF, summary tables, and versions.

## EDTA

```bash
sbatch \
  --export genome=07_assemblies/sample.primary.fa,sample=sample,species=others,sensitive=1 \
  01_sbatch/edta.sbatch
```

Use `species=others` unless a crop-specific mode is appropriate. `sensitive=1` is slower but useful for repeat-rich plant genomes.

## RepeatModeler2 + RepeatMasker

```bash
sbatch \
  --export genome=07_assemblies/sample.primary.fa,sample=sample \
  01_sbatch/repeatmodeler_repeatmasker.sbatch
```

This builds a de novo repeat database, runs RepeatModeler with LTR discovery, and soft-masks the genome with RepeatMasker.

## Release Mask Choice

Choose the repeat annotation that is:

- biologically plausible for the species
- well-classified
- reproducible
- compatible with gene annotation
- documented with tool versions and library provenance

Prefer soft masking for gene prediction so evidence-supported genes can still be modeled through repeats when appropriate.

For release-library decision logging, see `docs/repeat_library_decision_guide.md`.
For interpreting repeat composition and handoff into annotation, see `docs/repeat_landscape_interpretation.md` and `docs/repeat_to_gene_annotation_handoff.md`.

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
- Is the unclassified repeat fraction unusually high?
- Are LTR retrotransposons represented as expected?
- Did sequence filtering or haplotig duplication inflate repeat content?
- Are repeat tracks based on the exact FASTA names used for release?

## Release Rule

Do not change repeat libraries or masking after gene annotation without rerunning or validating downstream annotation.
