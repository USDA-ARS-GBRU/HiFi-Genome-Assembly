# Changelog

## 0.5.0-dev

Current development focus: v0.5 content review, v0.6-v0.8 active draft baselines, and v0.9 NCBI release candidate drafting.

- Promoted v0.5 to the active development version.
- v0.4 is now maintained as the dotplot and misassembly curation baseline.
- Added 3D-DNA/Juicebox/JBAT workflow guide.
- Added 3D-DNA scaffold sbatch template.
- Added T2T readiness checklist.
- Added gap-filling report helper and toy gap-filled FASTA example.
- Added documentation-site migration plan for the eventual GitHub-compatible web documentation split.
- Updated README versioning, roadmap, inventories, scaffolding references, and gap-filling examples.
- Added scaffolding candidate comparison helper and guidance.
- Added terminal telomere motif summary helper and workflow.
- Added initial documentation-site section index pages.
- Added AGP definition, AGP summary workflow, and AGP summary helper.
- Added first focused hifiasm docs page for the future web documentation.
- Added T2T readiness report helper and centromere candidate example table.
- Added web-doc AGP page under scaffolding.
- Added focused read-preparation docs page with btrim/HiFiAdapterFilt decision logic.
- Added empty centromere fixture to test unsupported T2T readiness cases.
- Added focused genome-profiling docs page.
- Added focused contamination-review docs page.
- Added local Markdown link checker for documentation navigation.
- Added focused hifiasm parameter/mode docs page.
- Added focused assembly metrics interpretation docs page.
- Added CI checks that Markdown link validation sees links and fails on a broken-link fixture.
- Added focused dotplot review docs page.
- Added focused Hi-C scaffolding reader path.
- Added documentation index status table for stable/draft/planned navigation.
- Added focused NCBI submission web-doc page.
- Added focused repeat and gene annotation web-doc pages.
- Added docs coverage checker mapping README workflow steps to focused docs.
- Added documentation status and roadmap page.
- Added CONTRIBUTING, CITATION.cff, and MIT LICENSE files.
- Added project metadata checker for CI.
- Added GitHub issue and pull request templates.
- Added v0.5 review checklist with remaining feature-complete work.
- Added v0.9 NCBI release kickoff, release package decision guide, annotation submission handoff, and release decision audit helper.
- Added release methods and structured comments guide with a Genome-Assembly-Data `.cmt` example.
- Added worked v0.9 release candidate and release bundle example pages.
- Added table2asn/discrepancy triage, accession handoff, and community database release companion guides.
- Added identifier crosswalk example and table2asn reviewer-response examples.
- Preserved the longform README in `archive/readme/` and started MkDocs documentation-site scaffolding with the first README condensation pass for software setup.
- Added GitHub Pages MkDocs deployment workflow, publishing guide, a second archived README snapshot, and the first assembly-focused README condensation pass.
- Added a third archived README snapshot, documented the current private-repo Pages blocker, ignored local MkDocs build artifacts, and condensed the README QC and curation sections.
- Added a fourth archived README snapshot, moved the remaining sbatch/reference/roadmap tail out of the root README, and exposed shared template/reference pages in MkDocs navigation.
- Added a fifth archived README snapshot and converted the root README into a short landing page that points readers to the live documentation site.
- Refined the docs home page into a clearer newcomer entry point, added a templates/checklists section, moved preserved README snapshots into `archive/readme/`, archived the legacy top-level NCBI submission page, and updated the GitHub Pages workflow to current documented action versions.
- Updated README and docs status with current v0.5 assessment.
- Added worked scaffolding decision case with candidate metrics, decision-log rows, methods text, and reviewer response language.
- Added README-to-docs migration plan with the section-shortening order for the future GitHub documentation split.
- Added public release metadata audit and citation/license review guide.
- Added beginner usability review guide and tracking fixture for outside-reader testing.
- Added v0.5 release-candidate notes and tagging dry-run checklist.
- Started v0.6 drafting with kickoff guide, T2T completeness evidence package, and example evidence table.
- Added tidk and quarTeT sbatch templates for v0.6 telomere/centromere review.
- Added T2T completeness evidence audit helper with positive and overclaim fixtures.
- Added manuscript and reviewer-response language guide for chromosome completeness claims.
- Added worked completeness claim case translating mixed evidence into manuscript and reviewer-response language.
- Started v0.7 repeat annotation drafting with kickoff guide, repeat library decision guide, and example decision table.
- Updated README release and roadmap sections to reflect v0.5 review, v0.6 draft baseline, and v0.7 active drafting.
- Added repeat summary comparison and repeat annotation decision audit helpers with positive and negative fixtures.
- Added repeat landscape interpretation guide and repeat-to-gene-annotation handoff checklist.
- Started v0.8 gene annotation drafting with kickoff guide, gene set decision guide, and example decision table.
- Updated README and release docs to reflect v0.5 review plus v0.6-v0.8 drafting lanes.
- Added annotation summary comparison and gene annotation decision audit helpers with positive and negative fixtures.
- Added functional annotation guide and annotation QC dashboard guide.

