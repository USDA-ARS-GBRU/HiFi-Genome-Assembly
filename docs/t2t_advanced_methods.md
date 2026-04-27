# Advanced T2T Methods

Use this page when a project is aiming beyond ordinary chromosome-scale assembly toward near-gapless or telomere-to-telomere claims. Most crop HiFi projects should not start here. Start here only when the project goal, available data, and validation plan are strong enough to support difficult repeat resolution.

## Core Principle

PacBio HiFi is excellent for accurate contigs, but HiFi reads alone often do not span the longest centromeric satellites, rDNA arrays, knob repeats, subtelomeric repeats, or other tandem arrays in crop genomes. Recent T2T crop publications add ultra-long ONT, Hi-C, optical maps, cytogenetic assays, targeted gap closure, or multiple independent assemblies before claiming completion.

## When To Escalate

Escalate into an advanced T2T lane when:

- the project explicitly needs candidate T2T chromosomes
- remaining gaps overlap biologically important repeats, rDNA, centromeres, or telomeres
- ultra-long ONT or similarly long-range evidence is available
- the team can validate repeat copy number, read spanning, and local structure
- the release language can distinguish chromosome-scale, near-gapless, candidate T2T, and fully complete

Stay in the ordinary chromosome-scale lane when the project only needs a strong reference for annotation, mapping, or first release.

## Data Types

| Evidence | What it helps resolve | Caution |
| --- | --- | --- |
| PacBio HiFi | accurate contigs, local sequence, k-mer QV | may not span long tandem repeats |
| Ultra-long ONT | long satellites, rDNA arrays, centromeric or telomeric repeats | requires polishing and independent validation |
| Hi-C / Omni-C | chromosome order, orientation, misjoin review | does not sequence missing repeat sequence |
| Optical map / Bionano | independent long-range structure | lower base-level resolution |
| Genetic map | independent chromosome-scale order | marker density can be uneven |
| FISH or cytogenetic evidence | repeat-array or centromere validation | not a replacement for sequence evidence |
| Related reference | context for expected chromosome structure | can hide accession-specific biology |

## Tool Roles

| Tool or approach | Best use | Caution |
| --- | --- | --- |
| Verkko | hybrid HiFi plus ONT near-T2T assembly | plan as a separate assembly lane |
| hifiasm-UL / hifiasm hybrid modes | scalable near-T2T or ONT-aware assembly where current docs support it | verify version-specific commands before production |
| NextDenovo / NECAT | ONT-heavy assembly support or comparison | usually needs polishing and careful validation |
| Canu HiFi mode | comparison or difficult-region support | not usually the first crop HiFi default now |
| TRFill | targeted tandem-repeat gap filling | requires careful configuration and local validation |
| quarTeT GapFiller / TeloExplorer / CentroMiner | gap, telomere, and centromere evidence review | do not let module output replace manual interpretation |
| manual repeat closure | final targeted closure when reads clearly support it | document every accepted and rejected edit |

## Validation Package

For each candidate T2T chromosome, collect:

```text
no-N FASTA status
terminal telomere motif evidence on both ends
internal telomere review
centromere candidate interval and support
rDNA/satellite/tandem-repeat interval review
spanning-read evidence for difficult repeats
read-depth consistency across closed gaps
Hi-C/contact-map support across joins
before/after dotplots for filled or corrected regions
Merqury QV/completeness and spectra-cn
contamination and organelle status
reviewer decision log
```

## Claim Ladder

| Claim | Use when |
| --- | --- |
| chromosome-scale | scaffolds are ordered/oriented with long-range evidence |
| gapless chromosome-scale scaffold | a chromosome scaffold has no Ns, but difficult terminal/repeat evidence is incomplete |
| candidate T2T chromosome | no Ns, both telomeres detected, centromere documented, structure validated |
| near-T2T assembly | most chromosomes meet candidate criteria, with a small number of documented unresolved regions |
| T2T-quality assembly | all chromosomes meet candidate criteria and difficult repeats have strong independent validation |

## Related Pages

- [T2T readiness checklist](t2t_readiness_checklist.md)
- [T2T evidence package](t2t_completeness_evidence_package.md)
- [T2T claim language](t2t_claim_language_guide.md)
- [gap filling workflow](gap_filling_workflow.md)
- [telomere summary workflow](telomere_summary_workflow.md)
- [alternate assembler comparison](assembly/alternate_assemblers.md)
