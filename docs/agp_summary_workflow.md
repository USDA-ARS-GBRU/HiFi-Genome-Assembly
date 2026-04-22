# AGP Summary Workflow

AGP means **A Golden Path**. An AGP file is a tab-delimited table that describes how smaller assembly components are arranged into larger objects such as scaffolds, linkage groups, or chromosomes. In practical crop genome assembly work, AGP is the map that explains how contigs were ordered, oriented, and separated by gaps to make chromosome-scale scaffolds.

AGP is not a read-alignment file, a gene/repeat annotation file, or a record of how the original contigs were assembled. It is a structural description of the final assembly objects.

## Why AGP Matters

Use AGP when:

- contigs have been scaffolded into chromosome-scale sequences
- the submitted FASTA contains `N` gaps between components
- NCBI or another archive needs the component-to-scaffold structure
- reviewers need to understand which sequence is real component sequence and which span is an unresolved gap

For NCBI submissions, validate AGP with both the local helper and NCBI's `agp_validate` when possible.

## Local Summary

```bash
scripts/summarize_agp.py \
  10_scaffolding/sample.scaffolds.agp \
  -o 10_scaffolding/sample.agp_summary.tsv
```

The summary reports:

- assembled object length
- part count
- component count
- gap count and total gap bases
- component type counts
- gap type counts
- linkage evidence counts
- unoriented component count
- obvious structural issues detected during summarization

## Interpretation

| Pattern | Review |
| --- | --- |
| many scaffold gaps | expected after Hi-C scaffolding, but document gap source |
| `U` gaps not 100 bp | invalid or suspicious for AGP conventions |
| nonsequential coordinates | run full validation before using the file |
| many unoriented components | expected for some reference-guided placements, but should be explicit |
| component/gap count mismatch with FASTA | regenerate AGP or FASTA before submission |

## Release Rule

The AGP, final FASTA, gap summary, scaffolding decision log, and NCBI release bundle should all describe the same assembly structure.

## References

- NCBI AGP Specification v2.1: https://www.ncbi.nlm.nih.gov/genbank/genome_agp_specification/
- NCBI AGP validation: https://www.ncbi.nlm.nih.gov/assembly/agp/
