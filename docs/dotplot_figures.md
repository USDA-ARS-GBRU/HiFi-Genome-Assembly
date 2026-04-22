# Dotplot Figure Guide

Dotplot figures are evidence. They should help a reviewer understand why an assembly was retained, corrected, or flagged for future work.

## Figures to Include

For a peer-reviewed crop genome manuscript or release report, include:

- whole-genome assembly-vs-reference dotplot
- chromosome-scale dotplots for every edited chromosome or scaffold
- self-alignment dotplot when duplication, haplotigs, or collapsed repeats are suspected
- before/after dotplot for any manual break, reorder, or orientation edit
- Hi-C contact map beside any chromosome-scale scaffolding correction
- read-depth or k-mer evidence for any destructive edit

## Minimum Caption Elements

Each figure caption should state:

- assembly version
- reference genome and version
- aligner and preset
- filtering applied to alignments
- reason the figure is shown
- final decision made from the figure

## Interpretation Patterns

| Figure pattern | What to say carefully |
| --- | --- |
| Clean diagonal | The assembly is broadly collinear with the comparison reference. |
| Inversion-like block | The region may be inverted relative to the reference; independent evidence is needed before flipping. |
| Chromosome jump | The region may be chimeric, translocated, introgressed, or reference-specific. |
| Repeated blocks | The pattern may reflect duplication, haplotigs, repeats, or copy-number differences. |
| Assembly-only sequence | The sequence may be a genuine insertion, a reference gap, contamination, or organellar carryover. |

## Common Mistakes

- showing only edited regions and hiding the whole-genome context
- using a reference from a distant species without warning about divergence
- treating every inversion-like pattern as an assembly error
- cropping axes so the apparent correction looks cleaner than it is
- failing to report alignment filters
- not archiving the command used to make the plot

## File Naming

Use stable names:

```text
09_dotplots/sample_vs_reference.whole_genome.png
09_dotplots/sample_vs_reference.chr03.break_review.png
09_dotplots/sample_self.duplication_review.png
09_dotplots/sample_before_after.edit_0001.png
```

## Release Rule

Every manual correction in the decision log should point to at least one archived figure or evidence file. If the figure cannot be regenerated from recorded commands and inputs, it is not strong enough for a release-quality audit trail.
