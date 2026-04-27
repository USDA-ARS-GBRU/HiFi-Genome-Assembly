# Key References and Tool Links

This page collects the major tool and reference links used throughout the protocol. Topic-specific docs remain the best place for step-level interpretation and parameter logic.

## Recent Crop Genome Method Anchors

These papers are useful for seeing what high-profile crop genome groups are actually choosing.

| Crop/project | Why it matters |
| --- | --- |
| Rice wild-cultivated pangenome, Nature 2025: https://www.nature.com/articles/s41586-025-08883-6 | PacBio HiFi, hifiasm, Hi-C/YaHS/Juicebox validation, BUSCO, LAI, Inspector, EDTA/panEDTA, RepeatMasker |
| Barley pangenome, Nature 2024: https://www.nature.com/articles/s41586-024-08187-1 | PacBio HiFi, hifiasm, TRITEX/Hi-C scaffolding, manual contact-map review, Merqury, heterozygosity checks, RNA/Iso-Seq-supported annotation |
| Wheat pangenome, Nature 2024/2025: https://www.nature.com/articles/s41586-024-08277-0 | chromosome-level wheat assemblies with hifiasm-supported method stack and large-polyploid review burden |
| Wheat GWH assembly record example: https://ngdc.cncb.ac.cn/gwh/Assembly/83483/show | public database record showing PacBio coverage and hifiasm assembly method for PRJCA021345 assemblies |
| Maize Mo17 T2T, Nature Genetics 2023: https://www.nature.com/articles/s41588-023-01419-6 | ultra-long ONT plus HiFi, NextDenovo, hifiasm, Canu, polishing, targeted repeat/rDNA closure, FISH/read validation |
| Cotton T2T Zhongmian 113, Nature Genetics 2025: https://www.nature.com/articles/s41588-025-02130-4 | multi-technology T2T crop assembly with HiFi, ONT ultra-long, Hi-C, Bionano, and repeat/centromere validation |
| Cotton G. raimondii T2T, Nature Genetics 2024: https://www.nature.com/articles/s41588-024-01877-6 | near-complete/T2T cotton assembly with ONT, HiFi, MGI reads, and Verkko-related method context |
| Soybean NDD2, Nature Genetics 2024: https://www.nature.com/articles/s41588-024-01901-9 | high-quality reference plus SV/trait discovery, highlighting downstream SV requirements |
| Maize drought pangenome, Nature Genetics 2025: https://www.nature.com/articles/s41588-025-02378-w | pangenome and annotation methods including EDTA/RepeatMasker, BRAKER2, PASA2, Mikado, Iso-Seq/EST refinement |
| Plant pangenomes review, Nature Reviews Genetics 2024: https://www.nature.com/articles/s41576-024-00691-4 | broad crop pangenome context and why long-read pangenomes matter for breeding |

## Assembly

- hifiasm documentation: https://hifiasm.readthedocs.io/
- hifiasm paper: https://www.nature.com/articles/s41592-020-01056-5
- hifiasm GitHub: https://github.com/chhylp123/hifiasm
- HiCanu paper: https://genome.cshlp.org/content/30/9/1291
- Flye paper/tool: https://github.com/fenderglass/Flye
- PacBio IPA/pbipa: https://github.com/PacificBiosciences/pbipa
- Verkko paper: https://www.nature.com/articles/s41587-023-01662-6
- Verkko GitHub: https://github.com/marbl/verkko
- hifiasm-UL/double graph paper: https://www.nature.com/articles/s41592-024-02269-8
- NCBI AGP Specification v2.1: https://www.ncbi.nlm.nih.gov/genbank/genome_agp_specification/
- NCBI AGP validation: https://www.ncbi.nlm.nih.gov/assembly/agp/
- Pacific Biosciences GitHub organization: https://github.com/PacificBiosciences
- PacBio pbtk: https://github.com/PacificBiosciences/pbtk
- PacBio pbmm2: https://github.com/PacificBiosciences/pbmm2

## Genome Profiling and Quality

- GenomeScope 2.0 and Smudgeplot: https://www.nature.com/articles/s41467-020-14998-3
- USDA-ARS-GBRU StandardizedHeterozygosityEvaluation: https://github.com/USDA-ARS-GBRU/StandardizedHeterozygosityEvaluation
- Merqury paper: https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02134-9
- BUSCO user guide: https://busco.ezlab.org/busco_userguide
- Inspector paper: https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02527-4
- LAI/LTR_retriever paper: https://academic.oup.com/nar/article/46/21/e126/5078385

## Scaffolding and Structural Review

