# Heterozygous HiFi Plus Hi-C Path

This path is for a heterozygous diploid crop with PacBio HiFi reads and matched Hi-C data.

## Typical Goal

Produce a chromosome-scale assembly without confusing true heterozygosity for assembly error.

## Suggested Path

1. Start with the [project starter kit](../project_starter_kit.md)
2. Use [genome profiling before assembly](../assembly/genome_profiling.md) to understand heterozygosity before assembly
3. Run [hifiasm](../assembly/hifiasm.md) and keep phased outputs under review
4. Compare primary and haplotype-aware outputs during [QC](../qc/index.md)
5. Review suspicious structures with [curation](../curation/index.md) before scaffolding
6. Move into [Hi-C scaffolding](../scaffolding/hic_scaffolding.md)
7. Compare scaffold candidates with [scaffolding candidate comparison](../scaffolding_candidate_comparison.md)
8. Use [T2T readiness](../t2t_readiness_checklist.md) only after chromosome-scale structure is defensible
9. Freeze sequence naming before annotation and release

## Default Bias

Be extra cautious:

- do not collapse true haplotypic divergence into a cleaner-looking but less faithful assembly
- do not trust Hi-C joins just because the contact map looks mostly tidy
- do not force reference-like structure when independent evidence disagrees

## What To Watch Closely

- inflated duplication from haplotig retention
- apparent misassemblies that are actually heterozygous structural differences
- Hi-C joins that outperform alternatives only by N50, not by independent evidence
- annotation confusion after scaffold renaming or sequence filtering

## Likely Deliverable

For many such projects, the strongest first release is:

- a carefully reviewed chromosome-scale primary representation
- explicit documentation of how alternate or phased outputs were handled
- a repeat mask and gene set built on frozen sequence IDs
- a release package that favors coherence over maximal phasing claims

## Read Next

- [genome profiling](../assembly/genome_profiling.md)
- [Hi-C scaffolding reader path](../scaffolding/hic_scaffolding.md)
- [scaffolding worked decision case](../scaffolding_worked_decision_case.md)
