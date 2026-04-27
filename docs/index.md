# HiFi Genome Assembly Documentation

Welcome to the documentation site for the crop plant PacBio HiFi genome assembly workflow.

Repo: [USDA-ARS-GBRU/HiFi-Genome-Assembly](https://github.com/USDA-ARS-GBRU/HiFi-Genome-Assembly)

This project is written to help a beginning bioinformatics graduate student move from raw HiFi reads to a defensible crop genome assembly, structured review, annotation handoff, and public release package. The emphasis is not only on commands, but on why one decision is stronger than another.

## Current Method Stance

Recent crop genome publications support a clear default path:

- start PacBio HiFi crop assemblies with `hifiasm`
- use alternate assemblers as diagnostic comparisons, not random replacements
- use Hi-C or similarly strong long-range evidence for chromosome-scale scaffolding
- reserve near-T2T or T2T language for projects with extra evidence for centromeres, telomeres, rDNA, satellites, and gap closure
- evaluate plant genomes with multiple evidence layers: BUSCO, Merqury, LAI or other repeat-space checks, dotplots/contact maps, read mapping, contamination review, and release validation

This site is organized around that default, then gives escalation paths when the data or publication goal requires more.

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

## Sidebar Organization

The sidebar is organized into four practical buckets:

- `Walkthroughs`: onboarding pages, worked project paths, review packets, and hard cases
- `Support Files`: sbatch templates, scripts, checklists, and shared references
- `Workflow Steps`: the end-to-end protocol from setup through release
- `Development Project`: roadmap, validation planning, docs-site work, and internal release history

If you are new here, start with `Walkthroughs` or `Workflow Steps`. If you are implementing or adapting the workflow, `Support Files` is usually the fastest route. If you are helping maintain the project itself, use `Development Project`.

## Four Ways To Navigate

### Walkthroughs

Start here when you want guidance, examples, and packet-style reading paths.

- [Walkthroughs overview](walkthroughs.md)
- [How to use this protocol](how_to_use_this_protocol.md)
- [Worked project paths](worked_project_paths.md)

### Support Files

Start here when you need reusable files, templates, scripts, or reference material.

- [Support files overview](support_files.md)
- [sbatch templates](sbatch/index.md)
- [scripts](scripts/index.md)

### Workflow Steps

Start here when you want the protocol in biological and operational order.

- [Workflow steps overview](workflow_steps.md)
- [Setup](setup/index.md)
- [Release](release/index.md)

### Development Project

Start here when you are maintaining the docs project itself.

- [Development project overview](development_project.md)
- [Status and roadmap](status.md)
- [Human validation runbook](human_validation_runbook.md)

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
4. [Alternate Assembler Comparison](assembly/alternate_assemblers.md), only if the default assembly needs a diagnostic comparison
5. [Assembly Metrics](qc/assembly_metrics.md)
6. [Dotplot Misassembly Curation](dotplot_misassembly_curation.md)
7. [Hi-C Scaffolding](scaffolding/hic_scaffolding.md) or [RagTag](ragtag_workflow.md) when appropriate
8. [Advanced T2T Methods](t2t_advanced_methods.md), only when the project is aiming beyond ordinary chromosome scale
9. [Repeat Library Decisions](repeat_library_decision_guide.md)
10. [Gene Set Decisions](gene_set_decision_guide.md)
11. [Release Package Decisions](release_package_decision_guide.md)

## Worked Project Paths

If you want a more concrete path instead of a section-by-section tour, start here:

- [Worked project paths](worked_project_paths.md)
- [Diploid inbred HiFi-only path](case_paths/diploid_inbred_hifi_only.md)
- [Heterozygous HiFi plus Hi-C path](case_paths/heterozygous_hifi_hic.md)
- [Reference-guided crop path](case_paths/reference_guided_crop.md)
- [Polyploid crop path](case_paths/polyploid_crop.md)

## Project Status

The public repo landing page now serves as a short front door. The detailed protocol lives here in the docs site.

Use these pages to track where the project is headed:

- [Documentation Status and Roadmap](status.md)
- [Active Draft Lanes](active_draft_lanes.md)
- [How to use this protocol in a real project](how_to_use_this_protocol.md)
- [Project starter kit](project_starter_kit.md)
- [Human validation runbook](human_validation_runbook.md)
- [README to Docs Migration Plan](readme_to_docs_migration_plan.md)
- [Documentation Platform Decision](site_platform_decision.md)
- [MkDocs and GitHub Pages Publishing](mkdocs_publishing.md)
- [Citation and License Review](release/citation_license_review.md)
- [GitHub repository](https://github.com/USDA-ARS-GBRU/HiFi-Genome-Assembly)
