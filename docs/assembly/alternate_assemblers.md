# Alternate Assembler Comparison

Use this page when the default `hifiasm` assembly is not enough to explain the data. Alternate assemblers are useful diagnostics, but they should not become tool shopping. Compare candidates with the same evidence package and choose the assembly that best matches the biology and release goal.

## When To Compare

Run an alternate assembly when:

- hifiasm output size strongly disagrees with genome profiling
- BUSCO, Merqury, read depth, or dotplots suggest collapse, duplication, or missing sequence
- a polyploid or highly heterozygous sample has ambiguous representation
- the project is aiming for near-T2T/T2T and includes ultra-long ONT or other long-range data
- reviewers or collaborators need evidence that the selected assembly is not an arbitrary tool choice

Do not run alternates only because one metric, such as N50, looks disappointing.

## Tool Roles

| Tool | Best role | Required inputs | Caution |
| --- | --- | --- | --- |
| hifiasm | primary PacBio HiFi default for most crop projects | PacBio HiFi, optional Hi-C/trio data | default output still needs QC and structural review |
| HiCanu | diagnostic comparator for HiFi assemblies | PacBio HiFi | slower; compare full QC, not contiguity alone |
| Flye | diagnostic comparator or training/simple workflow comparison | PacBio HiFi or ONT depending on mode | useful as a comparator, not the current crop default |
| IPA/pbipa | PacBio-supported comparison path where locally available | PacBio HiFi | installation and support vary by cluster |
| Verkko | advanced near-T2T/T2T hybrid lane | PacBio HiFi plus ONT, usually ultra-long | changes project design; not a drop-in replacement |
| hifiasm-UL / ONT-aware hifiasm modes | advanced hybrid or ONT-heavy lane | PacBio HiFi plus ONT or ONT-only depending on mode/version | check current official docs before using in a protocol run |
| Canu/NECAT/NextDenovo | ONT-heavy or historical comparator paths | ONT or HiFi depending on mode | often used as supporting assemblies in T2T papers, not as the ordinary HiFi default |

## Comparison Package

For each candidate, collect the same evidence:

```text
assembly FASTA
assembler logs
tool versions and parameters
seqkit or BBTools assembly statistics
BUSCO genome-mode summary
Merqury QV, completeness, and spectra-cn plots
read-to-assembly mapping summary when used
contamination and organelle screening status
dotplots against close references or candidate assemblies
Hi-C contact map if scaffolding or phasing is involved
```

Use the same read set, same k-mer database, same BUSCO lineage, and same contamination filters whenever possible.

## Decision Table

| Observation | Likely meaning | Action |
| --- | --- | --- |
| Alternate has higher N50 but worse Merqury or dotplots | contiguity may be inflated by joins, collapse, or missing sequence | do not choose on N50 alone |
| Alternate recovers missing BUSCOs but inflates total size | may retain haplotigs, homeologs, or real duplicated biology | inspect spectra-cn, depth, and dotplots |
| hifiasm and alternate agree on structure | stronger support for the selected representation | document agreement and keep both logs |
| candidates disagree in a known SV-rich region | could be true biology or assembly error | require read, Hi-C, or reference-independent evidence |
| hybrid/T2T tool closes repeat-rich gaps | promising but higher risk | validate with spanning reads, depth, telomere/centromere/rDNA checks, and before/after alignments |

## Assembly Merging Warning

Do not merge assemblies simply because each contains attractive pieces. Assembly mergers can duplicate sequence, collapse alleles, import structural errors, or hide unsupported joins. If a contig from another assembly is used to patch a gap or correct a region, treat it as a targeted correction with independent evidence and a decision log.

## Recommended Outcome

The final decision should state:

- which assembly is the release candidate
- which candidates are comparison-only
- which metric conflicts remain unresolved
- whether the selected assembly represents a primary, haplotype-aware, subgenome-aware, chromosome-scale, near-gapless, or candidate T2T product
- what evidence would be needed to escalate further

## Related Pages

- [hifiasm workflow](hifiasm.md)
- [hifiasm parameters and assembly modes](hifiasm_parameters.md)
- [assembly metrics](../qc/assembly_metrics.md)
- [advanced T2T methods](../t2t_advanced_methods.md)
