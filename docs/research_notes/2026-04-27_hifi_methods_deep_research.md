# HiFi Genome Assembly Methods Deep Research Pass

Date: 2026-04-27

Purpose: collect outside resources relevant to `HiFi-Genome-Assembly`, compare them against current repo coverage, and design iterative follow-up work for each method area. This is a working research note, not yet polished protocol text.

## Current Repo Coverage

The repository already has a broad end-to-end PacBio HiFi crop genome protocol. The workflow in `README.md` and `docs/workflow_steps.md` moves from metadata and sample definition through read QC, genome profiling, hifiasm assembly, QC, curation, scaffolding/finishing, telomere/centromere/T2T review, repeat annotation, gene annotation, and NCBI/community release.

Current method areas and local files:

| Method area | Current repo coverage | Notes from local review |
| --- | --- | --- |
| Setup and HPC execution | `docs/setup/environment.md`, `docs/sbatch_template_index.md`, `01_sbatch_templates/` | HPC-friendly templates are a strength. Could add more explicit container/apptainer patterns for tools that are fragile to install. |
| Read conversion and read QC | `docs/assembly/prepare_reads.md`, `bam2fastq.sbatch`, `btrim_hifi_adapters.sbatch` | Covers BAM-to-FASTQ, seqkit, coverage estimation, conservative adapter screening with btrim/HiFiAdapterFilt/FCS-adaptor. |
| Genome profiling | `docs/assembly/genome_profiling.md` | Covers meryl/GenomeScope, Smudgeplot, heterozygosity estimate from haplotypes, and hifiasm log peaks. |
| Primary assembly | `docs/assembly/hifiasm.md`, `docs/assembly/hifiasm_parameters.md`, `hifiasm.sbatch`, `extract_hifiasm_log_metrics.py` | hifiasm is the default method. HiFi-only, Hi-C integrated, trio mode, `-l0`, `--hom-cov`, polyploid cautions, and output selection are already covered. |
| Assembly metrics and QC | `docs/qc/assembly_metrics.md`, `assembly_stats.sbatch`, `busco.sbatch`, `merqury.sbatch`, `collect_qc_dashboard.py`, `plot_qc_dashboard.py` | Strong multi-evidence framing: contiguity, BUSCO, Merqury, QUAST, read mapping/Inspector, dashboard. |
| Dotplots and structural review | `docs/qc/dotplots.md`, `docs/dotplot_misassembly_curation.md`, `docs/paf_dotplot_options.md`, `mummer_plot.sbatch`, `minimap_assembly_paf.sbatch` | Covers MUMmer, minimap2 PAF, dotPlotly/pafr/SVbyEye/wgatools/PanDots/Pteranodon, and conservative evidence standards. |
| Manual correction and validation | `docs/manual_correction_workflow.md`, `docs/post_correction_validation.md`, `post_correction_validation.sbatch`, `split_fasta_at_breaks.py`, `validate_breaks.py`, `make_correction_report.py` | Good evidence-first correction logic and downstream validation. |
| Reference-guided comparison | `docs/ragtag_workflow.md`, `ragtag_correct_scaffold.sbatch` | RagTag is framed as review aid/comparison, not automatic truth. This matches outside cautions well. |
| Contamination and organelles | `docs/qc/contamination.md`, `docs/contamination_workflow.md`, `docs/organelle_workflow.md`, `fcs_adaptor.sbatch`, `fcs_gx.sbatch`, `blobtoolkit_prep.sbatch`, `sourmash_reads.sbatch`, `organelle_screen.sbatch` | Covers FCS, BlobToolKit, sourmash, organelle reference screening, and decision categories. |
| Hi-C scaffolding | `docs/yahs_hic_workflow.md`, `docs/3d_dna_juicebox_workflow.md`, `docs/hic_contact_map_qc.md`, `yahs_hic_scaffold.sbatch`, `3d_dna_scaffold.sbatch` | YaHS and 3D-DNA/JBAT are covered with contact-map review. SALSA2 and Bionano/optical-map paths are only implicit or absent. |
| AGP and scaffold consistency | `docs/scaffolding/agp.md`, `docs/agp_summary_workflow.md`, `validate_agp.py`, `summarize_agp.py` | Good AGP-aware release logic. |
| Gap filling | `docs/gap_filling_workflow.md`, `lr_gapcloser.sbatch`, `tgsgapcloser2.sbatch`, `trfill.sbatch`, `make_gap_filling_report.py`, `summarize_fasta_gaps.py` | Covers LR_Gapcloser, TGS-GapCloser2, Gapless, TRFill, and validation. |
| Telomere/centromere/T2T | `docs/telomere_summary_workflow.md`, `docs/t2t_completeness_evidence_package.md`, `docs/t2t_readiness_checklist.md`, `tidk_telomere.sbatch`, `quartet_telomere_centromere.sbatch`, `make_t2t_readiness_report.py` | Strong conservative claim language. Could add more explicit decision examples for wrong telomere motifs and centromere evidence conflicts. |
| Repeat annotation | `docs/annotation/repeats.md`, `docs/repeat_library_decision_guide.md`, `docs/repeat_landscape_interpretation.md`, `edta.sbatch`, `repeatmodeler_repeatmasker.sbatch`, `compare_repeat_summaries.py` | Covers EDTA, RepeatModeler2/RepeatMasker, curated libraries, release-mask decisions. |
| Gene annotation | `docs/annotation/genes.md`, `docs/gene_set_decision_guide.md`, `liftoff.sbatch`, `braker3.sbatch`, `maker.sbatch`, `compare_annotation_summaries.py` | Covers Liftoff, BRAKER3, MAKER, hybrid decision logic, table2asn readiness. |
| Release and submission | `docs/release/ncbi_submission.md`, `docs/release_submission_packet.md`, `docs/release_methods_and_structured_comments.md`, `table2asn_validate.sbatch`, release audit scripts | Release lane is mature: FASTA/AGP/header/manifest validation, FCS, table2asn discrepancy triage, accession tracking, community database companion. |

