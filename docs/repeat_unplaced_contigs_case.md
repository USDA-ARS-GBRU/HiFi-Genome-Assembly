# Repeat-Rich Unplaced Contigs Case

This case covers another common repeat-annotation problem: a large fraction of repeat signal is concentrated on unplaced or unlocalized contigs.

## Why This Matters

Repeat-rich unplaced contigs can be:

- legitimate repeat-dense genomic sequence
- organellar or contaminant carryover that was not removed cleanly
- unresolved satellites or knob-like sequence
- alternate or duplicated assembly content that should not define the release mask

## Scenario

A crop assembly has a plausible chromosome-scale scaffold set, but a subset of unplaced contigs shows:

- very high repeat density
- much lower gene density
- uncertain contamination or organelle history
- repeat composition that is harder to classify than the chromosome-scale scaffolds

## Conservative Interpretation

Do not assume these unplaced contigs should drive the release-wide repeat summary without review.

Instead, ask:

- are these sequences intended to remain in the release assembly?
- do they represent plausible biological repeat blocks for this crop?
- were contamination and organelle decisions finalized before repeat annotation?

If the answer is still unclear, keep the repeat interpretation conservative and describe the uncertainty directly.

## Recommended Wording

Safer results text:

```text
Repeat enrichment was strongest on a subset of unplaced contigs, which were reviewed separately because unresolved sequence class, contamination history, or repeat-rich structure could disproportionately influence whole-assembly repeat summaries. We therefore interpret assembly-wide repeat burden with caution until the final retained sequence set is fully stabilized.
```

## Reviewer-Response Logic

```text
We agree that repeat-rich unplaced contigs should not be interpreted automatically as representative of chromosome-scale repeat structure. The revised text now separates unplaced repeat-dense sequence from the core scaffold interpretation and emphasizes its reviewed but unresolved status where appropriate.
```

## Teaching Point

Sometimes the important question is not “how repetitive is the assembly?” but “which parts of the assembly are currently defining that answer?”

## Related Pages

- [Repeat annotation packet](repeat_annotation_packet.md)
- [Repeat landscape interpretation](repeat_landscape_interpretation.md)
- [Repeat-to-gene-annotation handoff](repeat_to_gene_annotation_handoff.md)
