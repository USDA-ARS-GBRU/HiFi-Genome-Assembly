# sbatch Template Index

This page is the lightweight guide to the reusable Slurm templates in:

```text
01_sbatch_templates/
```

The templates are examples, not cluster-independent production scripts. Copy them into a project-specific `01_sbatch/` directory and adapt:

- partition or queue
- account
- walltime
- memory
- module names or environment activation
- path conventions

## Core Assembly Templates

- `bam2fastq.sbatch`
- `hifiasm.sbatch`
- `busco.sbatch`
- `mummer_plot.sbatch`

Use these first when teaching the basic path from raw reads to contigs and QC.

## Curation Templates

- `minimap_reference_to_assembly_igv.sbatch`
- `post_correction_validation.sbatch`

These support the evidence-first v0.4 correction workflow.

## Scaffolding and Finishing Templates

- `yahs_hic_scaffolding.sbatch`
- `3d_dna_scaffold.sbatch`
- `ragtag_correct_scaffold.sbatch`
- `lr_gapcloser.sbatch`
- `tgsgapcloser2.sbatch`
- `trfill.sbatch`

Use these only after the contig assembly has already passed structural review.

## T2T and Repeat Templates

- `tidk_telomere.sbatch`
- `quartet_telomere_centromere.sbatch`
- `edta.sbatch`
- `repeatmodeler_repeatmasker.sbatch`

These are later-stage annotation and completeness templates.

## Gene Annotation Templates

- `liftoff.sbatch`
- `braker3.sbatch`
- `maker.sbatch`
- `table2asn_validate.sbatch`

Use these after the assembly and repeat-mask decisions are frozen enough to support annotation.

## Template Rule

Treat each sbatch file as a starting point with documented intent, not as a universal script that should run unchanged on every HPC system.

## Related Files

- `docs/setup/environment.md`
- `docs/assembly/index.md`
- `docs/scaffolding/index.md`
- `docs/annotation/index.md`
- `docs/release/index.md`