## Deep Resource Inventory

### A. Read Prep, Adapter, and Input QC

| Resource | Type | Why it matters | Follow-up |
| --- | --- | --- | --- |
| Sim et al. 2022, HiFiAdapterFilt, BMC Genomics, https://doi.org/10.1186/s12864-022-08375-1 | Research publication | Strongly supports read-level adapter sanitation before assembly. The paper reports adapter sequence in 53/55 public CCS datasets and shows downstream assembly artifacts. | Add a `HiFiAdapterFilt` example path beside btrim, plus a short comparison table: btrim pattern screening vs HiFiAdapterFilt vs FCS-adaptor. |
| HiFiAdapterFilt GitHub, https://github.com/sheinasim/HiFiAdapterFilt | Tool docs | Practical command source for implementing the method. | Verify current input options and output files; decide whether to add an sbatch template or link-only recipe. |
| NCBI FCS/FCS-adaptor documentation, https://www.ncbi.nlm.nih.gov/datasets/docs/v2/data-processing/policies-annotation/quality/contamination/fcs-contamination/ | Official protocol/tool docs | NCBI uses FCS for adapter/vector and foreign contamination screening; generated docs were current as of 2026-04-06 in the search result. | Keep `fcs_adaptor.sbatch` and `fcs_gx.sbatch`; add a note that commands and databases should be checked against current NCBI docs before each release. |
| PacBio whole-genome sequencing docs, https://www.pacb.com/products-and-services/applications/whole-genome-sequencing/plant-animal/ | Vendor protocol/blog | Gives vendor-level coverage guidance and workflow framing for plant/animal HiFi assemblies. | Use only as supporting context, not as independent validation. Add a small "vendor guidance changes over time" note. |
| PacBio documentation index, https://www.pacb.com/support/documentation/ | Vendor documentation | Current instrument/library prep checklists can shift faster than papers. | Link from setup/read-prep watchlist rather than hard-code all library details. |

### B. Genome Profiling and K-mer Interpretation

| Resource | Type | Why it matters | Follow-up |
| --- | --- | --- | --- |
| GenomeScope 2.0 and Smudgeplot, Nature Communications 2020, https://doi.org/10.1038/s41467-020-14998-3 | Research publication | Direct support for k-mer-based estimation of genome size, heterozygosity, repetitiveness, and ploidy, especially in polyploids. | Strengthen `docs/assembly/genome_profiling.md` with when to use Illumina vs HiFi k-mers, coverage per homolog cautions, and a short "model fit failure" troubleshooting box. |
| meryl/Merqury docs and paper, https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02134-9 | Research publication/tool | Supports reuse of meryl databases for profiling and later assembly QV/completeness. | Add a note that early k-mer DB choices should be recorded because they propagate into Merqury. |
| Biostars duplicated BUSCO in hifiasm tree genome, https://www.biostars.org/p/483811/ | Community discussion | Useful real-world confusion: duplicated BUSCOs can mean haplotypes, recent duplication, WGD, or assembly representation, not simply "bad assembly." | Add a short FAQ in QC: "Duplicated BUSCOs: haplotigs, polyploidy, biology, or contamination?" |
| Bioinformatics SE Merqury k-mer plot interpretation, https://bioinformatics.stackexchange.com/questions/18161/understand-this-kmer-plot-from-merqury | Community discussion | Good conceptual explanation of monoploid references and heterozygous k-mer inclusion. | Link as optional reading in Merqury interpretation notes; do not overfit examples. |

### C. Assembly Engines and Assembly Modes

