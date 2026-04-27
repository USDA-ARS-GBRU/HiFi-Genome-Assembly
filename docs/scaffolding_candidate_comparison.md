# Scaffolding Candidate Comparison

Run scaffolding candidates side by side when multiple tools are plausible. For example, a project may compare YaHS, 3D-DNA/JBAT, RagTag, and a gap-filled candidate. The goal is not to pick the assembly with the largest N50. The goal is to pick the structure with the strongest independent evidence.

This comparison step is especially important for crop pangenomes, where different groups may choose Hi-C scaffolding, reference/map-based ordering, or Triticeae-specific workflows depending on the species and project goal.

## Candidate Table

Create a FASTA-level comparison:

```bash
scripts/compare_scaffolding_candidates.py \
  --candidate contig=07_assemblies/sample.primary.fa \
  --candidate yahs=10_scaffolding/sample/yahs/sample.yahs_scaffolds_final.fa \
  --candidate 3d_dna=10_scaffolding/sample/3d_dna/sample.FINAL.fasta \
  --candidate ragtag=10_scaffolding/sample/ragtag/ragtag.scaffold.fasta \
  --candidate gapfilled=10_scaffolding/sample/gapfilled.fa \
  -o 10_scaffolding/sample.scaffolding_candidate_metrics.tsv
```

This helper reports sequence count, total length, N50/N90, gap count, gap bases, and maximum gap size for each candidate. It intentionally does not declare a winner.

For a small worked example that moves from candidate metrics to a final decision, see `docs/scaffolding_worked_decision_case.md`.

## What to Compare

| Evidence | Why it matters |
| --- | --- |
| FASTA metrics | catches large shifts in continuity, total length, and gap burden |
| AGP validation | confirms scaffold coordinates and gap records are coherent |
| Hi-C contact map | primary evidence for order, orientation, and joins |
| Dotplot | reveals inversions, translocations, duplications, and reference disagreements |
| HiFi read mapping | checks local continuity around suspicious joins |
| Merqury sanity check | confirms sequence content did not unexpectedly change during scaffolding |
| Telomere/centromere status | supports chromosome completeness and orientation |
| Contamination review | prevents contaminant or organellar sequence from being scaffolded |

## Decision Rules

- Prefer a lower N50 assembly when the higher N50 candidate is driven by unsupported joins.
- Leave short, repeat-rich, or weakly supported contigs unplaced when evidence is ambiguous.
- Treat reference-guided placements as hypotheses when the reference is a different genotype.
- Re-run release validation after choosing the final candidate.
- Record rejected candidates and the reason they were rejected.

## Reviewer-Ready Summary

```text
We compared [N] scaffold candidates generated with [tools]. Candidate selection was based on contact-map support, AGP validity, whole-genome alignments, local read support, gap status, and contamination review rather than continuity statistics alone. The selected candidate had [N] chromosome-scale scaffolds, [N] unplaced scaffolds, [N] unresolved gaps, and no unsupported high-confidence joins in the reviewed contact map.
```
