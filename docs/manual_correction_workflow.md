# Manual Evidence-First Correction Workflow

High-quality PacBio HiFi contigs usually should not require many manual breaks. When misassemblies occur, they are expected to be rare and often associated with difficult repetitive regions, collapsed repeats, haplotig confusion, organellar insertions, or unresolved structural variation. A correction workflow should therefore be conservative.

## Why Not Auto-Break Everything?

Algorithmic correction tools can be useful for triage, but they may introduce too many breaks when a crop genome differs structurally from the reference. Reference-guided methods are especially risky in species with cultivar-specific inversions, introgressions, recent duplications, and pan-genome presence/absence variation.

Use automated tools to nominate suspicious regions. Accept a break only after manual review and independent evidence.

Tools to treat as candidate generators:

- RagTag `correct`
- Breakwright-style algorithmic breakpoint searches
- Pteranodon auto mode
- PAF or MUMmer structural-difference summaries

## Preferred Manual Workflow

1. Generate whole-genome dotplots against a close reference and, when possible, another related assembly.
2. Mark questionable contigs or scaffolds from the dotplot.
3. Map the reference genome to the HiFi assembly with minimap2 and produce a sorted BAM.
4. Open the HiFi assembly as the IGV genome and load the reference-to-assembly BAM.
5. Scroll through only the questionable contigs, looking for places where the reference alignment clearly breaks, switches chromosome, changes orientation, or loses support.
6. Record the candidate coordinate in the correction decision log.
7. Validate the breakpoint table with `scripts/validate_breaks.py`.
8. Split the FASTA with `scripts/split_fasta_at_breaks.py`.
9. Regenerate dotplots, AGP, FASTA index, and downstream release files.

## Reference-to-Assembly IGV Mapping

In this workflow, the HiFi assembly is the alignment target and the reference genome is the query. This makes the BAM load naturally on the assembly coordinates in IGV.

```bash
sbatch \
  --export assembly=07_assemblies/sample.primary.fa,reference=references/close_reference.fa,sample=ref_to_sample,preset=asm20 \
  01_sbatch/minimap_reference_to_assembly_igv.sbatch
```

Open the assembly FASTA as the IGV genome, then load:

```text
09_dotplots/igv_reference_to_assembly/ref_to_sample.asm20.bam
```

Look for:

- reference alignments ending abruptly near the dotplot discordance
- adjacent reference segments from different chromosomes
- clear strand/orientation changes supported by the alignment pattern
- gaps or repetitive piles where a confident breakpoint cannot be chosen

## Breakpoint Recording

Use `break_after_1based`. If the last supported base before the break is 14500001, record:

```text
sequence_id	break_after_1based	action	evidence	reviewer	notes
chr03	14500001	break	reference-to-assembly IGV break plus dotplot jump	ReviewerName	Break after base 14500001.
```

Validate before splitting:

```bash
scripts/validate_breaks.py \
  --fasta 07_assemblies/sample.primary.fa \
  --breaks 00_metadata/sample.breaks.tsv \
  -o 00_metadata/sample.breaks.validation.tsv
```

Then split:

```bash
scripts/split_fasta_at_breaks.py \
  --fasta 07_assemblies/sample.primary.fa \
  --breaks 00_metadata/sample.breaks.tsv \
  -o 07_assemblies/sample.primary.corrected.fa \
  --map 00_metadata/sample.split_map.tsv
```

## Acceptance Rule

If you cannot find a defensible breakpoint by manual inspection, do not split. Record the region as reviewed and retained. A slightly suspicious contig with strong HiFi support is usually better than a fragmented assembly created by overcorrection.

## Tool Notes

- Breakwright: https://github.com/rotheconrad/Breakwright
- Pteranodon: https://github.com/w-korani/Pteranodon
- IGV: https://igv.org/
- minimap2: https://github.com/lh3/minimap2