| Resource | Type | Why it matters | Follow-up |
| --- | --- | --- | --- |
| Cheng et al. 2021 hifiasm, Nature Methods, https://www.nature.com/articles/s41592-020-01056-5 | Research publication | Primary support for current default assembler. | Keep as key reference; add a "why hifiasm is default but not the only diagnostic assembler" paragraph. |
| hifiasm docs, HiFi-only assembly, https://hifiasm.readthedocs.io/en/stable/pa-assembly.html | Official tool docs | Confirms GFA outputs, default purging, `-l0`, `-z20`, `--primary`, `-s`, and `--hom-cov` guidance. | Audit `docs/assembly/hifiasm_parameters.md` against current hifiasm docs; add notes on cache/bin reuse and when to force fresh overlaps. |
| hifiasm docs, Hi-C integrated assembly, https://hifiasm.readthedocs.io/en/latest/hic-assembly.html | Official tool docs | Confirms Hi-C integrated phasing is not scaffolding; separate scaffolders remain needed. | The repo already says this; add a direct "hifiasm Hi-C mode output still needs scaffold review" callout. |
| hifiasm parameter reference, https://hifiasm.readthedocs.io/en/latest/parameter-reference.html | Official tool docs | Source for trio-binning with yak dumps and Hi-C syntax. | Add yak/maternal/paternal k-mer dump recipe if trio mode becomes a fuller path. |
| HiCanu paper, Genome Research 2020, https://genome.cshlp.org/lookup/doi/10.1101/gr.263566.120 | Research publication | Strong alternate HiFi assembler, especially for segmental duplications, satellites, and allelic variants. | Add an "alternate assembler comparison" page with HiCanu as diagnostic comparator when hifiasm output is suspicious. |
| Flye HiFi mode docs/tutorials, Galaxy tutorial uses hifiasm and Flye, https://training.galaxyproject.org/training-material/topics/assembly/tutorials/hifi-assembly/tutorial.html | Protocol/tutorial | Practical alternate assembly path and training material for beginners. | Add Flye as an optional diagnostic assembler, not a default replacement. Include expected output comparison with hifiasm. |
| PacBio IPA/pbipa, https://github.com/PacificBiosciences/pbipa and Biowulf notes https://helixweb.nih.gov/apps/pbipa.html | Tool docs/HPC docs | Official PacBio assembler; useful for comparison, especially if local clusters already provide it. | Add IPA to alternate assembler matrix; verify licensing/install viability on UGA/HPC before recommending. |
| PacBio blog on high-quality HiFi assemblers, https://www.pacb.com/blog/high-quality-hifi-assemblers/ | Vendor blog | Historical framing for hifiasm/HiCanu/IPA/Peregrine era. | Use as background only; do not use for parameter authority. |
| Verkko paper, Nature Biotechnology 2023, https://www.nature.com/articles/s41587-023-01662-6 | Research publication | Major missing method for HiFi + ultra-long ONT T2T-style assemblies. | Add "when HiFi-only is not enough" lane: Verkko requires ONT ultra-long reads and changes the project design. |
| Verkko GitHub/Biowulf docs, https://hpc.nih.gov/apps/verkko.html | Tool/HPC docs | Practical description of Verkko's hybrid HiFi + ONT graph workflow. | Add as a watchlist item and candidate advanced sbatch template only after local install feasibility check. |
| hifiasm-UL/double graph paper, Nature Methods 2024, https://www.nature.com/articles/s41592-024-02269-8 | Research publication | Missing modern method for scalable near-T2T diploid/polyploid assembly using multiple data types. | Add to PacBio watchlist and future "advanced T2T assembly" lane. Verify current command-line support before writing protocol. |
| Bioinformatics SE "What assembler for HiFi reads?", https://bioinformatics.stackexchange.com/questions/11158/what-assembler-is-appropriate-for-high-fidelity-pacbio-reads | Community discussion | Useful historical community answer: hifiasm, HiCanu/Canu HiFi mode, IPA; hifiasm efficiency noted. | Use only as community context in the alternate assembler comparison notes. |
| Biostars hifiasm assembly statistics question, https://www.biostars.org/p/9470684/ | Community discussion | Shows beginner pain point: hifiasm GFA outputs and basic statistics. | Add a more explicit GFA-to-FASTA and stats beginner subsection. |
| Bioinformatics SE polishing with Illumina/HiFi, https://bioinformatics.stackexchange.com/a/21997 | Community discussion | Supports caution against unnecessary Illumina polishing of HiFi assemblies. | Add a "polishing is usually not a default HiFi step" FAQ; discuss when nextPolish2 or Racon is justified. |
| Bioinformatics SE hybrid assembly versus polishing, https://bioinformatics.stackexchange.com/questions/22280/hybrid-assembly-versus-polishing-for-hifi-and-illumina-reads | Community discussion | Reinforces using short reads mostly for profiling/QC, not blindly improving HiFi assembly. | Fold into polishing FAQ. |
| Biostars combine hifiasm and hifiasm-ONT assemblies, https://www.biostars.org/p/9614177/ | Community discussion | Real-world caution against assembly merging/quickmerge creating duplications. | Add warning in alternate assembly comparison: merging is not a safe default; evidence needed. |

### D. Assembly QC and Validation

| Resource | Type | Why it matters | Follow-up |
| --- | --- | --- | --- |
| Merqury paper, Genome Biology 2020, https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02134-9 | Research publication | Strongly supports reference-free QV, completeness, spectra-cn, phasing metrics. | Add a Merqury interpretation table with common spectra-cn patterns and action steps. |
| BUSCO paper, Bioinformatics 2015, https://academic.oup.com/bioinformatics/article/31/19/3210/211866 | Research publication | Supports gene-space completeness, but also documents that this is an ortholog expectation, not whole-genome truth. | Add "BUSCO is one evidence layer" caveat in QC page. |
| BUSCO user guide, https://busco.ezlab.org/busco_userguide | Official docs | Version/lineage details change; current repo says lineage and version should be reported. | Add a release-gate reminder to record BUSCO version, ODB lineage, download date, mode, and command. |
| QUAST paper, Bioinformatics 2013, https://pmc.ncbi.nlm.nih.gov/articles/PMC3624806/ | Research publication | Supports reference and no-reference assembly metric reporting. | Keep as supporting ref; add caveat about reference-biased interpretation in divergent crops. |
| Inspector paper, Genome Biology 2021, https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02527-4 | Research publication | Supports read-mapping-based assembly error detection. | Add Inspector as optional validation where correction/read support matters; create sbatch only if used often. |
| Biostars Merqury QV question, https://www.biostars.org/p/9616205/ | Community discussion | Useful real-world confusion about Inspector vs Merqury QV and polishing after HiFi. | Use as source for a troubleshooting FAQ: "Why do QV tools disagree?" |
| Biostars genome assembly QC from BAM files, https://www.biostars.org/p/9615110/ | Community discussion | Mirrors repo philosophy: QUAST/BUSCO are not enough; need misassembly/repeat/collapse evaluation. | Add a QC decision tree from stats -> k-mers -> read mapping -> dotplots/contact maps. |

