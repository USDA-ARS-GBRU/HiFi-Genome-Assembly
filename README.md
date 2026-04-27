# PacBio HiFi Genome Assembly for Crop Plants

> [!NOTE]
> This repository is under active development. Suggestions, corrections, teaching examples, and issue reports are welcome through GitHub Issues or pull requests.

This repository is a modular, beginner-friendly, peer-review-oriented workflow for assembling crop plant genomes from PacBio HiFi reads, evaluating quality, curating structure, preparing annotation, and building release-ready NCBI/INSDC submission packages.

## Documentation

The full protocol now lives in the documentation site:

- Docs site: [https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/)
- [Docs Home](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/)
- [Status and Roadmap](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/status/)
- [Publishing Guide](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/mkdocs_publishing/)

The repo-tracked source for documentation status remains `docs/status.md`.

Preserved longform snapshots are archived in [Archive Overview](https://github.com/USDA-ARS-GBRU/HiFi-Genome-Assembly/blob/main/archive/README.md).

## Scope

This project is designed for crop plant genome assembly work that needs to hold up in manuscript review, internal lab handoff, and public database release. The workflow emphasizes:

- PacBio HiFi-first assembly with hifiasm as the default published-method starting point
- systematic alternate-assembler comparison when the default assembly is suspicious
- Hi-C/contact-map-supported scaffolding when chromosome-scale structure is a project goal
- explicit escalation criteria for near-T2T or T2T claims
- plant-specific QC beyond N50, including k-mer validation, gene-space checks, repeat-space checks, structural review, and contamination screening
- transparent evidence-based decisions
- conservative structural correction
- repeat and gene annotation handoff
- NCBI/community-database release readiness
- HPC-friendly execution with reusable sbatch templates and helper scripts

## Published-Method Defaults

Recent high-profile crop genome and pangenome papers support two practical lanes for this protocol:

- **Chromosome-scale pangenome/reference lane:** PacBio HiFi plus `hifiasm` for contigs, Hi-C/Omni-C or carefully documented reference/map evidence for ordering, BUSCO plus Merqury and plant repeat-space metrics such as LAI, EDTA/RepeatMasker repeat annotation, and evidence-integrated gene annotation.
- **Near-T2T/T2T escalation lane:** standard HiFi assemblies are usually not enough for the hardest centromeric, rDNA, satellite, and telomeric repeats. Projects making T2T-style claims should plan for additional evidence such as ultra-long ONT, Hi-C, optical maps, cytogenetic evidence, targeted gap filling, and explicit repeat-region validation.

The default workflow therefore starts with a conservative hifiasm assembly, then escalates only when the biology, QC results, and project goal justify extra methods.

## Recommended Workflow

```text
metadata and sample definition
  -> read QC and preprocessing
  -> genome profiling and heterozygosity review
  -> hifiasm primary assembly
  -> optional alternate-assembler diagnostic comparison
  -> assembly metrics, k-mer validation, and plant repeat-space QC
  -> dotplots and structural review
  -> contamination and organelle review
  -> optional correction, scaffolding, and gap filling
  -> telomere/centromere/T2T evidence review when claims require it
  -> repeat annotation, masking, and library decision
  -> evidence-integrated gene annotation and QC
  -> release bundle preparation for NCBI/INSDC and community databases
```

## Project Starter Kit

The project starter kit is the quickest way to turn this protocol into a real working directory with the right first files, folders, and decision logs.

- [Project Starter Kit](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/project_starter_kit/)

Use it when you are:

- starting a new species or cultivar project
- setting up the first directory structure on HPC
- deciding which metadata files to create before large jobs start
- onboarding a new lab member into the workflow

## Worked Project Paths

The worked project paths are opinionated beginner routes through the protocol for common crop assembly situations.

[Worked Project Paths](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/worked_project_paths/)

- [Diploid Inbred HiFi-Only](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/case_paths/diploid_inbred_hifi_only/)
- [Heterozygous HiFi Plus Hi-C](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/case_paths/heterozygous_hifi_hic/)
- [Reference-Guided Crop](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/case_paths/reference_guided_crop/)
- [Polyploid Crop](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/case_paths/polyploid_crop/)

Use them when you want:

- a realistic first-pass reading order
- clearer guidance on what to postpone
- a better sense of which outputs to keep and which cautions matter most
- a path that feels closer to an actual crop project than a generic tool index

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

- [Environment Setup](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/setup/environment/)
- [hifiasm Workflow](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/assembly/hifiasm/)
- [Dotplot Curation](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/dotplot_misassembly_curation/)
- [Gap Filling](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/gap_filling_workflow/)
- [Repeat Annotation](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/repeat_library_decision_guide/)
- [Gene Annotation](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/gene_set_decision_guide/)
- [NCBI Release](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/release/)

## Repository Contents

Top-level resources include:

- `docs/`: MkDocs source for the public documentation site
- `01_sbatch_templates/`: reusable Slurm templates
- `scripts/`: helper scripts for QC, audits, reporting, and release checks
- `examples/`: toy inputs, decision tables, validation fixtures, and release examples
- `.github/workflows/`: CI and docs deployment workflows

Helpful indexes:

- [sbatch Template Index](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/sbatch_template_index/)
- [sbatch Templates Section](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/sbatch/)
- [Scripts Section](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/scripts/)
- [Key References](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/key_references/)
- [PacBio Watchlist](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/pacbio_watchlist/)
- [Project Starter Kit](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/project_starter_kit/)

## Version and Roadmap

Current project version: **v0.9.0-dev**

Current roadmap state:

- `v0.1-v0.4`: historical baselines for assembly core, QC, validation, and curation
- `v0.5`: signed-off stable baseline for scaffolding, gap filling, T2T readiness, and docs migration
- `v0.6`: completed first-draft packet for telomere, centromere, and completeness claims
- `v0.7`: completed first-draft packet for repeat annotation refinement
- `v0.8`: completed first-draft packet for gene annotation refinement
- `v0.9`: current active development lane for release-packet tightening and submitter handoff polish
- `v1.0`: stable public protocol target

See:

- [Version Status](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/status/)
- [Active Draft Lanes](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/active_draft_lanes/)
- [Changelog](https://github.com/USDA-ARS-GBRU/HiFi-Genome-Assembly/blob/main/CHANGELOG.md)
- [Documentation Roadmap](https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/status/)

## Contributing and Reuse

- [Contributing Guide](https://github.com/USDA-ARS-GBRU/HiFi-Genome-Assembly/blob/main/CONTRIBUTING.md)
- [Citation Metadata](https://github.com/USDA-ARS-GBRU/HiFi-Genome-Assembly/blob/main/CITATION.cff)
- [License](https://github.com/USDA-ARS-GBRU/HiFi-Genome-Assembly/blob/main/LICENSE)

This project is being written so a beginning bioinformatics graduate student can follow the logic, not just copy commands. Contributions that improve clarity, evidence standards, examples, or release readiness are especially valuable.

### Corresponding Contact

Contact info for current maintaining author

Roth Conrad: roth.conrad@uga.edu

## License

This software is a work of the United States Department of Agriculture, Agricultural Research Service and is released under a Creative Commons CC0 public domain attribution - see the LICENSE.txt file for details

## Acknowledgments

Thanks to everyone from the GBRU team.

### Funding Support
This is a project supported by the U.S. Department of Agriculture - Agricultural Research Service (USDA-ARS) - Genomics and Bioinformatics Research Unit (GBRU) through CRIS Project No. 6066-21310-006-000-D.
Additional project support was through <and any additional agreements or grants>.
