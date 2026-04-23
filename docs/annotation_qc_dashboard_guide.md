# Annotation QC Dashboard Guide

Use this guide to summarize the final release gene set in a compact dashboard or review table. The goal is to show whether the selected annotation is plausible, well-supported, and ready for release.

## Core Metrics

Track at minimum:

| Metric | Why it matters |
| --- | --- |
| protein-coding gene count | catches overprediction or underprediction |
| transcript count | shows isoform handling and model inflation |
| BUSCO protein completeness | checks conserved gene-space completeness |
| functional annotation rate | distinguishes supported proteins from unannotated models |
| internal stop codon count | flags broken or low-quality models |
| TE-derived model count or review status | checks repeat-related overprediction |
| table2asn validation status | signals release-readiness for annotation submission |

## Example Summary Table

Use the compact summary format from:

```text
examples/annotation_summary.tsv
examples/annotation_summary_liftoff.tsv
examples/annotation_summary_hybrid.tsv
```

When comparing multiple candidate annotations, use:

```bash
scripts/compare_annotation_summaries.py \
  --candidate liftoff=examples/annotation_summary_liftoff.tsv \
  --candidate hybrid=examples/annotation_summary_hybrid.tsv \
  -o /tmp/annotation_summary_comparison.tsv
```

## Interpretation Rules

- Higher gene count is not automatically better.
- Higher BUSCO is useful but can still coexist with TE-derived overprediction.
- Functional annotation rate should be interpreted with gene length, protein quality, and TE filtering in mind.
- A release-track set with slightly fewer genes can be better if it has cleaner structure and stronger evidence support.

## Suggested Review Sections

### Structural QC

- gene count
- transcript count
- median transcript length
- median protein length
- internal stop codon review

### Completeness QC

- BUSCO protein-mode complete
- BUSCO duplicated
- BUSCO fragmented
- BUSCO missing

### Biological Plausibility

- fraction of proteins with functional assignment
- TE-derived model review summary
- suspicious scaffold/chromosome enrichment
- comparison to related crop annotations

### Release Readiness

- final GFF3 and protein FASTA use release sequence IDs
- repeat handoff documented
- decision log identifies one release gene set
- table2asn status reviewed

## Manuscript Language

```text
Annotation quality was summarized using a compact dashboard that included gene count, transcript count, BUSCO protein-mode completeness, functional annotation rate, and review of TE-derived or structurally suspicious models. Candidate gene sets were compared side by side before the release annotation was selected.
```

## Reviewer Response Language

```text
We now provide a compact annotation QC summary showing structural counts, BUSCO protein completeness, functional annotation rate, and review of TE-derived models. This helps distinguish the selected release gene set from comparison-only annotation runs.
```

## Related Files

- `docs/gene_annotation.md`
- `docs/gene_set_decision_guide.md`
- `docs/functional_annotation_guide.md`
- `examples/annotation_summary.tsv`
