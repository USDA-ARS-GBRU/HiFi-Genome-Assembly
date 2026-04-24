# Gene-Set Disagreement Case

This worked case covers a common v0.8 problem: different annotation strategies disagree, and the candidate with the best headline metric is not obviously the best release gene set.

## Scenario

A heterozygous crop assembly has three candidates:

- Liftoff transfer from a close cultivar
- BRAKER3 with RNA-seq and protein support
- a hybrid gene set combining transferred and de novo loci after filtering

The hybrid set has the best BUSCO protein completeness, but internal review shows many short single-exon predictions in repeat-rich intervals. Liftoff preserves stable models and IDs well, but misses some cultivar-specific loci supported by RNA-seq. BRAKER3 recovers novel loci, but also contributes the largest set of low-confidence short models.

## Evidence Snapshot

| Candidate | Protein BUSCO complete percent | Gene count | Strongest feature | Main concern |
| --- | --- | --- | --- | --- |
| Liftoff | 95.1 | 47,820 | preserves trusted models and IDs | misses supported novel loci |
| BRAKER3 | 96.4 | 58,930 | adds RNA-supported novel loci | inflated short-model burden |
| hybrid filtered | 96.8 | 49,270 | balances support and novelty | requires careful provenance tracking |

## Disagreement Pattern

The disagreement is not really about BUSCO alone. It is about how much extra biological signal is real and how much is model inflation.

Use this sequence:

1. confirm all candidates were run on the same final soft-masked FASTA
2. compare gene counts against crop expectations and related references
3. review short single-exon and TE-adjacent predictions
4. verify whether novel loci have transcript or protein support
5. prefer the candidate that is easiest to defend under release and manuscript review

## Recommended Resolution

In this case, the hybrid filtered set is the release choice because it:

- keeps the stable backbone of lifted models
- retains a smaller set of supported novel loci from de novo evidence
- removes a large share of suspect short repeat-adjacent models
- stays compatible with release sequence IDs and downstream table2asn review

BRAKER3 remains valuable as comparison evidence, but not as the release set on its own.

## Decision-Log Language

```text
The hybrid filtered gene set was selected for release because it preserved trusted transferred models while retaining a supported subset of novel loci from de novo evidence. Although the unfiltered BRAKER3-supported candidate produced slightly higher BUSCO completeness, it also increased short repeat-adjacent predictions and was not chosen as the release annotation without additional filtering.
```

## What To Archive

Archive:

- annotation summaries for all candidates
- filtering notes for removed loci
- evidence summaries for retained novel loci
- one final release-gene-set decision row in the decision table

## Reviewer Response Language

```text
We compared transfer, de novo, and hybrid annotations and selected the release set using evidence support, structural plausibility, repeat-adjacent overprediction review, and release compatibility rather than BUSCO completeness alone. The chosen hybrid set preserved stable transferred models while retaining supported novel loci and removing a larger burden of low-confidence short predictions.
```
