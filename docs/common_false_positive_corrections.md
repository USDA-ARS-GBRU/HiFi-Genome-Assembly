# Common False Positive Correction Signals

Many suspicious patterns are not true misassemblies. This page lists common false positives that can lead to overcorrection.

## Dotplot False Positives

| Signal | Why it can be misleading | Review response |
| --- | --- | --- |
| Inversion-like block | Real cultivar inversion or reference orientation issue | Check Hi-C, alternate references, and read continuity |
| Broken diagonal in repeats | Repeat collapse, TE expansion, or low uniqueness | Inspect repeat annotation and depth before splitting |
| Chromosome jump | Introgression, translocation, or reference-specific structure | Use multiple references and IGV review |
| Assembly-only sequence | Reference gap or accession-specific sequence | Screen contamination, then retain if supported |
| Small scattered hits | Low-complexity or repetitive alignments | Filter by length/identity for whole-genome plots |

## PAF/Minimap False Positives

- secondary alignments can make duplicated regions look chimeric
- distant references can create fragmented alignments
- overly permissive presets may align repeats as structural evidence
- overly strict filters can hide the true transition around a breakpoint
- query/target orientation can confuse interpretation if not documented

## RagTag and Reference-Guided False Positives

- clean reference-like output can hide real accession structure
- many proposed breaks in a HiFi assembly may indicate overcorrection
- small contigs may be placed confidently against the wrong repeat-rich region
- scaffolding can improve N50 while worsening biological truth

## Pteranodon and Interactive Editing False Positives

- point-and-click edits can be too easy to accept without enough evidence
- visual summaries may hide weak read or k-mer support
- auto mode should be reviewed like any other candidate generator

## Manual Review False Positives

- IGV screenshots without coordinate context can be misleading
- alignment pileups in repeats can look like breakpoints
- one reference ending at a coordinate does not prove the assembly breaks there
- lack of reference alignment can mean novel sequence, not error

## Rule of Thumb

If the evidence does not define a precise coordinate and an independent support track, record the region as reviewed and retained.
