# T2T and Chromosome-Completeness Claim Language

Use this guide when writing manuscripts, genome announcements, NCBI descriptions, reviewer responses, or release notes for chromosome-scale crop genome assemblies. The purpose is to describe completeness accurately without overclaiming telomere-to-telomere status.

Most crop assemblies made from PacBio HiFi plus Hi-C are excellent chromosome-scale assemblies, but not automatically T2T. Long satellites, centromeres, rDNA arrays, knobs, introgressions, B chromosomes, organellar insertions, and collapsed repeats may remain unresolved even when contig and scaffold metrics look strong.

## Core Principle

State the strongest claim supported by the weakest unresolved evidence category.

If the assembly has chromosome-scale Hi-C support but unresolved gaps, call it chromosome-scale. If it has no gaps but missing terminal telomere evidence, call it near-gapless rather than T2T. If one chromosome meets stringent evidence but others do not, claim candidate T2T chromosomes individually, not a T2T genome.

## Claim Classes

| Claim class | Appropriate when | Suggested wording |
| --- | --- | --- |
| `chromosome_scale` | chromosome order/orientation is supported, but gaps, missing telomeres, unresolved repeats, or centromere uncertainty remain | chromosome-scale assembly |
| `near_gapless` | very few or no Ns remain, gap-filling decisions are documented, but not all T2T evidence is complete | near-gapless chromosome-scale assembly |
| `candidate_t2t_chromosome` | a specific chromosome has no Ns, terminal telomere support at both ends, plausible centromere evidence, and no unresolved structure review | candidate T2T chromosome |
| `t2t_quality_assembly` | all expected chromosomes meet candidate T2T criteria, difficult repeats have spanning support, and independent evidence agrees | T2T-quality assembly |
| `unresolved` | evidence conflicts or required support is missing | unresolved completeness status |

## Methods Text

### General Completeness Review

```text
Chromosome completeness was assessed using a structured evidence table that combined FASTA gap status, AGP gap records, terminal and internal telomeric repeat calls, centromere candidate evidence, Hi-C contact-map review, whole-genome dotplots, contamination screening, and difficult-repeat annotations. Completeness classes were assigned conservatively according to the weakest unresolved evidence category for each chromosome-scale scaffold.
```

### Chromosome-Scale Assembly

```text
Hi-C scaffolding produced [N] chromosome-scale scaffolds representing the expected chromosome number for [species/crop]. Scaffold order and orientation were reviewed using contact maps and whole-genome alignments. Because [retained gaps/missing terminal telomere evidence/unresolved centromere evidence] remained, we describe the assembly as chromosome-scale rather than telomere-to-telomere.
```

### Near-Gapless Assembly

```text
The final assembly was reviewed for gap status using FASTA and AGP records. [N] chromosome-scale scaffolds contained no runs of Ns, and [N] retained documented gaps. Gap-filling decisions were accepted only when supported by local sequence evidence and did not conflict with scaffold-level review. We therefore describe the assembly as near-gapless rather than fully T2T.
```

### Candidate T2T Chromosomes

```text
[N] chromosome-scale scaffolds were classified as candidate T2T chromosomes because they contained no runs of Ns, had terminal telomeric repeat signal at both ends, included plausible centromere candidates, and showed no unresolved contact-map, dotplot, or contamination concerns. Remaining chromosomes were classified separately according to their unresolved evidence categories.
```

### T2T-Quality Assembly

```text
The assembly was classified as T2T-quality only after all expected chromosomes had no unresolved gaps, terminal telomere evidence at both ends, plausible centromere annotations, contact-map support, dotplot consistency, contamination clearance, and review of difficult repeat regions. Long-read and/or independent long-range evidence supported the resolution of complex repeats.
```

Use the last statement only when every chromosome meets the evidence standard.

## Results Text

### Conservative Summary

