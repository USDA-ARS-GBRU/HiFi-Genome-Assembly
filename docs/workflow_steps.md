# Workflow Steps

This section is the end-to-end protocol path.

Use these pages when you want to move through the actual assembly workflow from project setup to release packaging.

## Published-Method Plan

The workflow now follows a staged plan grounded in recent crop genome publications:

1. Build a defensible HiFi contig assembly with `hifiasm`.
2. Compare alternate assemblers only when QC or biology gives a reason.
3. Use BUSCO, Merqury, repeat-space metrics such as LAI, read mapping, contamination review, and structural plots as a combined evidence set.
4. Scaffold with Hi-C/Omni-C, reference/map evidence, or RagTag only when the project goal and evidence justify chromosome-scale organization.
5. Treat T2T as a separate escalation lane requiring additional evidence for long repeats, centromeres, telomeres, rDNA arrays, and gap closure.
6. Freeze sequence IDs before repeat annotation, gene annotation, and release packaging.

## Step Order

The main workflow moves in this order:

1. [Setup](setup/index.md)
2. [Assembly](assembly/index.md)
3. [QC](qc/index.md)
4. [Curation](curation/index.md), when structural review is needed
5. [Scaffolding and Finishing](scaffolding/index.md), when moving toward chromosome scale
6. [Annotation](annotation/index.md)
7. [Release](release/index.md)

## Best Uses

- following the protocol in biological order
- orienting a new project without jumping between helper pages
- deciding which section should come next
- checking whether the current project is ready to move forward

## Good Companion Pages

- [How to use this protocol in a real project](how_to_use_this_protocol.md)
- [Project starter kit](project_starter_kit.md)
- [Status and roadmap](status.md)

## Read This Way

Move forward only when the outputs of the current section are believable enough to support the next one. The protocol is meant to help you slow down at the right moments, not rush from reads to release.
