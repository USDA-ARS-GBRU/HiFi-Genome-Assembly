# PacBio HiFi Genome Assembly for Crop Plants

> [!NOTE]
> This repository is under active development. Suggestions, corrections, teaching examples, and issue reports are welcome through GitHub Issues or pull requests.

This repository is a modular, beginner-friendly, peer-review-oriented workflow for assembling crop plant genomes from PacBio HiFi reads, evaluating quality, curating structure, preparing annotation, and building release-ready NCBI/INSDC submission packages.

## Documentation

The full protocol now lives in the documentation site:

- Docs site: [https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/)
- Docs home: [docs/index.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/index.md)
- Status and roadmap: [docs/status.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/status.md)
- Publishing guide: [docs/mkdocs_publishing.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/mkdocs_publishing.md)

Preserved longform snapshots are archived in [archive/README.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/archive/README.md).

## Scope

This project is designed for crop plant genome assembly work that needs to hold up in manuscript review, internal lab handoff, and public database release. The workflow emphasizes:

- PacBio HiFi-first assembly
- transparent evidence-based decisions
- conservative structural correction
- repeat and gene annotation handoff
- NCBI/community-database release readiness
- HPC-friendly execution with reusable sbatch templates and helper scripts

## Recommended Workflow

```text
metadata and sample definition
  -> read QC and preprocessing
  -> genome profiling and heterozygosity review
  -> hifiasm assembly
  -> assembly metrics and k-mer validation
  -> dotplots and structural review
  -> contamination and organelle review
  -> optional correction, scaffolding, and gap filling
  -> telomere/centromere/T2T evidence review
  -> repeat annotation and masking
  -> gene annotation and QC
  -> release bundle preparation for NCBI/INSDC and community databases
```

## Start Here

For most users, the best entry points are:

1. [Setup](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/setup/)
2. [Assembly](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/assembly/)
3. [QC](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/qc/)
4. [Curation](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/curation/)
5. [Scaffolding and Finishing](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/scaffolding/)
6. [Annotation](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/annotation/)
7. [Release](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/release/)

Useful focused pages:

- Environment setup: [docs/setup/environment.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/setup/environment.md)
- hifiasm workflow: [docs/assembly/hifiasm.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/assembly/hifiasm.md)
- Dotplot curation: [docs/dotplot_misassembly_curation.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/dotplot_misassembly_curation.md)
- Gap filling: [docs/gap_filling_workflow.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/gap_filling_workflow.md)
- Repeat annotation: [docs/repeat_library_decision_guide.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/repeat_library_decision_guide.md)
- Gene annotation: [docs/gene_set_decision_guide.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/gene_set_decision_guide.md)
- NCBI release: [docs/release/index.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/release/index.md)

## Repository Contents

Top-level resources include:

- `docs/`: MkDocs source for the public documentation site
- `01_sbatch_templates/`: reusable Slurm templates
- `scripts/`: helper scripts for QC, audits, reporting, and release checks
- `examples/`: toy inputs, decision tables, validation fixtures, and release examples
- `.github/workflows/`: CI and docs deployment workflows

Helpful indexes:

- sbatch templates: [docs/sbatch_template_index.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/sbatch_template_index.md)
- shared references: [docs/key_references.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/key_references.md)
- PacBio watchlist: [docs/pacbio_watchlist.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/pacbio_watchlist.md)

## Version and Roadmap

Current project version: **v0.5.0-dev**

Current roadmap state:

- `v0.5`: content review for scaffolding, gap filling, T2T readiness, and docs migration
- `v0.6`: active draft baseline for telomere, centromere, and completeness claims
- `v0.7`: active draft baseline for repeat annotation refinement
- `v0.8`: active draft baseline for gene annotation refinement
- `v0.9`: active draft baseline for NCBI release-candidate polish
- `v1.0`: stable public protocol target

See:

- [VERSION](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/VERSION)
- [CHANGELOG.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/CHANGELOG.md)
- [docs/status.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/docs/status.md)

## Contributing and Reuse

- Contributing: [CONTRIBUTING.md](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/CONTRIBUTING.md)
- Citation metadata: [CITATION.cff](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/CITATION.cff)
- License: [LICENSE](/Users/rothconrad/Library/CloudStorage/OneDrive-UniversityofGeorgia/Binf-protocols/HiFi-Genome-Assembly/LICENSE)

This project is being written so a beginning bioinformatics graduate student can follow the logic, not just copy commands. Contributions that improve clarity, evidence standards, examples, or release readiness are especially valuable.