- YaHS paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC9848053/
- YaHS GitHub: https://github.com/c-zhou/yahs
- Plant Hi-C scaffolding benchmark: https://pmc.ncbi.nlm.nih.gov/articles/PMC11604747/
- 3D-DNA GitHub: https://github.com/aidenlab/3d-dna
- Juicebox GitHub: https://github.com/aidenlab/Juicebox
- Juicebox Assembly Tools documentation: https://github.com/aidenlab/Juicebox/wiki/Juicebox-Assembly-Tools
- SALSA2 GitHub: https://github.com/marbl/SALSA
- TRITEX paper: https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1899-5
- RagTag GitHub: https://github.com/malonge/RagTag
- MUMmer4 GitHub: https://github.com/mummer4/mummer
- minimap2: https://github.com/lh3/minimap2
- Pteranodon: https://github.com/w-korani/Pteranodon
- Breakwright: https://github.com/rotheconrad/Breakwright

## Gap Filling

- Long-read gap-filling evaluation: https://pubmed.ncbi.nlm.nih.gov/38275608/
- LR_Gapcloser paper: https://academic.oup.com/gigascience/article/8/1/giy157/5256637
- LR_Gapcloser GitHub: https://github.com/CAFS-bioinformatics/LR_Gapcloser
- TGS-GapCloser paper: https://academic.oup.com/gigascience/article/9/9/giaa094/5902284
- TGS-GapCloser2 GitHub: https://github.com/BGI-Qingdao/TGS-GapCloser2
- Gapless paper/tool: https://www.life-science-alliance.org/content/6/7/e202201471
- Gapless GitHub: https://github.com/schmeing/gapless
- TRFill paper: https://pubmed.ncbi.nlm.nih.gov/40721805/
- TRFill GitHub: https://github.com/panlab-bioinfo/TRFill

## Telomeres and Centromeres

- tidk paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11814493/
- tidk GitHub: https://github.com/tolkit/telomeric-identifier
- quarTeT paper: https://pubmed.ncbi.nlm.nih.gov/37560017/
- quarTeT GitHub: https://github.com/aaranyue/quarTeT

## Contamination

- NCBI FCS documentation: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/data-processing/policies-annotation/quality/contamination/fcs-contamination/
- NCBI FCS GitHub: https://github.com/ncbi/fcs
- FCS-GX paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC10246020/
- VecScreen/UniVec: https://www.ncbi.nlm.nih.gov/tools/vecscreen/
- btrim paper: https://doi.org/10.1016/j.ygeno.2011.05.009
- HiFiAdapterFilt paper: https://doi.org/10.1186/s12864-022-08375-1
- HiFiAdapterFilt GitHub: https://github.com/sheinasim/HiFiAdapterFilt
- BlobToolKit paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC7144090/
- sourmash docs: https://sourmash.readthedocs.io/
- MitoHiFi paper/tutorial context: https://training.galaxyproject.org/training-material/topics/assembly/tutorials/mitochondrion-assembly/tutorial.html

## Repeat Annotation

- EDTA paper: https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1905-y
- EDTA GitHub: https://github.com/oushujun/EDTA
- RepeatModeler2 paper: https://pubmed.ncbi.nlm.nih.gov/32300014/
- RepeatMasker: https://www.repeatmasker.org/
- LTR_retriever: https://github.com/oushujun/LTR_retriever

## Gene Annotation

- BRAKER: https://github.com/Gaius-Augustus/BRAKER
- BRAKER3 paper: https://genome.cshlp.org/content/34/5/769
- MAKER paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC2134774/
- MAKER2 paper: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-12-491
- Liftoff: https://github.com/agshumate/Liftoff
- Liftoff paper: https://academic.oup.com/bioinformatics/article/37/12/1639/6035128

## NCBI Submission

- Genome submission portal: https://submit.ncbi.nlm.nih.gov/about/genome/
- Eukaryotic genome submission guide: https://www.ncbi.nlm.nih.gov/genbank/eukaryotic_genome_submission/
- Eukaryotic annotation guide: https://www.ncbi.nlm.nih.gov/genbank/eukaryotic_genome_submission_annotation/
- Submitting eukaryotic genome data: https://www.ncbi.nlm.nih.gov/genbank/eukaryotic_submission/
- Structured comments: https://www.ncbi.nlm.nih.gov/genbank/structuredcomment/

## Community Databases

- MaizeGDB genome center: https://www.maizegdb.org/genome
- SoyBase genome information: https://www.soybase.org/resources/genome_info/
- SoyBase genome nomenclature: https://www.soybase.org/about/genome_nomenclature/
- Gramene update: https://pubmed.ncbi.nlm.nih.gov/41335101/
