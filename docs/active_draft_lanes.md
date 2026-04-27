# Active Draft Lanes

This page separates the signed-off `v0.5.0` baseline from the active-draft lanes that are still being expanded before a broader `v1.0` validation cycle.

Current active development version: `v0.9.0-dev`

## Current Method Refresh

The 2026-04-27 methods review added a cross-lane refresh grounded in recent crop genome publications. The main effects are:

- hifiasm is the default published-method HiFi contig assembly lane.
- alternate assemblers are framed as diagnostic comparisons.
- YaHS/Juicebox and contact-map review are first-class Hi-C scaffolding paths.
- T2T is a separate escalation lane requiring additional long-range and repeat-region evidence.
- LAI/repeat-space QC, EDTA/RepeatMasker, pangenome repeat libraries, and evidence-integrated gene annotation are now emphasized across relevant pages.

## Stable Baseline

`v0.5.0` is now the signed-off stable baseline for:

- scaffolding and finishing
- gap filling
- T2T readiness framing
- documentation-site migration
- release-readiness teaching paths

This means new contributors should treat `v0.5.0` as the current stable foundation, not as a draft waiting for basic approval.

## Active-Draft Lanes

The following lanes are still under active expansion:

### v0.6 Telomere, Centromere, and T2T Refinement

Status:

- completed first-draft packet

Focus:

- completeness evidence packaging
- conservative claim language
- telomere and centromere interpretation
- stronger examples for hard repeat regions

Best starting pages:

- [v0.6 T2T kickoff](v0.6_t2t_kickoff.md)
- [T2T review packet](t2t_review_packet.md)
- [T2T readiness checklist](t2t_readiness_checklist.md)
- [T2T claim language guide](t2t_claim_language_guide.md)
- [T2T internal telomere review case](t2t_internal_telomere_case.md)
- [T2T repeat-rich centromere case](t2t_repeat_rich_centromere_case.md)

### v0.7 Repeat Annotation Refinement

Status:

- completed first-draft packet

Focus:

- repeat library choices
- release-mask decisions
- repeat interpretation and handoff to genes

Best starting pages:

- [v0.7 repeat kickoff](v0.7_repeat_annotation_kickoff.md)
- [repeat annotation packet](repeat_annotation_packet.md)
- [repeat library decision guide](repeat_library_decision_guide.md)
- [repeat-to-gene handoff](repeat_to_gene_annotation_handoff.md)
- [repeat unclassified burden case](repeat_unclassified_burden_case.md)
- [repeat-rich unplaced contigs case](repeat_unplaced_contigs_case.md)
- [repeat release-mask decision case](repeat_release_mask_decision_case.md)

### v0.8 Gene Annotation Refinement

Status:

- completed first-draft packet

Focus:

- release gene-set decisions
- annotation QC framing
- functional annotation and evidence integration

Best starting pages:

- [v0.8 gene kickoff](v0.8_gene_annotation_kickoff.md)
- [gene annotation packet](gene_annotation_packet.md)
- [gene set decision guide](gene_set_decision_guide.md)
- [annotation QC dashboard guide](annotation_qc_dashboard_guide.md)
- [gene-set disagreement case](gene_set_disagreement_case.md)
- [gene ID preservation vs novel-locus recovery case](gene_id_preservation_vs_novel_loci_case.md)

### v0.9 NCBI Release Candidate Polish

Status:

- current active development lane

Focus:

- submission-packet decisions
- accession and identifier coherence
- annotation handoff and discrepancy cleanup

Best starting pages:

- [v0.9 release kickoff](v0.9_ncbi_release_kickoff.md)
- [release submission packet](release_submission_packet.md)
- [release package decision guide](release_package_decision_guide.md)
- [release internal handoff example](release_internal_handoff_example.md)

Current assessment:

- nearly complete first-draft packet; ready for a human validation pass on the full release path

## Sequential Goal

The current goal is to finish the first tightened draft of each remaining lane in order:

1. `v0.9`
2. broader human validation toward `v1.0`

After each lane feels coherent as a packet, the repository version can move forward to the next active development lane while keeping earlier lanes available as stable or near-stable references.

## How To Contribute Safely

When editing active-draft lanes:

- do not rewrite the stable `v0.5.0` baseline casually
- keep draft-lane changes clearly scoped
- prefer adding worked examples, comparisons, and review logic over broad rewrites
- keep wording conservative when a lane is still evolving

## Read Next

- [Documentation status and roadmap](status.md)
- [How to use this protocol in a real project](how_to_use_this_protocol.md)
- [Project starter kit](project_starter_kit.md)
- [v1.0 human validation plan](v1_human_validation_plan.md)
