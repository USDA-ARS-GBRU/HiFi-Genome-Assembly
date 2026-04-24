# Repeat Release-Mask Decision Case

This worked case closes the v0.7 packet with a common plant-genome problem: one repeat annotation run masks more sequence, but the extra masking falls heavily on gene-rich contigs and recent TE-rich chromosome arms where annotation sensitivity still matters.

## Scenario

A maize-like crop assembly has three repeat candidates:

- EDTA strict structural library
- RepeatModeler2 and RepeatMasker de novo library
- a merged library after manual filtering

The merged library masks the highest fraction of the genome, but it also expands masked sequence near many transferred and evidence-supported gene models.

## Evidence Snapshot

| Candidate | Total masked percent | Unclassified percent | Genes overlapped by new masking | Reviewer concern |
| --- | --- | --- | --- | --- |
| EDTA strict | 79.8 | 9.4 | low | may miss some lineage-specific families |
| RepeatModeler2 and RepeatMasker | 82.3 | 18.7 | moderate | high unclassified burden |
| merged filtered | 83.1 | 11.8 | high | possible over-masking near genes |

## Decision Logic

Do not choose the library with the highest masked fraction by default.

In this case, the release decision favors the EDTA strict library because it:

- gives a cleaner family interpretation
- introduces fewer overlaps with known or strongly supported genes
- is easier to explain in manuscript methods
- reduces the chance that downstream gene prediction is suppressed by overly aggressive masking

The merged library is still worth keeping as a comparison resource, but not as the release mask.

## Final Action

Recommended decision-log language:

```text
The EDTA strict repeat library was selected as the release soft-mask because it balanced repeat sensitivity with lower overlap across supported gene loci. A merged repeat library masked a slightly larger fraction of the assembly but introduced additional masking across gene-rich regions and was retained as a comparison-only run rather than the release mask.
```

## What To Keep

Keep:

- the release repeat summary
- the comparison summary for rejected candidates
- one short note explaining why more masking was not treated as automatically better

Do not keep as the only rationale:

- total masked percent
- chromosome-scale TE density plots without gene-overlap review
- "highest masking won"

## Reviewer Response Language

```text
We compared multiple repeat-library candidates and selected the release mask based on interpretability and downstream annotation compatibility rather than masked fraction alone. The rejected merged library increased total masking only modestly while expanding masking into more gene-rich intervals, so it was retained for comparison but not used as the release mask.
```
