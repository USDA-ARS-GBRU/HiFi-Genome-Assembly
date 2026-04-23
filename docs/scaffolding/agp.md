# AGP for Scaffolded Assemblies

AGP means **A Golden Path**. An AGP file is a tab-delimited assembly map describing how smaller component sequences are arranged into larger scaffolds, linkage groups, or chromosomes. It also records the unresolved gaps between components.

For crop genome projects, AGP is most often needed after Hi-C, optical-map, genetic-map, or reference-guided scaffolding. It explains which spans of a chromosome FASTA are real component sequence and which spans are unresolved `N` gaps.

AGP is not:

- a read alignment file
- a gene annotation file
- a repeat annotation file
- a substitute for a scaffolding decision log

## When to Create AGP

Create or retain AGP when:

- contigs are joined into larger scaffold/chromosome objects
- the FASTA contains scaffold gaps
- NCBI or another archive requests component structure
- reviewers need to trace scaffold joins back to input contigs

AGP may not be needed for an unscaffolded contig assembly where each FASTA record is submitted exactly as assembled.

## Basic Structure

Each AGP row describes one span of a larger object. Component rows point to sequence records. Gap rows describe unresolved intervals.

Common row types:

| Type | Meaning |
| --- | --- |
| `W` | WGS sequence component |
| `A` | active finishing sequence component |
| `D` | draft sequence component |
| `F` | finished sequence component |
| `N` | gap with estimated length |
| `U` | gap with unknown length, conventionally 100 bp |

## Local Checks

Validate basic structure:

```bash
scripts/validate_agp.py \
  10_scaffolding/sample.scaffolds.agp \
  -o 10_scaffolding/sample.agp_validation.tsv
```

Summarize scaffold objects:

```bash
scripts/summarize_agp.py \
  10_scaffolding/sample.scaffolds.agp \
  -o 10_scaffolding/sample.agp_summary.tsv
```

Use NCBI's `agp_validate` as the release-facing check when available:

```bash
agp_validate 10_scaffolding/sample.scaffolds.agp
```

## Review Questions

- Do AGP object IDs match the scaffold/chromosome IDs in the final FASTA?
- Do component IDs match the contig FASTA or component records used to build the scaffold?
- Are coordinates sequential and non-overlapping?
- Are `U` gaps represented consistently?
- Are linkage evidence terms appropriate for the scaffolding method?
- Do AGP gap counts agree with the final FASTA gap summary?
- Were AGP files regenerated after manual breaks, orientation changes, gap filling, or renaming?

## Release Rule

The final FASTA, AGP, scaffold decision log, gap summary, and release manifest must describe the same assembly version.

## Related Pages

- [AGP summary workflow](../agp_summary_workflow.md)
- [AGP after splitting or correcting FASTA](../agp_after_splitting.md)
- [Scaffolding candidate comparison](../scaffolding_candidate_comparison.md)
