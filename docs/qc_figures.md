# QC Figures for Peer Review and Manuscripts

Use figures to show independent evidence that the assembly is complete, accurate, uncontaminated, and structurally credible. A strong manuscript or release report should not rely on a single N50 table.

## Core Figure Set

| Figure | Purpose | Typical source |
| --- | --- | --- |
| Read length distribution | Shows input read quality and whether data are long enough for the genome | seqkit, NanoPlot, custom histogram |
| k-mer spectrum | Shows genome size, heterozygosity, repeat signal, and possible contamination | meryl/jellyfish + GenomeScope/Smudgeplot |
| Assembly contiguity comparison | Compares raw/trimmed/default/alternate assemblies | seqkit, BBTools, QUAST |
| BUSCO summary | Shows conserved gene completeness and duplication | BUSCO |
| Merqury spectra-cn and QV | Shows k-mer completeness, copy-number behavior, and base accuracy | Merqury |
| Whole-genome dotplot | Shows collinearity, inversions, translocations, and possible misjoins | MUMmer, minimap2, plotsr |
| Hi-C contact map | Shows chromosome-scale scaffolding support | YaHS/3D-DNA/Juicebox |
| GC/coverage/taxonomy blob plot | Shows contamination and outlier review | BlobToolKit |
| Telomere summary plot/table | Shows chromosome-end completeness | tidk, quarTeT, seqkit locate |
| Repeat composition bar chart | Shows repeat landscape and masking result | EDTA, RepeatModeler2/RepeatMasker |
| Gene annotation QC | Shows gene count, BUSCO protein completeness, functional annotation | BRAKER/MAKER/Liftoff + BUSCO |

## Minimum Internal Review Package

- Read stats table and read length histogram.
- k-mer profile with estimated genome size and heterozygosity.
- Assembly stats table.
- BUSCO genome summary.
- Merqury QV/completeness summary.
- At least one whole-genome dotplot against a close reference or related assembly.
- Contamination summary from FCS and BlobToolKit or equivalent.

## Minimum Public Release Package

- Internal review package.
- Hi-C contact map if chromosome-scale scaffolding was used.
- Telomere/gap summary if chromosome-level claims are made.
- Repeat annotation summary if gene annotation is included.
- Gene annotation QC if annotation is submitted or described.
- Decision log for every sequence removed, split, masked, or retained after contamination review.

## Figure Design Guidelines

- Label assemblies, haplotypes, and versions clearly.
- Report tool versions and lineage/database names in captions or methods.
- Avoid presenting N50 alone as a quality claim.
- For dotplots, include enough axis labels to identify chromosomes/scaffolds.
- For BUSCO, state the lineage dataset.
- For Merqury, state k-mer size and read set used.
- For BlobToolKit, explain color/taxonomy and coverage axes.
- For Hi-C maps, show the final reviewed assembly, not only the initial scaffold output.

