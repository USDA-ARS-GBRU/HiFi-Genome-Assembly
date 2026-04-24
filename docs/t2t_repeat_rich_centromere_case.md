# T2T Repeat-Rich Centromere Case

This case covers another common hard situation: a chromosome-scale scaffold appears gapless and well supported, but centromere evidence is still weak or indirect because the relevant region is deeply repeat rich.

## Why This Matters

A chromosome can look nearly complete while still lacking enough evidence for a strong centromere-related completeness claim.

That often happens when:

- long satellites are difficult to resolve
- repeat annotation is incomplete or low confidence
- Hi-C structure is supportive overall but not decisive across the centromeric interval

## Scenario

A scaffold has:

- no FASTA gaps
- terminal telomere motif signal at both ends
- strong chromosome-scale Hi-C support
- strong overall dotplot collinearity
- a large repeat-rich internal interval with only weak centromere candidate evidence

## Conservative Interpretation

This scaffold may still be best described as `near_gapless` or `candidate_t2t_chromosome`, depending on the rest of the evidence package, but it should not be upgraded casually to a whole-assembly T2T claim.

If centromere evidence remains weak, say that directly rather than hiding it behind stronger shorthand.

## Recommended Wording

Safer results text:

```text
The scaffold was gapless in the release FASTA and showed terminal telomeric repeat signal at both ends, but the centromeric interval remained supported primarily by indirect repeat-rich sequence evidence. We therefore describe the chromosome as a candidate near-complete scaffold and avoid a stronger whole-assembly T2T claim.
```

## Reviewer-Response Logic

```text
We agree that gap absence and terminal telomere evidence alone do not establish full chromosome completeness in repeat-rich centromeric regions. The revised text now distinguishes between a gapless chromosome-scale scaffold and a stronger T2T-quality claim that would require more decisive centromere-support evidence.
```

## Teaching Point

The hard part of T2T language is often not the telomeres. It is knowing when repeat-rich internal evidence is still too weak for the strongest label.

## Related Pages

- [T2T review packet](t2t_review_packet.md)
- [T2T completeness evidence package](t2t_completeness_evidence_package.md)
- [T2T claim language guide](t2t_claim_language_guide.md)