### E. Dotplots, Manual Curation, and Reference-Guided Review

| Resource | Type | Why it matters | Follow-up |
| --- | --- | --- | --- |
| minimap2 GitHub/paper, https://github.com/lh3/minimap2 | Tool docs | Current repo uses minimap2 PAF for assembly comparisons. | Keep; add exact preset recommendations by divergence and a small filtering example for whole-genome vs breakpoint views. |
| MUMmer4 GitHub, https://github.com/mummer4/mummer | Tool docs | Current repo uses classic nucmer/mummerplot. | Keep as stable option; add troubleshooting for huge plant genomes. |
| RagTag paper/tomato application, Genome Biology 2022, https://genomebiology.biomedcentral.com/articles/10.1186/s13059-022-02823-7 | Research publication | Supports RagTag, and is crop-relevant. Also emphasizes personalized assemblies and reference-guided scaffolding. | Keep RagTag as comparison/review aid. Add tomato example to "good use case" list. |
| RagTag GitHub/Wiki, https://github.com/malonge/RagTag | Tool docs | Documents correct, scaffold, patch, merge. | Extend local RagTag page to mention patch/merge but keep correction conservative. |
| RagTag correct wiki, https://github.com/malonge/RagTag/wiki/correct | Tool docs | Clarifies correction breaks query sequences but does not add/subtract sequence. | Add this exact conceptual distinction to docs. |
| RagTag scaffold wiki, https://github.com/malonge/RagTag/wiki/scaffold | Tool docs | Clarifies scaffolding orders/orients and joins with gaps without changing input sequence. | Good addition to beginner explanation. |
| Bioinformatics SE manual curation question, https://bioinformatics.stackexchange.com/questions/18438/how-to-manually-curate-a-genome-assembly-for-sequence-variation-or-error | Community discussion | Useful case of confusing true structural variation with assembly error. | Add as motivation for requiring independent evidence before correction. |

### F. Hi-C Scaffolding and Contact Map Review

| Resource | Type | Why it matters | Follow-up |
| --- | --- | --- | --- |
| YaHS paper, Bioinformatics 2023, https://academic.oup.com/bioinformatics/article/39/1/btac808/6917071 | Research publication | Direct support for current YaHS scaffolding path. | Keep; add benchmark context and known limitation about rare T2T false joins. |
| YaHS GitHub, https://github.com/c-zhou/yahs | Tool docs | Important practical details: `juicer pre`, JBAT outputs, limitations, contig count limit. | Audit `docs/yahs_hic_workflow.md` against current README; add limitations section and PretextMap/Higlass outputs if useful. |
| Plant Hi-C scaffolder benchmark, PMC, https://pmc.ncbi.nlm.nih.gov/articles/PMC11604747/ | Research publication | Directly relevant to plant genomes; compares Hi-C scaffolders on assemblies from PacBio HiFi and ONT reads. | Add to scaffolding references; extract practical messages about scaffolders not strongly affecting k-mer QV/completeness but affecting structure. |
| 3D-DNA GitHub, https://github.com/aidenlab/3d-dna | Tool docs | Current alternative scaffolding/JBAT path. | Keep; verify current post-review command details. |
| Juicebox Assembly Tools wiki, https://github-wiki-see.page/m/aidenlab/Juicebox/wiki/Juicebox-Assembly-Tools | Tool docs | Practical JBAT load/save/assembly edits guidance. | Add explicit archive list for `.assembly`, `.hic`, export, and post-review FASTA/AGP. |
| Dudchenko et al. 2017 Aedes aegypti Hi-C scaffolding, https://doi.org/10.1126/science.aal3327 | Research publication | Foundational 3D-DNA/Juicebox assembly paper. | Add to key refs if not already present. |
| SALSA2, https://github.com/marbl/SALSA | Tool docs/research method | Not currently covered. Plant benchmark includes SALSA2; useful alternate comparator. | Add SALSA2 to "alternate scaffolders" matrix before deciding if a template is worth adding. |
| Biostars YaHS QV drop question, https://www.biostars.org/p/9616448/ | Community discussion | Useful live example that scaffolding can appear to change Merqury QV unexpectedly, often due to Ns, sequence naming, using the wrong input, or pipeline issues. | Add troubleshooting note: re-run Merqury on pre/post scaffolds with same read DB; inspect N handling and file identity. |
| Bioinformatics SE Dovetail/Hi-C improvement question, https://bioinformatics.stackexchange.com/questions/18377/how-to-improve-a-genome-assembly-using-dovetail-and-pacbio-assembly | Community discussion | Reinforces that Hi-C orders/orients contigs and must be visualized; it does not magically improve base quality. | Add to Hi-C contact-map QC teaching notes. |

### G. Contamination, Organelles, and Read/Assembly Taxonomy