## 0.4.0-dev

Current development focus: dotplot review, evidence-first manual curation, conservative assembly correction, and post-correction validation.

- Promoted v0.4 to the active development version.
- v0.3 is now maintained as the release-readiness baseline.
- Added minimum evidence checklist for correction decisions.
- Added IGV breakpoint reporting guide.
- Added post-correction validation mini-workflow and sbatch template.
- Added post-correction report template.
- Added correction decision audit helper.
- Added rejected-correction examples.
- Added v0.4 curation workflow index.
- Added toy manual correction case study.
- Added correction report generator.
- Added pre/post correction FASTA stats comparison helper.
- Updated Step 8 to point readers into the v0.4 curation workflow.
- Added IGV session setup guide.
- Added common false-positive correction guide.
- Added v0.4 release-candidate checklist.
- Added v0.4 review-pass document.
- Added README inventory checker.
- Added v0.5 scaffolding kickoff guide.
- Refined YaHS Hi-C scaffolding template and workflow guide.
- Added Hi-C contact map QC checklist.
- Added scaffolding decision log template.
- Added conservative gap-filling workflow.
- Added LR_Gapcloser, TGS-GapCloser2, and TRFill sbatch templates.
- Added FASTA gap summarizer helper.
- Added gap-filling decision log example.

## 0.3.0-dev

Release-readiness baseline:

- FASTA and AGP release-readiness validation.
- Tool version and command-capture policy.
- Assembly decision logging.
- Standardized heterozygosity evaluation option for haplotype assemblies.
- Toy dataset and GitHub Actions validation for helper scripts.
- FCS-adaptor/FCS-GX template jobs.
- Organelle detection and release decision workflow.
- Assembly review standards.
- BlobToolKit and sourmash contamination review templates.
- Organelle PAF hit summarizer.
- Contamination decision TSV template.
- btrim option for HiFi adapter screening.
- PacBio GitHub watchlist for relevant QC and assembly guidance.
- Contamination decision tree.
- NCBI-oriented FASTA header, manifest, and release bundle helper scripts.
- EDTA and RepeatModeler2/RepeatMasker sbatch templates.
- QC figures guide for review and manuscripts.
- Added table2asn validation template and NCBI submission guide.
- Added Liftoff, BRAKER3, and MAKER sbatch templates.
- Added repeat and gene annotation strategy guides.
- Added tracked toy release bundle so manifest audits pass as real tests.
- Added NCBI metadata template guide for BioProject, BioSample, SRA, assembly, and annotation planning.
- Added toy annotation validation fixtures and expected table2asn-style review notes.
- Added GFF3-vs-FASTA sequence ID audit helper.
- Started v0.4 dotplot and misassembly curation guide with example decision cases.
- Added accession tracking TSV linking BioProject, BioSample, SRA, Assembly, and Annotation records.
- Added correction decision log template.
- Added FASTA split helper for curated breakpoints.
- Added dotplot figure guide for reports and manuscripts.
- Added RagTag correction/scaffolding comparison guide and sbatch template.
- Added breakpoint validation helper.
- Added before/after correction report text examples for methods and reviewer response.
- Added manual reference-to-assembly IGV correction workflow.
- Added minimap2 PAF dotplot guidance and sbatch templates.
- Added correction summary helper and AGP-after-splitting guidance.
- Added cautious notes for automated correction tools including RagTag, Breakwright-style methods, and Pteranodon.

## 0.2.0

- Added peer-review QC report template.
- Added public release checklist.
- Added methods text template.
- Added release manifest example.
- Expanded QC dashboard collection for additional release metrics.
- Added quick QC plotting helper.
- Removed source note archive from the public protocol surface.

## 0.1.0

- Established longform crop plant PacBio HiFi assembly protocol.
- Added reusable sbatch templates.
- Added sample/reference metadata examples.
- Added hifiasm log metric extraction.
- Added FASTA filtering and renaming helper.
