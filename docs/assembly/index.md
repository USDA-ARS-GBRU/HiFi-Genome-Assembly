# Assembly

This section covers the path from raw PacBio HiFi reads to an interpretable first assembly.

The default assembly lane is intentionally simple: profile the genome, assemble HiFi reads with `hifiasm`, preserve all primary/alternate/haplotype outputs, then let QC decide whether any diagnostic assembler or advanced method is needed. This matches the dominant pattern in recent high-profile crop pangenome papers.

## Read This Section First If

- you need to estimate genome properties before assembly
- you are deciding how conservative or aggressive to be with hifiasm settings
- you want a clean first-pass primary assembly before scaffolding or curation
- you are comparing inbred, heterozygous, phased, trio, or reference-assisted assembly paths
- you need a structured way to compare hifiasm against HiCanu, Flye, IPA, Verkko, or ONT-aware methods

## Best Starting Pages

- [Prepare PacBio HiFi reads](prepare_reads.md)
- [Genome profiling before assembly](genome_profiling.md)
- [hifiasm assembly workflow](hifiasm.md)
- [hifiasm parameters and assembly modes](hifiasm_parameters.md)
- [Alternate assembler comparison](alternate_assemblers.md)

## Practical Outcome

After this section, you should have:

- read QC and preprocessing decisions
- a first estimate of genome size and heterozygosity
- a primary assembly plan that matches the biology
- a documented decision about whether alternate assembly comparison is warranted
- an assembly decision log worth carrying into QC and release

## Read Next

Continue to [QC](../qc/index.md) before making structural edits or jumping into scaffolding.