| Resource | Type | Why it matters | Follow-up |
| --- | --- | --- | --- |
| NCBI FCS documentation, https://www.ncbi.nlm.nih.gov/datasets/docs/v2/data-processing/policies-annotation/quality/contamination/fcs-contamination/ | Official docs | Central release gate for contamination screening. | Keep current templates; add date/version/database capture fields to contamination decision log. |
| FCS-GX paper, Genome Biology 2023, https://pmc.ncbi.nlm.nih.gov/articles/PMC10246020/ | Research publication | Supports rapid contamination screening at scale and NCBI release relevance. | Add citation and short explanation of specificity/sensitivity claims. |
| BlobToolKit paper, G3 2020, https://pmc.ncbi.nlm.nih.gov/articles/PMC7144090/ | Research publication | Strongly supports GC/coverage/taxonomy/BUSCO interactive review. | Expand BlobToolKit prep docs with required files and how to interpret organelle/high-copy clusters. |
| sourmash docs/papers, https://sourmash.readthedocs.io/ | Tool docs | Current repo uses sourmash reads. Useful for preassembly sketching. | Add sketch database provenance/version capture. |
| MitoHiFi paper/tutorial, Galaxy mitochondrial HiFi tutorial, https://training.galaxyproject.org/training-material/topics/assembly/tutorials/mitochondrion-assembly/tutorial.html | Protocol/tutorial | Missing explicit organelle assembly lane. Current repo screens organelles, but does not provide a full MitoHiFi path. | Add "optional organelle assembly and separate submission" page or appendix. |
| Biostars circular scaffolds in hifiasm, https://www.biostars.org/p/9548209/ | Community discussion | Practical sign that hifiasm circular outputs may be organelles or repeats. | Add FAQ to organelle workflow: `_c`/circular sequences require BLAST/minimap/coverage review. |
| Bioinformatics SE contamination on assembly, https://bioinformatics.stackexchange.com/questions/14765/contamination-on-genome-assembly | Community discussion | Useful example of GC/coverage/BUSCO ambiguity. | Add to contamination teaching notes. |

### H. Gap Filling, T2T, Telomere, and Centromere Evidence

| Resource | Type | Why it matters | Follow-up |
| --- | --- | --- | --- |
| LR_Gapcloser paper, GigaScience 2019, https://academic.oup.com/gigascience/article/8/1/giy157/5256637 | Research publication | Supports current LR_Gapcloser option. | Keep as older but still useful; emphasize validation after fills. |
| TGS-GapCloser paper, GigaScience 2020, https://academic.oup.com/gigascience/article/9/9/giaa094/5902284 | Research publication | Supports current TGS-GapCloser/TGS-GapCloser2 family. | Confirm differences between TGS-GapCloser and TGS-GapCloser2 docs before final protocol wording. |
| Comprehensive evaluation of long-read gap filling tools, Genes 2024, https://doi.org/10.3390/genes15010127 | Review/benchmark | Supports comparing gap fillers rather than trusting one tool. | Add as headline reference for conservative gap filling page. |
| Gapless paper/tool, https://www.life-science-alliance.org/content/6/7/e202201471 | Research/tool | Already listed as option; combines scaffolding, gap filling, correction. | Add "higher-risk because correction behavior is broader" note. |
| TRFill paper, Genome Biology 2025, https://genomebiology.biomedcentral.com/articles/10.1186/s13059-025-03685-5 | Research publication | Newer method for tandem repeat gap filling using HiFi + Hi-C; current repo already has template. | Expand `trfill.sbatch` docs with use cases and required configs; add decision-log fields specific to tandem-repeat fills. |
| tidk paper, Bioinformatics 2025, https://academic.oup.com/bioinformatics/article/41/2/btaf049/7994463 | Research publication | Supports de novo and known telomere motif discovery/scanning. | Upgrade telomere page: known motif path plus de novo motif path, with plant motif caveats. |
| quarTeT paper, Horticulture Research 2023, https://pmc.ncbi.nlm.nih.gov/articles/PMC10407605/ | Research publication | Supports current TeloExplorer/CentroMiner telomere/centromere route and crop/horticultural T2T framing. | Add module-by-module notes: AssemblyMapper, GapFiller, TeloExplorer, CentroMiner, and when not to use AssemblyMapper. |
| Li and Durbin 2024 T2T-era review, Nature Reviews Genetics, https://www.nature.com/articles/s41576-024-00718-w | Review | Good broad context for near-complete/T2T assembly expectations. | Use to frame v1.0 T2T language and advanced lanes. |

### I. Repeat Annotation and Release Mask

| Resource | Type | Why it matters | Follow-up |
| --- | --- | --- | --- |
| EDTA paper, Genome Biology 2019, https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1905-y | Research publication | Direct support for EDTA in plant/eukaryotic TE annotation. | Keep as primary repeat annotation ref; add limitations and input hygiene notes. |
| EDTA GitHub, https://github.com/oushujun/EDTA | Tool docs | Important details: short/simple sequence names, CDS/curated library options, panEDTA. | Add EDTA input-name caution to repeat workflow and release ID planning. |
| EDTA commentary response, Genome Biology 2024, https://genomebiology.biomedcentral.com/articles/10.1186/s13059-023-03119-0 | Commentary | Useful nuance: EDTA was developed primarily in plant genomes; TE landscapes differ. | Add caution against assuming EDTA is universally optimal outside plants or for all TE classes. |
| RepeatModeler2 paper, PNAS 2020, https://pubmed.ncbi.nlm.nih.gov/32300014/ | Research publication | Supports alternate de novo repeat library path and LTR structural discovery improvements. | Keep comparison-only path; add when RepeatModeler2 may find useful unclassified repeats. |
| RepeatMasker docs, https://www.repeatmasker.org/ | Tool docs | Required for masking release/gene input. | Add version/library capture fields to repeat summary. |

