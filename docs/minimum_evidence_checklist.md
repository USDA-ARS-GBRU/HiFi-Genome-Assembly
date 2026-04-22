# Minimum Evidence Checklist for Assembly Corrections

Use this checklist before changing a crop plant HiFi assembly. The default posture is conservative: retain sequence unless independent evidence supports a specific edit.

## Decision Table

| Decision | Minimum evidence | Default bias |
| --- | --- | --- |
| Retain | Assembly-supported structure with no clear independent contradiction | Retain unless a clear error is demonstrated |
| Break | Dotplot discordance plus at least one independent support track at the same coordinate | Do not break unless the coordinate is defensible |
| Reverse complement | Orientation conflict supported by Hi-C or multiple close references | Retain current orientation unless support is strong |
| Remove | Contamination, organelle, vector, adapter, or unsupported artifact evidence | Retain or submit separately until evidence is clear |
| Mask | Localized low-confidence sequence or adapter/vector region not requiring removal | Prefer targeted masking over deletion |
| Submit separately | Real non-nuclear, alternate, or haplotype sequence not appropriate for the nuclear primary assembly | Do not discard biologically valid sequence |

Machine-readable examples are in `examples/correction_evidence_checklist.tsv`.

## Evidence Types

Useful independent evidence includes:

- reference-to-assembly IGV inspection
- whole-genome dotplot
- focused contig/chromosome dotplot
- HiFi read alignment depth
- Hi-C contact map
- k-mer copy-number or Merqury evidence
- contamination/taxonomy screen
- organelle alignment evidence
- multiple close references or haplotype assemblies
- manual review notes from the correction decision log

## Strong Break Criteria

A strong manual break usually has:

- a suspicious dotplot pattern
- a reference-to-assembly alignment break at a precise assembly coordinate
- a second support track such as Hi-C, read depth, k-mer behavior, or an alternate reference
- a validated `break_after_1based` coordinate
- a plan to regenerate downstream FASTA index, AGP, repeat, gene, and release files

## Weak Break Criteria

Do not break for these reasons alone:

- a single reference disagrees with the assembly
- an automated tool proposes many candidate breaks
- the edit improves N50 or visual tidiness
- a repetitive region is confusing but lacks a precise coordinate
- a crop accession differs from a reference cultivar

## Documentation Rule

Every accepted edit needs a correction decision log entry, before/after evidence, and a post-correction validation record. Every rejected edit should also be documented when it was reviewed seriously.
