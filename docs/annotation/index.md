# Annotation

This section covers repeat annotation, masking strategy, gene annotation, and the handoff from evidence collection to a release-ready gene set.

Recent high-profile crop genome papers generally pair EDTA/RepeatMasker-style repeat annotation with evidence-integrated gene annotation from RNA-seq, Iso-Seq, protein homology, and ab initio prediction. Use this section to make those choices reproducible rather than treating annotation as a single command after assembly.

## Read This Section First If

- the assembly is stable enough to freeze sequence IDs and masking strategy
- you need to choose between EDTA, RepeatModeler2, or a curated repeat library
- you are comparing Liftoff, BRAKER3, MAKER, or hybrid gene-set strategies
- you want annotation QC that will survive NCBI validation and manuscript review

## Best Starting Pages

- [Repeat annotation packet](../repeat_annotation_packet.md)
- [Repeat annotation and masking](repeats.md)
- [Repeat library decision guide](../repeat_library_decision_guide.md)
- [Repeat release-mask decision case](../repeat_release_mask_decision_case.md)
- [Repeat-to-gene-annotation handoff](../repeat_to_gene_annotation_handoff.md)
- [Gene annotation packet](../gene_annotation_packet.md)
- [Gene annotation](genes.md)
- [Gene set decision guide](../gene_set_decision_guide.md)
- [Gene-set disagreement case](../gene_set_disagreement_case.md)
- [Gene ID preservation vs novel-locus recovery case](../gene_id_preservation_vs_novel_loci_case.md)
- [Functional annotation guide](../functional_annotation_guide.md)

## Practical Outcome

After this section, you should have:

- a repeat mask and library you are willing to release
- repeat annotation provenance suitable for pangenome or community reuse
- a gene-set decision backed by evidence rather than habit
- annotation QC tables for internal review and public submission
- a cleaner handoff into the NCBI release path

## Read Next

Move to [Release](../release/index.md) when sequence names, annotation files, and package decisions are stable enough to prepare submission bundles.