### J. Gene Annotation, Functional Annotation, and Submission Validation

| Resource | Type | Why it matters | Follow-up |
| --- | --- | --- | --- |
| Liftoff paper, Bioinformatics 2021, https://academic.oup.com/bioinformatics/article-abstract/37/12/1639/6035128 | Research publication | Supports current close-reference gene transfer path. | Add divergence thresholds/diagnostics for when Liftoff should be comparison-only. |
| BRAKER3 paper, Genome Research 2024, https://doi.org/10.1101/gr.278090.123 | Research publication | Supports current BRAKER3 RNA-seq + protein evidence path. | Add exact evidence minimums and container recommendation. |
| MAKER paper, Genome Biology/Genome annotation pipeline, https://pmc.ncbi.nlm.nih.gov/articles/PMC2134774/ | Research publication | Supports current MAKER evidence-integration option. | Keep as mature but installation-heavy option; add "when MAKER is worth the complexity." |
| MAKER2 paper, BMC Bioinformatics 2011, https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-12-491 | Research publication | Supports updated MAKER annotation/evidence handling. | Add to key refs if missing. |
| NCBI Eukaryotic annotated genome submission guide, https://www.ncbi.nlm.nih.gov/genbank/eukaryotic_genome_submission/ | Official docs | Supports table2asn, annotation optionality, locus tag prefix, FASTA requirements. | Keep release docs current; add "annotation optional for genome submission" as explicit early decision. |
| NCBI Eukaryotic annotation guide, https://www.ncbi.nlm.nih.gov/genbank/eukaryotic_genome_submission_annotation/ | Official docs | Supports feature table/GFF validation and common discrepancy issues. | Keep table2asn discrepancy triage aligned with NCBI. |
| NCBI AGP v2.1 spec, https://www.ncbi.nlm.nih.gov/genbank/genome_agp_specification/ | Official docs | Supports AGP validation and biological gap types. | Keep AGP helper scripts; add gap type/linkage examples for Hi-C/proximity_ligation and biological gaps. |
| NCBI genome submission portal, https://submit.ncbi.nlm.nih.gov/about/genome/ | Official docs | Confirms genome submission scope and recommends FCS before submission. | Add to release checklist "check portal docs before final upload." |

### K. Protocols, Tutorials, Blogs, and Training Material

| Resource | Type | Why it matters | Follow-up |
| --- | --- | --- | --- |
| Galaxy HiFi assembly tutorial, https://training.galaxyproject.org/training-material/topics/assembly/tutorials/hifi-assembly/tutorial.html | Training protocol | Beginner-friendly comparison of hifiasm/Flye, GFA-to-FASTA, QC steps. | Mine for teaching language and beginner exercises, not for HPC commands. |
| Galaxy VGP assembly tutorial, https://training.galaxyproject.org/training-material/topics/assembly/tutorials/vgp_genome_assembly/tutorial.html | Training protocol | Strong full-workflow framing with hifiasm, genome profiling, Bionano/Hi-C/manual curation. | Use as benchmark for whether this repo's user journey is complete. |
| RCAC HiFi assembly tutorial, https://rcac-bioinformatics.github.io/tutorials/hifi_assembly/ | HPC tutorial | Provides practical hifiasm install/container/HPC framing and maize example. | Compare setup/environment page for missing container examples. |
| RCAC 2026 HiFiASM training, https://rcac-bioinformatics.github.io/genome-assembly/pacbio-hifi-assembly.html | Recent training page | Mentions newer hifiasm support for ONT, ultra-long ONT, hybrid assembly, Hi-C, parental k-mers. | Use as current training signal; verify with official hifiasm docs before adding protocol claims. |
| USDA SCINet data prep/QC event, https://scinet.usda.gov/events/2025-04-29-data | Training material | USDA-adjacent training using hifiasm on HiFi reads and QC. | Add to training/resources list; compare command style with repo sbatch templates. |
| PacBio blog on assemblers, https://www.pacb.com/blog/high-quality-hifi-assemblers/ | Blog | Helpful background on the HiFi assembler ecosystem. | Use only as background. |
| protocols.io IPA assembly for HiFi reads, https://www.protocols.io/view/ipa-assembly-for-hifi-pacbio-reads-buwfnxbn | Protocol | Plant-genome IPA protocol exists, but protocols.io may require JS. | Put on manual retrieval list if we want details beyond search snippets. |

### L. Community Threads Worth Tracking

Stack Overflow itself appears to have very little directly useful HiFi assembly content; results were mostly generic FASTA/GFF scripting. BioStars and Bioinformatics Stack Exchange are much more relevant for genome assembly practice.

Useful community threads:

