# Gene Set Decision Guide

Use this guide to choose and document the release gene set. The right answer is not always the run with the largest gene count or the one that produces the fewest missing orthologs in BUSCO.

## Candidate Inputs

Common candidates include:

- Liftoff annotation transfer from a close cultivar or species
- BRAKER3 annotation with RNA-seq and/or protein support
- MAKER annotation integrating multiple evidence types
- a merged or curated hybrid gene set

Run candidates against the same final soft-masked FASTA whenever possible.

## Decision Table

Record decisions in:

```text
examples/gene_annotation_decisions.tsv
```

Recommended columns:

| Column | Meaning |
| --- | --- |
| `decision_id` | stable decision identifier |
| `sample_id` | project or accession |
| `assembly_version` | assembly version reviewed |
| `candidate_method` | Liftoff, BRAKER3, MAKER, hybrid |
| `candidate_outputs` | key output files |
| `gene_count` | total gene models |
| `busco_protein_complete_percent` | BUSCO protein-mode completeness |
| `primary_strength` | strongest reason to use this candidate |
| `primary_concern` | strongest reason to reject or review |
| `final_action` | use_for_release, comparison_only, reject, needs_review |
| `table2asn_ready` | yes/no |
| `reviewer` | reviewer name or initials |
| `notes` | short rationale |

## Choosing the Release Gene Set

Prefer the candidate that is:

- supported by transcript and/or protein evidence
- biologically plausible for the crop and assembly representation
- not inflated by TE-derived predictions or unresolved duplicates
- compatible with release FASTA sequence IDs
- reproducible from archived commands and evidence inputs
- acceptable under table2asn and downstream release review

## Common Decision Cases

| Observation | Interpretation | Action |
| --- | --- | --- |
| Liftoff preserves known models cleanly | useful for close cultivar transfer | strong release candidate if divergence is limited |
| BRAKER3 adds plausible novel models | useful de novo support | compare against transfer and TE-derived overprediction |
| MAKER integrates multiple evidence types well | useful for release-grade curation | use if configuration and provenance are well documented |
| candidate has best BUSCO but many short or TE-like models | possible overprediction | review before release |
| candidate gene set uses stale sequence IDs | release mismatch | regenerate on final FASTA |
| table2asn reports major structural problems | submission blocker | fix or reject candidate |

## Handoff to Release

The release package should include:

```text
14_genes/sample.annotation.gff3
14_genes/sample.proteins.fa
14_genes/sample.transcripts.fa
14_genes/sample.annotation_summary.tsv
examples/gene_annotation_decisions.tsv
```

Keep comparison-only annotation runs, but mark them clearly as not-for-release.

## Manuscript Language

```text
Candidate gene annotations were generated with [Liftoff/BRAKER3/MAKER/hybrid strategy] and compared using evidence support, BUSCO protein-mode completeness, structural plausibility, repeat-derived overprediction review, and compatibility with the final release sequence set. The selected release gene set was chosen for biological plausibility and reproducibility rather than model count alone.
```

## Reviewer Response Language

```text
We have clarified how the release gene set was selected. Candidate annotations were compared using transcript/protein support, BUSCO protein-mode completeness, structural plausibility, TE-derived overprediction review, and compatibility with the final release FASTA and repeat mask. Comparison-only runs were retained for transparency but not used as release annotations.
```
