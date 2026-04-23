# Genome Profiling Before Assembly

Genome profiling estimates genome size, heterozygosity, repeat content, coverage, and ploidy signal before assembly. These estimates help choose an assembly strategy, interpret hifiasm output, and explain why an assembly size is plausible.

## Key Questions

- What is the expected haploid genome size?
- Is the sample inbred, heterozygous, clonally propagated, or polyploid?
- Does the k-mer profile show one clear homozygous peak or multiple dosage peaks?
- Is there enough HiFi coverage for the assembly goal?
- Do prior references, flow cytometry, and k-mer estimates agree?

## Coverage Estimate

```text
coverage = total HiFi bases / expected haploid genome size
```

Example:

```text
30 Gb HiFi reads / 1.0 Gb genome = 30x
```

For many diploid crop assemblies, 25-40x HiFi is a practical lower range and 40-80x is common for robust projects. Larger, more heterozygous, or polyploid genomes often benefit from additional data and more careful interpretation.

## meryl and GenomeScope

Merqury uses `meryl`, so using `meryl` early creates reusable k-mer databases.

```bash
meryl k=21 count output 05_kmers/sample.k21.meryl 03_reads_raw/sample.fastq.gz
meryl histogram 05_kmers/sample.k21.meryl > 05_kmers/sample.k21.hist
```

Upload the histogram to GenomeScope 2.0 or run a local GenomeScope installation.

Record:

- estimated genome size
- heterozygosity
- repeat content
- main k-mer peak
- model fit quality
- k-mer size
- read set used

## Smudgeplot

Use Smudgeplot when ploidy, subgenome structure, or heterozygous dosage is uncertain. This is especially useful for polyploid crops, wild relatives, and heterozygous clonally propagated material.

Interpret Smudgeplot with caution when:

- coverage is low
- the sample is contaminated
- a crop has recent whole-genome duplication
- the sequencing data combine multiple genotypes

## Haplotype-Based Heterozygosity

When high-quality haplotype-level assemblies are available for the same individual, the USDA-ARS-GBRU StandardizedHeterozygosityEvaluation approach can provide a standardized SNP-based estimate.

Conceptual workflow:

1. Align haplotype assembly 1 and haplotype assembly 2 with MUMmer `nucmer`.
2. Extract non-repetitive SNPs with `show-snps -Clr`.
3. Count SNP records after removing header lines.
4. Divide by organism genome size.
5. Multiply by 100 to report percent heterozygosity.

This complements read-based k-mer estimates. It should not replace GenomeScope or Smudgeplot when raw reads are available.

Reference:

- https://github.com/USDA-ARS-GBRU/StandardizedHeterozygosityEvaluation

## hifiasm Log Peaks

hifiasm logs often include useful peak estimates. Search logs with:

```bash
grep -E "collected|genome size|peak_hom|peak_het|peak" 00_log/hifiasm_sample.err
```

Useful values:

- total collected bases
- estimated genome size
- `peak_hom`
- `peak_het`

For inbred lines, a strong homozygous peak and weak heterozygous peak can be normal. For heterozygous diploids, a heterozygous peak near half the homozygous peak may be expected. For polyploids, multiple peaks may reflect allele dosage and homeologous structure.

## Decision Rules

- Do not force the assembly to match a single genome-size estimate if independent data disagree.
- Treat k-mer estimates from contaminated read sets as suspect.
- Use genome profiling to choose between primary, haplotype-resolved, trio, or Hi-C integrated assembly strategies.
- Revisit profiling if assembly size, BUSCO duplication, Merqury spectra, and dotplots disagree.
