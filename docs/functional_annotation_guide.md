# Functional Annotation Guide

Use this guide after selecting the structural gene set for release. Functional annotation should help explain what the predicted genes likely encode without inflating confidence for low-support or transposable-element-derived models.

## Common Functional Annotation Sources

Typical sources include:

- InterProScan for conserved domains and signatures
- eggNOG-mapper for orthology and broad function assignment
- DIAMOND or BLASTP against curated protein databases
- Pfam, Panther, or related domain databases
- GO terms, KEGG orthology, or pathway mappings when appropriate

The best release package usually combines domain evidence with homology evidence rather than relying on one annotation source alone.

## Inputs to Freeze

Before functional annotation, freeze:

- final protein FASTA for the release gene set
- transcript FASTA if transcript-based annotation is planned
- release gene IDs
- filtering rules for TE-derived, fragmentary, or unsupported models
- exact software versions and database versions

Do not run functional annotation on one gene set and then publish a different structural annotation without rerunning or remapping the functional labels.

## Minimum Deliverables

```text
14_genes/sample.proteins.fa
14_genes/sample.functional_annotation.tsv
14_genes/sample.interpro.tsv
14_genes/sample.eggnog.tsv
14_genes/sample.annotation_summary.tsv
```

## Review Questions

- What fraction of proteins received any functional assignment?
- Are the largest unannotated categories plausible for the crop lineage and gene-set strategy?
- Were TE-derived proteins handled separately from likely host genes?
- Are major functional classes consistent with related crop annotations?
- Do suspiciously short proteins dominate the unannotated fraction?

## Release Rules

- Keep database versions with the output.
- Distinguish "no hit" from "not searched."
- Do not imply experimental validation from homology alone.
- Document whether TE-derived or low-confidence models were filtered before or after functional annotation.

## Manuscript Language

```text
Predicted proteins from the selected release gene set were functionally annotated using [InterProScan/eggNOG-mapper/DIAMOND/other] with database versions recorded in the release metadata. Functional annotation rates were summarized together with structural gene-set QC to distinguish unsupported models from genes lacking informative homology or domain assignments.
```

## Reviewer Response Language

```text
We have clarified the functional annotation workflow and now report both the annotation source and the fraction of proteins receiving functional assignments. Functional labels were generated from the final release protein set and are linked to the exact release gene IDs.
```

## Related Files

- `docs/gene_annotation.md`
- `docs/gene_set_decision_guide.md`
- `docs/annotation_qc_dashboard_guide.md`
- `examples/annotation_summary.tsv`
