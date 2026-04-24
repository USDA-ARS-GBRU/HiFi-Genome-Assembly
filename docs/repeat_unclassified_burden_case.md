# Repeat Unclassified Burden Case

This case covers a common repeat-annotation problem: the total masked fraction looks plausible, but the unclassified repeat fraction is too high to support confident biological interpretation.

## Why This Matters

A run can look superficially successful while still being weak for release if too much of the repeat space remains unclassified.

High unclassified burden can reflect:

- genuine lineage-specific repeats
- weak classification in the chosen library
- noisy or inflated repeat discovery
- unresolved assembly representation issues

## Scenario

Two candidate repeat runs are compared on the same frozen assembly:

- EDTA: plausible masked fraction, lower unclassified burden, cleaner major class breakdown
- RepeatModeler2 plus RepeatMasker: similar total masked fraction, but a much larger unclassified fraction

## Conservative Interpretation

Do not choose the candidate with the noisier classification just because the total masked percent is similar.

If the unclassified burden is meaningfully higher, the more class-resolved candidate is usually the better release mask unless there is a clear biological reason to prefer the other run.

## Recommended Wording

Safer methods text:

```text
Candidate repeat annotations were compared not only by total masked fraction but also by unclassified repeat burden, major repeat class plausibility, and compatibility with downstream gene annotation. We selected the release mask with the stronger overall classification profile rather than relying on masked percentage alone.
```

## Reviewer-Response Logic

```text
We agree that total masked percentage alone is not sufficient for repeat-library selection. The revised text now makes clear that unclassified repeat burden and class-level interpretability were explicit decision criteria in choosing the release repeat mask.
```

## Teaching Point

Masked percentage can tell you the size of the answer. Classification quality tells you whether you actually understand the answer.

## Related Pages

- [Repeat annotation packet](repeat_annotation_packet.md)
- [Repeat library decision guide](repeat_library_decision_guide.md)
- [Repeat landscape interpretation](repeat_landscape_interpretation.md)
