# T2T Internal Telomere Review Case

This case covers a common hard situation: a chromosome-scale scaffold has terminal telomere signal at both ends and no obvious FASTA gaps, but an internal telomere signal appears partway through the sequence.

## Why This Matters

An internal telomere signal can mean very different things:

- a real structural problem
- a repeat-rich region that happens to resemble the telomere motif
- a collapsed or misjoined subtelomeric segment
- a motif-rich region that needs review but does not justify an automatic break

## Scenario

A chromosome-scale scaffold has:

- terminal telomere signal at both ends
- no FASTA gaps
- strong overall Hi-C support
- one internal telomere cluster near a repeat-rich interval
- a dotplot that is mostly clean but slightly ambiguous across the same region

## Conservative Interpretation

Do not call the chromosome `candidate_t2t_chromosome` until the internal telomere signal is reviewed against:

- dotplots
- Hi-C map structure
- repeat annotation
- read-backed alignments, if available

If the region remains ambiguous after review, classify it as `unresolved` rather than forcing a stronger completeness label.

## Recommended Wording

Safer results text:

```text
The scaffold had terminal telomeric repeat signal at both ends and no retained FASTA gaps, but an internal telomeric repeat cluster overlapped a repeat-rich interval that remained under structural review. We therefore retained an unresolved completeness status for this chromosome rather than classifying it as candidate T2T.
```

## Reviewer-Response Logic

```text
We did not treat terminal telomere signal and gap absence as sufficient on their own. Because an internal telomeric repeat cluster remained present in a structurally ambiguous interval, we retained a conservative unresolved classification pending stronger evidence that the region did not reflect a misjoin or collapsed repeat structure.
```

## Teaching Point

This is exactly the kind of situation where conservative claim language protects the assembly more than a stronger label would.

## Related Pages

- [T2T review packet](t2t_review_packet.md)
- [T2T claim language guide](t2t_claim_language_guide.md)
- [Worked completeness claim case](t2t_completeness_worked_case.md)
