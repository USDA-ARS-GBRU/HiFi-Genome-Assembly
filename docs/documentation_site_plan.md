# Documentation Site Plan

The README is the longform source narrative while the protocol is under active development. Before v1.0, split it into a tractable GitHub-compatible documentation site built with MkDocs while preserving the README as the landing page.

## Suggested Site Structure

```text
docs/
  index.md
  setup/
    environment.md
    project_layout.md
  assembly/
    strategy.md
    hifiasm.md
    haplotypes.md
  qc/
    dashboard.md
    figures.md
    contamination.md
  curation/
    dotplots.md
    manual_breaks.md
    correction_reports.md
  scaffolding/
    yahs.md
    3d_dna_juicebox.md
    ragtag.md
    gap_filling.md
    t2t_readiness.md
  annotation/
    repeats.md
    genes.md
  release/
    ncbi.md
    manifest.md
    checklist.md
```

The initial section landing pages now exist under `docs/`. They are intentionally light index pages until the README-to-docs migration begins. A first MkDocs configuration is now maintained in `mkdocs.yml`.

The planned publication target is GitHub Pages at:

```text
https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/
```

The first focused migration pages are:

- `docs/assembly/hifiasm.md`
- `docs/assembly/prepare_reads.md`
- `docs/assembly/genome_profiling.md`
- `docs/assembly/hifiasm_parameters.md`
- `docs/qc/assembly_metrics.md`
- `docs/qc/contamination.md`
- `docs/qc/dotplots.md`
- `docs/scaffolding/agp.md`
- `docs/scaffolding/hic_scaffolding.md`
- `docs/annotation/repeats.md`
- `docs/annotation/genes.md`
- `docs/release/ncbi_submission.md`

## Migration Rules

- Keep the root README as the project overview, quickstart, and roadmap.
- Move long procedural sections into focused `docs/` pages.
- Keep commands copy-pasteable and HPC paths consistent across pages.
- Keep every helper script documented in exactly one primary page and referenced from the README inventory.
- Use MkDocs as the primary documentation framework while the content is being split out of the README.
- Preserve stable links where possible by using descriptive filenames rather than versioned filenames for durable topics.

## v1.0 Documentation Gate

Before tagging v1.0:

- README is shorter than the full manual and points to docs pages.
- All docs pages linked from README exist and pass the inventory checker.
- The roadmap states which pieces are stable and which are still examples.
- Helper scripts have at least one toy or validation command.
- sbatch templates pass shell syntax checks.
- Release guidance includes NCBI/INSDC outputs, annotation handoff, and manuscript methods language.
