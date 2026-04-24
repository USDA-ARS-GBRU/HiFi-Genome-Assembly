# HiFi Genome Assembly Documentation

Welcome to the documentation site for the crop plant PacBio HiFi genome assembly workflow.

This project is written to help a beginning bioinformatics graduate student move from raw HiFi reads to a defensible crop genome assembly, structured review, annotation handoff, and public release package. The emphasis is not only on commands, but on why one decision is stronger than another.

## Start Paths

Choose the path that matches where you are today:

- New lab member or first real project: [How to use this protocol in a real project](how_to_use_this_protocol.md)
- Starting a brand-new assembly workspace: [Project starter kit](project_starter_kit.md)
- Want a concrete beginner example path: [Worked project paths](worked_project_paths.md)
- New to the project: [Setup](setup/index.md)
- Ready to assemble: [Assembly](assembly/index.md)
- Checking whether an assembly is trustworthy: [QC](qc/index.md)
- Reviewing structural problems by hand: [Curation](curation/index.md)
- Moving to chromosome scale: [Scaffolding and Finishing](scaffolding/index.md)
- Preparing repeats or genes: [Annotation](annotation/index.md)
- Packaging for NCBI and community databases: [Release](release/index.md)

## What This Site Covers

| Section | Status | Start here |
| --- | --- | --- |
| Setup | draft | [Setup](setup/index.md) |
| sbatch templates | active draft | [sbatch templates](sbatch/index.md) |
| helper scripts | active draft | [scripts](scripts/index.md) |
| Shared references | active draft | [sbatch Template Index](sbatch_template_index.md), [Key References](key_references.md), [PacBio Watchlist](pacbio_watchlist.md) |
| Assembly | active draft | [Assembly](assembly/index.md) |
| QC | active draft | [QC](qc/index.md) |
| Curation | maintained draft | [Curation](curation/index.md) |
| Scaffolding and finishing | active draft | [Scaffolding and Finishing](scaffolding/index.md) |
| Telomere, centromere, and T2T | active draft | [v0.6 T2T Kickoff](v0.6_t2t_kickoff.md), [T2T Claim Language](t2t_claim_language_guide.md) |
| Annotation | active draft | [Annotation](annotation/index.md), [v0.7 Repeat Kickoff](v0.7_repeat_annotation_kickoff.md), [v0.8 Gene Kickoff](v0.8_gene_annotation_kickoff.md) |
| Release | active draft | [Release](release/index.md) |
| Templates and checklists | active draft | [Templates and Checklists](workflow_templates/index.md) |

Status meanings:

- `active draft`: currently being expanded and validated.
- `maintained draft`: usable content exists and is being kept consistent.
- `early draft`: skeleton or partial content exists.
- `planned`: not yet written.

## Recommended Reading Order

For most projects, the cleanest reading order is:

1. [Software Environments](setup/environment.md)
2. [Genome Profiling](assembly/genome_profiling.md)
3. [hifiasm Workflow](assembly/hifiasm.md)
4. [Assembly Metrics](qc/assembly_metrics.md)
5. [Dotplot Misassembly Curation](dotplot_misassembly_curation.md)
6. [Hi-C Scaffolding](scaffolding/hic_scaffolding.md) or [RagTag](ragtag_workflow.md) when appropriate
7. [Repeat Library Decisions](repeat_library_decision_guide.md)
8. [Gene Set Decisions](gene_set_decision_guide.md)
9. [Release Package Decisions](release_package_decision_guide.md)

## Worked Project Paths

If you want a more concrete path instead of a section-by-section tour, start here:

- [Worked project paths](worked_project_paths.md)
- [Diploid inbred HiFi-only path](case_paths/diploid_inbred_hifi_only.md)
- [Heterozygous HiFi plus Hi-C path](case_paths/heterozygous_hifi_hic.md)

## Project Status

The public repo landing page now serves as a short front door. The detailed protocol lives here in the docs site.

Use these pages to track where the project is headed:

- [Documentation Status and Roadmap](status.md)
- [How to use this protocol in a real project](how_to_use_this_protocol.md)
- [Project starter kit](project_starter_kit.md)
- [README to Docs Migration Plan](readme_to_docs_migration_plan.md)
- [Documentation Platform Decision](site_platform_decision.md)
- [MkDocs and GitHub Pages Publishing](mkdocs_publishing.md)
- [Citation and License Review](release/citation_license_review.md)
