# T2T Readiness Checklist

Use this checklist when a project wants to claim chromosome completeness, near-gapless status, or telomere-to-telomere quality. Most crop HiFi projects will not be true T2T from HiFi alone. The goal is to describe the evidence honestly and identify what remains unresolved.

## Minimum Inputs

| Evidence | Strong support | Caution |
| --- | --- | --- |
| PacBio HiFi | high QV contigs and local base accuracy | may not span long centromeric satellites or rDNA arrays |
| Hi-C | chromosome order/orientation and misjoin review | cannot sequence unresolved repeats by itself |
| Ultra-long ONT | can span large tandem repeats and centromeres | needs independent polishing/validation strategy |
| Optical map | independent long-range structure | lower sequence resolution |
| Genetic map | chromosome-scale order validation | marker density may be uneven |
| Related reference | helps interpret structure | can hide accession-specific variation |

## Required Summaries

Prepare these tables for every chromosome-scale assembly:

- FASTA statistics before and after scaffolding.
- AGP validation summary. AGP means A Golden Path: the tab-delimited map describing how component sequences and gaps form larger scaffolds or chromosomes.
- Gap count, gap length, and maximum gap length per chromosome.
- Terminal telomere motif count and orientation per chromosome end.
- Internal telomere motif candidates with interpretation.
- Centromere candidate intervals and supporting evidence.
- Hi-C contact-map review decisions.
- Dotplot review decisions against a close reference or related assembly.
- Contamination/organelle review decisions.

## Gap Status Classes

| Class | Meaning | Release language |
| --- | --- | --- |
| gapless | no `N` run in the chromosome FASTA | gapless chromosome-scale scaffold |
| terminal_telomere_both | telomere signal at both ends | candidate complete chromosome |
| terminal_telomere_one | telomere signal at one end | one end may be complete |
| internal_telomere_review | telomere signal inside scaffold | review for misjoin or biological interstitial repeat |
| unresolved_gap | retained `N` run with documented reason | scaffold contains unresolved gap |
| complex_repeat_gap | gap overlaps satellite, rDNA, or long tandem repeat | do not fill without spanning evidence |
| unplaced_sequence | valid sequence not assigned to chromosome | submit as unplaced/unlocalized when appropriate |

## T2T Claim Decision

| Claim | Minimum evidence |
| --- | --- |
| chromosome-scale | Hi-C/contact-map support, AGP validation, dotplot review |
| near-gapless | very few documented gaps, gap-filling decisions reviewed, no unsupported fills |
| candidate T2T chromosome | no Ns, telomere signal at both ends, centromere candidate documented, Hi-C support, no unresolved contamination |
| T2T-quality assembly | all chromosomes meet candidate T2T criteria and difficult repeats have spanning evidence, ideally with ultra-long ONT or optical-map support |

## Review Questions

- Are all Ns intentional and represented in AGP where appropriate?
- Did any gap-filling tool remove Ns in regions where the scaffold join itself was uncertain?
- Do terminal telomere calls agree with chromosome orientation?
- Are centromere candidates plausible for the crop lineage and repeat landscape?
- Are rDNA arrays, knob repeats, B chromosomes, organellar insertions, or introgressions documented?
- Are unplaced contigs biologically plausible rather than overlooked contamination?
- Would a reviewer be able to reproduce the completeness claim from the archived logs and tables?

## Recommended Files

```text
12_telomere_centromere/sample.telomere_summary.tsv
12_telomere_centromere/sample.centromere_candidates.tsv
10_scaffolding/sample.gap_summary.tsv
10_scaffolding/sample.gap_filling_report.md
10_scaffolding/sample.scaffolding_decisions.tsv
08_stats/sample.qc_dashboard.tsv
15_release/sample.agp_validation.tsv
15_release/sample.fasta_validation.tsv
```

## Manuscript Language

Use precise language. Avoid saying "complete genome" unless the evidence supports every chromosome.

Example:

```text
The final assembly consisted of [N] chromosome-scale scaffolds and [N] unplaced scaffolds. Gap status was summarized directly from the final FASTA and AGP files. [N] chromosomes contained no runs of Ns, [N] retained documented scaffold gaps, and [N] had telomeric repeat signal at both terminal ends. We therefore describe the assembly as [chromosome-scale/near-gapless/candidate T2T] rather than fully complete.
```