| Thread | Lesson | Follow-up |
| --- | --- | --- |
| Biostars duplicated BUSCO after hifiasm, https://www.biostars.org/p/483811/ | BUSCO duplication can represent haplotypes, WGD/retained duplication, or assembly representation. | Add duplicated-BUSCO FAQ. |
| Biostars hifiasm GFA/stats, https://www.biostars.org/p/9470684/ | Beginners struggle with GFA outputs and basic stats. | Add "from GFA to FASTA to metrics" quick recipe. |
| Biostars assembly QC from BAMs, https://www.biostars.org/p/9615110/ | Users seek misassembly/repeat-collapse checks beyond QUAST/BUSCO. | Add QC decision tree. |
| Biostars Merqury QV disagreement, https://www.biostars.org/p/9616205/ | QV tools can disagree; read DB, polishing, N handling, and method definitions matter. | Add QV troubleshooting. |
| Biostars hifiasm + ONT merging, https://www.biostars.org/p/9614177/ | Merging assemblies can introduce duplicated sequence if one assembly is structurally wrong. | Add "do not merge by default" warning. |
| Biostars circular hifiasm scaffolds, https://www.biostars.org/p/9548209/ | Circular sequences may be organelles or repeats; verify. | Add organelle/circular contig FAQ. |
| Biostars scaffolding with CLR, https://www.biostars.org/p/9608760/ | Legacy CLR can scaffold but may add risk; Hi-C usually better for chromosome-scale. | Add long-read scaffolding caveat. |
| Biostars YaHS QV drop, https://www.biostars.org/p/9616448/ | Post-scaffolding QC surprises need file identity and method sanity checks. | Add YaHS/Merqury troubleshooting. |
| Bioinformatics SE HiFi assembler choice, https://bioinformatics.stackexchange.com/questions/11158/what-assembler-is-appropriate-for-high-fidelity-pacbio-reads | hifiasm/HiCanu/IPA are the core historical HiFi choices. | Use in alternate assembler matrix. |
| Bioinformatics SE polishing HiFi with Illumina, https://bioinformatics.stackexchange.com/a/21997 | Illumina polishing of HiFi assemblies is not a default best practice and can harm haplotype representation. | Add polishing FAQ. |
| Bioinformatics SE manual curation, https://bioinformatics.stackexchange.com/questions/18438/how-to-manually-curate-a-genome-assembly-for-sequence-variation-or-error | Dotplot discordance needs independent evidence to separate real SV from assembly error. | Use in curation examples. |
| Bioinformatics SE BUSCO inconsistency/contamination, https://bioinformatics.stackexchange.com/questions/17970/busco-results-apparently-inconsistent | BUSCO can be affected by contamination and lineage assumptions. | Add "BUSCO can be fooled" caveat. |

## Gap Analysis

Strongly covered:

- hifiasm as default crop HiFi assembler.
- Multi-layer QC using contiguity, BUSCO, Merqury, QUAST, read mapping, dotplots, and contamination review.
- Evidence-first structural correction.
- YaHS and 3D-DNA/JBAT as main Hi-C scaffolding paths.
- Conservative gap filling and T2T claim language.
- EDTA/RepeatModeler2 repeat annotation and Liftoff/BRAKER3/MAKER gene annotation decision logs.
- NCBI release/readiness logic.

Missing or underdeveloped:

- Alternate assembler comparison lane: HiCanu, Flye, IPA, Verkko, hifiasm-UL.
- Polishing policy: when not to polish HiFi assemblies with Illumina; when nextPolish2/Racon/HiFi-based polishing is justified.
- Explicit GFA-to-FASTA/statistics beginner recipe.
- SALSA2 and possibly Bionano/optical-map scaffolding as comparison-only options.
- MitoHiFi / organelle assembly as a companion route separate from nuclear organelle screening.
- More precise Merqury spectra-cn and QV disagreement troubleshooting.
- More explicit hifiasm cache/bin reuse, `-i`, `--write-paf`, `--write-ec`, and current parameters audit.
- More current advanced T2T lane for Verkko and hifiasm-UL, especially with ultra-long ONT.
- More examples of wrong telomere motifs, internal telomere signals, and centromere evidence conflicts.
- More source/version/database capture for NCBI FCS, BUSCO ODB, EDTA libraries, RepeatMasker libraries, BlobToolKit databases, and sourmash sketches.

## Iterative Follow-up Plan

### Iteration 1: Stabilize Current Core Docs

Goal: improve current default path without expanding scope too much.

Actions:

1. Add a beginner recipe: `hifiasm GFA -> FASTA -> seqkit stats -> BUSCO -> Merqury`.
2. Audit `docs/assembly/hifiasm_parameters.md` against current hifiasm docs for `-l0`, `--hom-cov`, `-s`, `-z`, `--primary`, cache/bin reuse, and trio/yak notes.
3. Add read-prep subsection comparing btrim, HiFiAdapterFilt, cutadapt, and FCS-adaptor.
4. Add QC FAQ for duplicated BUSCOs, Merqury QV disagreement, and "N50 is not enough."
5. Add "polishing policy" box: HiFi assemblies are not automatically polished with Illumina; justify any polishing with before/after QC.

Deliverables:

- `docs/assembly/gfa_to_fasta_and_stats.md` or a subsection in `docs/assembly/hifiasm.md`.
- Updates to `docs/assembly/prepare_reads.md`.
- Updates to `docs/qc/assembly_metrics.md`.
- New/updated `docs/qc/merqury_interpretation.md` if the page grows too large.

### Iteration 2: Alternate Assembly and Diagnostic Comparison Lane

Goal: give users a defensible way to compare assembly candidates without random tool shopping.

Actions:

1. Create `docs/assembly/alternate_assemblers.md`.
2. Include hifiasm default, HiCanu diagnostic, Flye diagnostic, IPA comparison, Verkko advanced hybrid, hifiasm-UL advanced hybrid.
3. Define required comparison outputs: total size, contig count, N50/N90, BUSCO, Merqury QV/completeness/spectra-cn, contamination, dotplots, hifiasm/assembler logs, read mapping.
4. Add a warning against unsafe assembly merging/quickmerge without independent evidence.
5. Add decision table: "When an alternate assembler beats hifiasm on one metric but loses on another."

Deliverables:

