# Repeat-to-Gene-Annotation Handoff Checklist

Use this checklist before starting Liftoff, BRAKER3, MAKER, or any custom gene annotation workflow. The goal is to freeze exactly which repeat outputs are feeding gene prediction and to prevent silent drift between repeat annotation and gene annotation.

## Required Inputs

The annotation team should receive:

```text
13_repeats/sample.softmasked.fa
13_repeats/sample.repeatmasker.gff
13_repeats/sample.repeat_library.fa
13_repeats/sample.repeat_summary.tsv
examples/repeat_annotation_decisions.tsv
```

Also provide:

- final assembly version identifier
- sequence ID map used for release
- contamination/organelle exclusion decisions
- any scaffold or chromosome renaming log
- tool versions and command history for the repeat run

## Handoff Checks

- [ ] The soft-masked FASTA comes from the selected release repeat mask.
- [ ] The repeat GFF3 or GFF track uses the same sequence IDs as the soft-masked FASTA.
- [ ] The repeat library provenance is documented.
- [ ] The repeat annotation decision log marks exactly one release mask.
- [ ] The repeat annotation decision log marks exactly one gene annotation input.
- [ ] No scaffold splitting, renaming, contamination filtering, or assembly replacement occurred after the repeat run.
- [ ] If assembly structure changed after repeat annotation, the repeat run was regenerated or explicitly remapped and validated.
- [ ] The gene annotation workflow input path matches the selected soft-masked FASTA.

## Common Failure Cases

| Problem | Why it matters | Fix |
| --- | --- | --- |
| Gene annotation used an older soft-masked FASTA | gene coordinates and repeat evidence no longer match release sequence IDs | rerun annotation or repeat masking on final FASTA |
| Repeat GFF uses stale scaffold names | browser tracks and gene overlap checks become misleading | rerun or remap repeat annotation |
| Multiple repeat candidates marked as release masks | provenance is unclear | choose one release mask and document the rest as comparison-only |
| Repeat library changed after gene prediction | gene models may have been influenced by a different masking regime | rerun gene annotation or validate impact explicitly |
| Organellar or contaminant contigs were removed after repeat annotation | repeat fractions and sequence coverage changed | regenerate repeat summaries and handoff files |

## Release Rule

Do not release the gene annotation unless the repeat handoff is traceable. Reviewers and database curators should be able to identify:

- which repeat library was used
- which soft-masked FASTA fed gene prediction
- whether repeat-derived gene models were filtered
- whether repeat coordinates and final release sequence IDs agree

## Methods Language

```text
Gene annotation was performed on the selected soft-masked release assembly produced from the final repeat annotation run. Repeat library provenance, masking method, repeat summary statistics, and the repeat decision log were archived with the annotation inputs to ensure that gene models could be traced to the exact release masking set.
```

## Reviewer Response Language

```text
We have clarified the repeat-to-annotation handoff. The final gene annotation used the selected soft-masked release assembly and repeat track generated from the final release sequence IDs. Candidate repeat masks that were not chosen for release were retained only as comparison evidence and were not used as annotation inputs.
```

## Related Files

- `docs/repeat_library_decision_guide.md`
- `docs/gene_annotation.md`
- `docs/annotation/genes.md`
- `examples/repeat_annotation_decisions.tsv`
