# Hi-C Contact Map QC Checklist

Hi-C contact maps are the main evidence for chromosome-scale scaffolding. Review them before accepting scaffolds, and archive representative screenshots for the release report.

Recent crop pangenome workflows use contact maps as curation evidence, not as decoration. A scaffold candidate is not release-ready until the contact map has been reviewed against AGP, dotplot, contamination, and expected chromosome biology.

## Whole-Genome Review

Look for:

- strong square chromosome blocks along the diagonal
- low background between unrelated chromosomes
- no obvious large off-diagonal translocation blocks
- no sudden contact drop at a scaffold join
- expected number of chromosome-scale scaffolds for the crop
- unplaced contigs staying unplaced when evidence is weak

## Per-Chromosome Review

For each chromosome-scale scaffold:

- diagonal signal is continuous
- orientation changes are supported by contact decay
- joins do not create abrupt checkerboard patterns
- chromosome ends are not joined to unrelated contigs
- repetitive centromeric regions are interpreted carefully
- telomere evidence, if available, agrees with scaffold ends

## Warning Patterns

| Pattern | Possible issue | Review action |
| --- | --- | --- |
| bright off-diagonal block | translocation, misjoin, repeat-driven signal, or true biology | compare dotplot and read evidence |
| abrupt diagonal break | unsupported join or assembly break | inspect local contigs and AGP |
| checkerboard pattern | orientation/order problem | review in Juicebox/JBAT |
| many tiny placed contigs | over-scaffolding of repeats or low-confidence contigs | consider leaving contigs unplaced |
| weak whole-map signal | poor Hi-C library or mapping issue | review read pairing, duplicates, mapping rate |
| strong signal involving organelle or contaminant contigs | non-nuclear sequence in scaffold input | remove or classify before accepting scaffold |
| apparent improvement after aggressive joining | N50-driven over-scaffolding | compare with candidate metrics and local evidence |

## Minimum Evidence to Accept Scaffolds

- Hi-C map supports order and orientation.
- Dotplot does not show an unreviewed contradiction.
- AGP validates.
- FASTA headers are release-safe.
- Contamination and organelle decisions were made before scaffolding.
- Manual curation decisions are logged.

## Screenshot Set

Archive:

```text
10_scaffolding/qc/sample.whole_genome_contact_map.png
10_scaffolding/qc/sample.chr01_contact_map.png
10_scaffolding/qc/sample.suspicious_join_edit_0001.png
10_scaffolding/qc/sample.before_after_manual_curation.png
```

## Release Rule

The final scaffold FASTA and AGP should be traceable to the contact map review. Any manual edit from Juicebox/JBAT should have a decision log row.
