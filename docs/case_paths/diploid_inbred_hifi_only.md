# Diploid Inbred HiFi-Only Path

This path is for a relatively inbred diploid crop with PacBio HiFi reads and no Hi-C.

## Typical Goal

Produce a strong primary contig assembly first, then decide whether later reference-assisted scaffolding is justified.

## Suggested Path

1. Start with the [project starter kit](../project_starter_kit.md)
2. Set up software with [software environments on HPC](../setup/environment.md)
3. Profile the reads with [genome profiling before assembly](../assembly/genome_profiling.md)
4. Assemble with [hifiasm](../assembly/hifiasm.md)
5. Review [assembly metrics](../qc/assembly_metrics.md) and [dotplots](../qc/dotplots.md)
6. Check [contamination](../qc/contamination.md)
7. Use [curation](../curation/index.md) only if strong structural evidence appears
8. Move to [annotation](../annotation/index.md) once the contigs look stable
9. Use [release](../release/index.md) for assembly-first submission readiness

## Default Bias

Be conservative:

- favor the primary assembly as the first release candidate
- treat hifiasm as the default published-method starting point
- use alternate assemblers only as diagnostics if QC disagrees with profiling or biology
- do not force chromosome-scale scaffolding just because a related reference exists
- do not over-purge duplicated sequence without strong evidence that it is assembly redundancy
- do not describe the assembly as T2T without telomere, centromere, gap, and difficult-repeat evidence

## What To Watch Closely

- unexpected assembly inflation relative to genome profiling
- BUSCO duplication that is too high for the biology
- organelle carryover
- false confidence from good contig N50 without structural review
- missing repeat-space QC when the crop is repeat-rich

## Likely Deliverable

For many such projects, the first defensible deliverable is:

- a high-quality primary contig assembly
- repeat masking
- a first-pass gene annotation
- an assembly-first NCBI package

## Read Next

- [hifiasm workflow](../assembly/hifiasm.md)
- [alternate assembler comparison](../assembly/alternate_assemblers.md)
- [assembly metrics](../qc/assembly_metrics.md)
- [release package decisions](../release_package_decision_guide.md)
