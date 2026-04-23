# Worked Completeness Claim Case

This case shows how a mixed chromosome-completeness evidence table becomes conservative manuscript language. The example is small, but it mirrors a common crop assembly situation: most chromosomes are excellent, some are near complete, and a few still have evidence limitations that should block T2T claims.

## Scenario

A diploid crop assembly has 12 expected chromosomes. The final scaffold set has:

- 12 chromosome-scale scaffolds
- 9 unplaced scaffolds
- no high-confidence contamination
- strong Hi-C support for chromosome-scale order and orientation
- telomere evidence that varies by chromosome
- centromere candidates with mixed confidence

The team wants to know whether the assembly can be described as T2T.

## Evidence Table

Use the v0.6 completeness evidence package:

```text
examples/t2t_completeness_evidence.tsv
```

The toy rows illustrate three outcomes:

| Sequence | Evidence summary | Claim class |
| --- | --- | --- |
| `chr01` | no gaps, telomeres at both ends, moderate centromere evidence, strong Hi-C, collinear dotplot | `candidate_t2t_chromosome` |
| `chr02` | one documented gap, one missing telomere, low-confidence centromere evidence | `chromosome_scale` |
| `chr03` | no gaps, telomeres at both ends, but internal telomere signal and unresolved dotplot/contact-map review | `unresolved` |

Run the audit before writing release language:

```bash
scripts/audit_t2t_evidence_package.py \
  examples/t2t_completeness_evidence.tsv \
  -o /tmp/t2t_evidence_audit.tsv
```

The audit should pass for the example table. The intentionally bad fixture should fail:

```bash
scripts/audit_t2t_evidence_package.py \
  examples/t2t_completeness_evidence_bad.tsv \
  -o /tmp/t2t_bad_evidence_audit.tsv
```

## Decision

Do not call the full assembly T2T. A defensible summary is:

- The assembly is chromosome-scale.
- One reviewed chromosome is a candidate T2T chromosome in this toy example.
- Some chromosomes remain chromosome-scale because gaps, missing telomeres, or weak centromere evidence remain.
- Some chromosomes are unresolved because structural or internal telomere evidence still needs review.

This language protects the project from overclaiming while still highlighting the best-supported chromosomes.

## Manuscript Methods Text

```text
Chromosome completeness was assessed using a per-scaffold evidence table that combined FASTA gap status, AGP gap records, terminal and internal telomeric repeat calls, centromere candidate evidence, Hi-C contact-map review, whole-genome dotplots, contamination screening, and difficult-repeat annotations. Completeness classes were assigned conservatively according to the weakest unresolved evidence category for each chromosome-scale scaffold.
```

## Manuscript Results Text

```text
The final assembly contained 12 chromosome-scale scaffolds and 9 unplaced scaffolds. Completeness evidence was evaluated per chromosome. Chromosomes with no FASTA gaps, terminal telomeric repeat signal at both ends, plausible centromere evidence, and no unresolved contact-map or dotplot concerns were classified as candidate T2T chromosomes. Chromosomes with retained gaps, missing terminal telomere evidence, weak centromere evidence, or unresolved internal telomere/dotplot signals were classified as chromosome-scale or unresolved rather than T2T.
```

## Reviewer Response

```text
We have revised the assembly description to avoid implying that the full genome is T2T. Completeness is now reported per chromosome using a structured evidence table that includes gap status, AGP gaps, telomere evidence, centromere candidates, Hi-C review, dotplot review, and difficult-repeat annotations. We classify only chromosomes meeting all evidence criteria as candidate T2T chromosomes and describe the remaining chromosomes as chromosome-scale or unresolved according to their limiting evidence category.
```

## Teaching Notes

- Candidate T2T is a chromosome-level claim unless every expected chromosome meets the standard.
- Missing telomere signal should trigger review, not automatic failure or automatic motif switching.
- A no-gap chromosome can still be unresolved if contact maps, dotplots, or internal telomere evidence raise structural concerns.
- A conservative claim with a transparent evidence table is easier to defend than a stronger claim that reviewers can puncture.