```text
The final assembly contained [N] chromosome-scale scaffolds and [N] unplaced scaffolds. Of the chromosome-scale scaffolds, [N] had no FASTA gaps, [N] had terminal telomeric repeat signal at both ends, and [N] had plausible centromere candidates. Based on the combined evidence, we classified [N] scaffolds as chromosome-scale, [N] as near-gapless, [N] as candidate T2T chromosomes, and [N] as unresolved pending additional review.
```

### Explaining Missing Telomeres

```text
Missing terminal telomere signal was not interpreted as definitive assembly failure because telomeric motifs can vary by lineage and subtelomeric repeats can be difficult to assemble. These chromosome ends were flagged for review rather than used to support T2T claims.
```

### Explaining Centromere Uncertainty

```text
Centromere candidates were treated as evidence classes rather than absolute annotations. Candidate intervals were considered stronger when repeat enrichment, Hi-C behavior, lineage-specific repeat knowledge, or experimental evidence agreed.
```

### Explaining Retained Gaps

```text
Retained gaps were left in the assembly when no defensible spanning sequence or placement evidence was available. We preferred documented unresolved gaps over unsupported gap closure in repetitive or structurally ambiguous regions.
```

## Reviewer Responses

### Reviewer Asks Why the Assembly Is Not Called T2T

```text
We agree that the assembly is highly contiguous, but we have avoided calling it T2T because [specific evidence limitation: retained gaps, missing terminal telomere support, unresolved centromere evidence, or difficult-repeat uncertainty] remains. We now describe the assembly as [chromosome-scale/near-gapless/candidate T2T for N chromosomes] and provide a per-chromosome evidence table summarizing gap, telomere, centromere, Hi-C, dotplot, and difficult-repeat support.
```

### Reviewer Asks Whether Missing Telomeres Indicate Assembly Error

```text
We have clarified that missing terminal telomere motif signal is a review flag rather than definitive evidence of an assembly error. The affected chromosome ends were not used to support T2T claims. We added this limitation to the completeness evidence table and revised the assembly description accordingly.
```

### Reviewer Asks Why Gaps Were Not Filled

```text
We chose not to fill these gaps because the available evidence did not provide a defensible spanning sequence or because the gap overlapped complex repetitive sequence. We preferred retaining documented gaps over introducing unsupported sequence. The revised manuscript now reports retained gap counts and explains the evidence threshold used for gap filling.
```

### Reviewer Asks Why Only Some Chromosomes Are Candidate T2T

```text
We now classify completeness on a per-chromosome basis. [N] chromosomes met our candidate T2T criteria, while the remaining chromosomes had [specific limitation]. We revised the text to avoid implying that the entire assembly is T2T-quality.
```

## Phrases to Avoid

Avoid these unless the evidence is unusually strong:

- `complete genome`
- `fully resolved genome`
- `gapless genome`
- `T2T assembly`
- `finished genome`
- `centromeres were resolved`

Prefer these more precise alternatives:

- `chromosome-scale assembly`
- `near-gapless chromosome-scale assembly`
- `candidate T2T chromosome`
- `no FASTA gaps detected in [N] chromosome-scale scaffolds`
- `terminal telomeric repeat signal was detected at both ends of [N] scaffolds`
- `putative centromere candidates were annotated`

## Release Checklist

Before using T2T or near-gapless language:

- [ ] Run the T2T completeness evidence audit.
- [ ] Confirm FASTA and AGP gap counts agree or explain differences.
- [ ] Confirm terminal telomere motif choice is appropriate for the crop lineage.
- [ ] Review internal telomere signals.
- [ ] Document centromere evidence class and support type.
- [ ] Review Hi-C contact maps for each claimed chromosome.
- [ ] Review dotplots for structural concerns.
- [ ] Document difficult repeats and unresolved loci.
- [ ] Downgrade the claim if evidence conflicts.

## Related Files

- `docs/t2t_readiness_checklist.md`
- `docs/t2t_completeness_evidence_package.md`
- `docs/t2t_completeness_worked_case.md`
- `docs/telomere_summary_workflow.md`
- `examples/t2t_completeness_evidence.tsv`
- `scripts/audit_t2t_evidence_package.py`
