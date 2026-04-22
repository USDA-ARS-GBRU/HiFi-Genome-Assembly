# IGV Session Setup for Manual Correction Review

This guide describes a practical loading order for IGV when reviewing possible assembly corrections.

## Goal

Use IGV to inspect evidence on assembly coordinates. The HiFi assembly should be the genome, and the close reference should be loaded as alignments against that assembly.

## Recommended Files

```text
07_assemblies/sample.primary.fa
07_assemblies/sample.primary.fa.fai
09_dotplots/igv_reference_to_assembly/ref_to_sample.asm20.bam
09_dotplots/igv_reference_to_assembly/ref_to_sample.asm20.bam.bai
08_stats/read_depth/sample.hifi_depth.bw
10_scaffolding/hic/sample.contact_review.png
13_repeats/sample.repeats.gff3
11_contamination/sample.contamination_intervals.bed
```

## Loading Order

1. Load the HiFi assembly FASTA as the IGV genome.
2. Load the reference-to-assembly BAM.
3. Load HiFi read-depth or coverage tracks.
4. Load repeat or contamination intervals if available.
5. Navigate to contigs listed in the correction decision log or dotplot review notes.

## Track Naming

Use names that tell the reviewer what they are seeing:

```text
Reference_to_Assembly_minimap2_asm20
HiFi_Read_Depth
HiC_Break_Evidence
Repeat_Annotation
Contamination_Intervals
```

## Display Tips

- sort alignments by start or strand when orientation changes are suspected
- color alignments by strand when reviewing inversions
- keep coordinate labels visible in screenshots
- capture both a broad context view and a zoomed breakpoint view
- do not hide tracks that contradict the proposed edit

## Session Files

Save an IGV session file when possible:

```text
09_dotplots/igv/sample.edit_review.igv_session.xml
```

The session file should be archived with screenshots and correction logs so the review can be reopened later.
