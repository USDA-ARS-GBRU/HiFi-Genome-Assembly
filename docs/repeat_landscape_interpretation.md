# Repeat Landscape Interpretation

Use this guide when reviewing repeat summaries, repeat composition plots, and repeat-age landscapes for crop plant genomes. The goal is to interpret repeat structure biologically without confusing assembly artifacts, masking differences, or haplotig carryover for true transposable element history.

## What a Repeat Landscape Can Show

A repeat landscape can help summarize:

- overall repeat burden
- proportions of major repeat classes
- LTR retrotransposon dominance
- DNA transposon contribution
- unclassified repeat burden
- possible waves of repeat amplification
- differences among cultivars, accessions, or haplotypes

For crop genomes, these summaries are useful but easy to overinterpret. Always connect them back to assembly quality, masking method, and lineage expectations.

## First Questions

Before interpreting the plot or summary table, ask:

- Was the same assembly representation used across comparisons?
- Were the same repeat tools and library rules used across samples?
- Were contaminant, organellar, alternate, or haplotig sequences removed consistently?
- Are sequence names and final release objects stable?
- Is the unclassified repeat fraction low enough to trust class-level conclusions?

## Common Patterns

| Observation | Possible interpretation | Review before claiming |
| --- | --- | --- |
| High total masked fraction with plausible major classes | repeat-rich crop genome or large TE burden | assembly size, haplotig duplication, contamination |
| EDTA and RepeatModeler similar total masked percent | robust overall repeat estimate | class definitions and unclassified burden |
| Large unclassified fraction | novel repeats, weak classification, or library noise | whether a curated library or additional curation is needed |
| LTR retrotransposons dominate | common in many plant genomes | whether assembly inflation or unresolved duplication contributes |
| Major difference from related cultivar | real biology, accession structure, or technical differences | assembly size, masking method, and input sequence set |
| Strong repeat enrichment on unplaced contigs | repeat-rich genuine sequence or unresolved assembly fraction | contamination, organelles, B chromosomes, satellites, introgressions |

## Signals That Need Caution

Do not make strong biological claims from repeat landscapes alone when:

- the assembly still contains many unresolved duplicates
- the unclassified fraction is high
- the candidate repeat library changed after gene annotation
- different masking tools or options were used across compared samples
- alternate haplotypes were included in one sample but not another
- scaffold correction or contamination filtering happened after repeat annotation

## Crop-Specific Notes

In crop genomes, repeat-rich regions can reflect:

- centromeres and pericentromeres
- knob repeats
- large LTR retrotransposon blocks
- rDNA arrays
- introgressed haploblocks
- B chromosomes or supernumerary chromosomes
- lineage-specific tandem repeats

These can be biologically important, but they also overlap with exactly the regions where assemblies and masking are most fragile.

## Practical Review Rules

- Compare repeat landscapes only after the assembly representation is frozen.
- Review total masked percent together with assembly size and duplication status.
- Treat high unclassified burden as a reason to review, not as a biological class.
- Check whether repeat-heavy unplaced contigs are plausible biological sequence or unresolved junk.
- Make sure the soft-masked FASTA used for gene annotation matches the repeat run being interpreted.

## Manuscript Language

```text
Repeat composition was summarized from the selected release repeat library and masking run. Major repeat classes were interpreted in the context of assembly size, repeat library provenance, unclassified repeat burden, and the final assembly representation. We avoid overinterpreting repeat-age or class-enrichment patterns where classification uncertainty or assembly representation could influence the result.
```

## Reviewer Response Language

```text
We have clarified that repeat landscape interpretation was restricted to the final release assembly representation and the selected repeat library. We also note that class-level conclusions were not based on masked percentage alone, but were reviewed together with unclassified repeat burden, library provenance, and assembly structure.
```

## Related Files

- `docs/repeat_annotation.md`
- `docs/repeat_library_decision_guide.md`
- `examples/repeat_summary.tsv`
- `examples/repeat_summary_edta.tsv`
- `examples/repeat_summary_repeatmodeler.tsv`
