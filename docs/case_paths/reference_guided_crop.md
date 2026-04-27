# Reference-Guided Crop Path

This path is for a crop genome where a close reference exists, Hi-C is absent or limited, and reference-guided scaffolding is being considered.

## Typical Goal

Use the reference to organize the assembly cautiously without letting reference bias erase true biological differences.

## Suggested Path

1. Start with the [project starter kit](../project_starter_kit.md)
2. Build and review the contig assembly with [assembly](../assembly/index.md) and [QC](../qc/index.md)
3. Use [curation](../curation/index.md) to resolve clear structural problems before scaffolding
4. Review [RagTag](../ragtag_workflow.md) and the [scaffolding candidate comparison](../scaffolding_candidate_comparison.md)
5. Compare reference-guided structure against dotplots and read-backed evidence
6. Keep unsupported placements out of the final release scaffold set
7. Freeze naming and release objects only after unsupported joins are rejected or documented

## Default Bias

Be conservative:

- use the reference as an organizing hypothesis, not as proof
- distinguish pangenome comparability from de novo truth; some published pangenome projects use reference or map ordering for consistency, but that choice must be explicit
- prefer unplaced or unscaffolded sequence over a confident-looking but weakly supported placement
- do not “correct” real structural differences just to match the reference
- preserve evidence for PAVs, inversions, introgressions, and accession-specific structure

## What To Watch Closely

- reference-guided joins that are unsupported by independent evidence
- inversions or translocations that may be real biology
- over-fragmentation from aggressive correction before scaffolding
- chromosome names that imply confidence beyond the evidence
- downstream SV analyses that depend on whether reference-guided order altered interpretation

## Likely Deliverable

The strongest early release is often:

- a mostly reference-organized scaffold set
- unsupported or ambiguous sequence retained separately
- a clear decision log describing what was placed, withheld, or split
- release notes that distinguish evidence-supported order from reference-guided convenience

## Read Next

- [RagTag workflow](../ragtag_workflow.md)
- [scaffolding worked decision case](../scaffolding_worked_decision_case.md)
- [release package decision guide](../release_package_decision_guide.md)
