# IGV Breakpoint Reporting Guide

Use IGV as a manual evidence viewer, not as a standalone correction algorithm. The goal is to document exactly why a breakpoint was accepted or rejected.

## Setup

For reference-to-assembly review:

1. Open the HiFi assembly FASTA as the IGV genome.
2. Load the BAM created by `01_sbatch/minimap_reference_to_assembly_igv.sbatch`.
3. Load optional tracks such as HiFi read depth, Hi-C evidence summaries, repeat annotation, or contamination intervals.
4. Navigate only to contigs flagged by dotplot review or another evidence source.

See `docs/igv_session_setup.md` for loading order, track naming, and session-file guidance.

## Screenshot Set

For each accepted break, archive:

- whole-contig view showing the suspicious alignment pattern
- zoomed breakpoint view with coordinate visible
- neighboring sequence context on both sides of the break
- optional read-depth or Hi-C evidence panel
- after-correction dotplot or alignment view

For each retained suspicious region, archive:

- focused dotplot or IGV view showing the reviewed region
- evidence supporting retention
- short note explaining why no edit was made

## File Names

Use stable names that connect to the correction log:

```text
09_dotplots/igv/edit_0001.chr03.whole_contig.png
09_dotplots/igv/edit_0001.chr03.breakpoint_zoom.png
09_dotplots/igv/edit_0001.chr03.read_depth.png
09_dotplots/igv/edit_0001.after_correction_dotplot.png
```

## Caption Template

```text
Edit [edit_id] on [sequence_id]. Reference-to-assembly minimap2 alignments were viewed in IGV with the HiFi assembly as the genome. The accepted breakpoint was recorded as break_after_1based=[coordinate]. The alignment pattern showed [description], supported by [secondary evidence]. Downstream FASTA, AGP, and release validation files were regenerated after correction.
```

## What to Avoid

- screenshots without visible coordinate labels
- screenshots cropped so tightly that orientation/context is unclear
- images that hide tracks contradicting the proposed edit
- unversioned filenames such as `break.png`
- edits made from IGV inspection without a correction log row

## Release Rule

The correction log should point to the IGV image filenames or an evidence directory. A reviewer should be able to move from the log row to the screenshot, then to the command that generated the BAM, then to the corrected FASTA.
