# Changelog

## 0.5.0-dev

Current development focus: chromosome-scale scaffolding, contact-map review, conservative gap filling, and T2T-readiness triage.

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