- New docs page.
- Optional `examples/assembly_candidate_decisions.tsv`.
- Optional helper script enhancement to compare multiple candidates across existing dashboard fields.

### Iteration 3: Scaffolding Comparison and Contact Map Hardening

Goal: strengthen chromosome-scale methods with current YaHS limitations and comparison methods.

Actions:

1. Audit `docs/yahs_hic_workflow.md` against current YaHS GitHub, especially `juicer pre`, JBAT `-a`, output files, and limitations.
2. Add alternate scaffolders matrix: YaHS, 3D-DNA/JBAT, SALSA2, RagTag, Bionano/optical maps where available.
3. Add post-scaffolding QC checklist: contact-map review, AGP validation, dotplot before/after, Merqury sanity check, FASTA identity check, gap summary.
4. Add troubleshooting note for apparent QV drops after scaffolding.
5. Decide whether SALSA2 deserves an sbatch template or only a comparison note.

Deliverables:

- Updates to YaHS and 3D-DNA pages.
- New or expanded scaffolding candidate comparison table.
- Possibly `01_sbatch_templates/salsa2_scaffold.sbatch` only after local command verification.

### Iteration 4: Contamination and Organelle Companion Route

Goal: clarify nuclear release vs organelle release.

Actions:

1. Expand organelle workflow with circular hifiasm contig review.
2. Add optional MitoHiFi route for assembling mitochondria from HiFi reads.
3. Add FCS version/database/date capture fields to contamination decisions.
4. Add BlobToolKit interpretation notes: GC/coverage/taxonomy clusters, organelle high-coverage behavior, low-coverage contaminant/cobiont candidates.
5. Add sourmash database provenance capture.

Deliverables:

- Updates to `docs/organelle_workflow.md`.
- Optional new `docs/organelle_assembly.md`.
- Update `examples/contamination_decisions.tsv` or add fields if needed.

### Iteration 5: Advanced T2T and Gap/Repeat Resolution Lane

Goal: separate normal chromosome-scale workflows from advanced near-T2T projects requiring extra data.

Actions:

1. Add "advanced T2T project design" page covering when HiFi-only is insufficient.
2. Compare Verkko, hifiasm-UL, TRFill, quarTeT GapFiller, and targeted gap filling.
3. Add data-requirement table: HiFi, ultra-long ONT, Hi-C, trio/parental reads, CENH3/centromere evidence, optical maps if available.
4. Expand telomere page with tidk de novo motif discovery vs known motif search.
5. Add centromere evidence conflict examples.

Deliverables:

- New `docs/t2t_advanced_methods.md` or expansion of existing v0.6 lane.
- Update `docs/telomere_summary_workflow.md`.
- Update `docs/t2t_completeness_evidence_package.md`.

### Iteration 6: Repeat and Gene Annotation Refinement

Goal: make release masks and gene sets more reproducible and less fragile.

Actions:

1. Add EDTA input naming caution and plant-centric limitations.
2. Add panEDTA/curated-library/pangenome library notes as an advanced option.
3. Add RepeatModeler2 comparison interpretation: useful unclassified repeats vs overmasking.
4. Add BRAKER3 evidence matrix and container recommendation.
5. Add Liftoff divergence and reference suitability decision rules.
6. Add table2asn issue-to-action map from NCBI docs.

Deliverables:

- Updates to repeat library and gene set decision guides.
- Maybe new annotation evidence matrix example.

### Iteration 7: Resource Index and Watchlist

Goal: make future maintenance easier.

Actions:

1. Expand `docs/key_references.md` into a method-by-method resource index.
2. Add status columns: `core`, `alternate`, `watchlist`, `needs_local_validation`.
3. Move fast-changing vendor/tool docs to `docs/pacbio_watchlist.md`.
4. Add "manual retrieval needed" list for resources that are JS-gated or PDF-only.
5. Add a quarterly/biannual review cadence for hifiasm, Verkko, YaHS, FCS, BUSCO datasets, EDTA, BRAKER3, NCBI submission docs.

Deliverables:

- Updated `docs/key_references.md`.
- Updated `docs/pacbio_watchlist.md`.
- Optional `examples/method_resource_review.tsv`.

## Manual Retrieval / PDF List

Most key papers had open HTML/PMC/Oxford/Nature/BMC pages available. Possible manual retrieval targets if we want exact protocol details or figures:

1. protocols.io IPA assembly for HiFi PacBio reads: https://www.protocols.io/view/ipa-assembly-for-hifi-pacbio-reads-buwfnxbn
2. BRAKER3 Genome Research full text if institutional access exposes more than abstract/preprint: https://doi.org/10.1101/gr.278090.123
3. hifiasm-UL/double graph Nature Methods supplementary details: https://www.nature.com/articles/s41592-024-02269-8
4. Verkko supplementary methods: https://www.nature.com/articles/s41587-023-01662-6
5. Plant Hi-C scaffolder benchmark supplementary tables: https://pmc.ncbi.nlm.nih.gov/articles/PMC11604747/

## Recommended Next Move

Start with Iteration 1 and Iteration 2. The repo already has the major protocol backbone, so the highest-value next work is to make the default path easier to defend and make alternate methods systematic rather than ad hoc.

Proposed first concrete patch set:

1. Add `docs/assembly/alternate_assemblers.md`.
2. Add a compact `docs/qc/merqury_busco_troubleshooting.md`.
3. Update `docs/key_references.md` with new sources from this pass.
4. Add a `methods_resource_review.tsv` example or template so future literature passes can be incremental.
