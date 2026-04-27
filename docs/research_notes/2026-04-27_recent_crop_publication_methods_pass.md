# Recent Crop Genome Publication Methods Pass

Date: 2026-04-27

Scope: high-profile crop plant genome and pangenome papers published roughly within
the last three years, emphasizing what leading groups actually chose for assembly,
scaffolding, validation, repeat annotation, and gene annotation.

## Bottom Line

Recent high-profile crop genome papers are converging on two method lanes.

1. Chromosome-scale pangenome lane:
   PacBio HiFi plus hifiasm for contig assembly; Hi-C/Omni-C or map/collinearity
   information for chromosome ordering; BUSCO plus plant repeat-space metrics
   such as LAI; Merqury/Inspector/QV when available; EDTA/RepeatMasker-style TE
   annotation; evidence-integrated gene annotation from RNA-seq, Iso-Seq, protein
   homology, and ab initio prediction.

2. T2T/near-T2T lane:
   HiFi alone is not usually enough for the hardest repeats. Leading T2T crop
   papers add ONT ultra-long reads, sometimes Bionano/FISH/Hi-C/genetic maps,
   plus manual or targeted closure of rDNA, satellite, centromeric, and telomeric
   regions. Verkko, hifiasm, NextDenovo/NECAT, Canu, and custom gap closing appear
   depending on genome/repeat architecture.

## Publication-Level Method Matrix

| Crop / publication | Venue / year | What they chose | Implication for this repo |
| --- | --- | --- | --- |
| Wild and cultivated rice pangenome, 145 chromosome-level assemblies | Nature, 2025 | Mostly PacBio HiFi; hifiasm v0.16.0 default for 133 HiFi accessions; ONT accessions assembled with NECAT or NextDenovo and polished with Racon/NextPolish; organelle filtering with MUMmer; chromosome scaffolding with ALLMAPS plus Hi-C validation/scaffolding using Chromap, YaHS, Juicebox; assembly evaluation with BUSCO, LAI/LTR_retriever, Inspector QV, and QUAST comparisons; TE annotation with EDTA/panEDTA and RepeatMasker. | Strong support for making `hifiasm` the primary HiFi assembler, adding `YaHS` as a first-class Hi-C option, and elevating LAI/Inspector alongside BUSCO/Merqury for plant assemblies. |
| Barley pangenome, 76 wild and domesticated genomes | Nature, 2024 | PacBio HiFi CCS reads at about 20x haploid coverage; hifiasm v0.11-r302 for contigs; conformation capture/Hi-C scaffolding through the TRITEX pipeline; manual inspection of Hi-C contact matrices for chimeric contigs and orientation errors; Merqury for completeness/consensus accuracy; Merqury + FindGSE + k-mer heterozygosity checks; transcript and homology-supported annotations with RNA-seq and Iso-Seq. | This is the cleanest support for a Triticeae/cereal path: hifiasm + Hi-C contact-map curation + Merqury + explicit heterozygosity/duplication audit. |
| Wheat pangenome, 17 chromosome-level cultivars | Nature, published 2024 / issue 2025 | The paper reports 17 chromosome-level assemblies. Genome Warehouse records under PRJCA021345 list PacBio 30x and hifiasm 0.16.1 for assemblies; the Nature article references hifiasm, Hi-C processing, BUSCO, LAI, RepeatMasker, GeneWise/PASA/AUGUSTUS-style annotation components, and NLR/subtelomere custom scripts. | Supports keeping a large-polyploid warning lane: hifiasm works, but wheat-scale projects need careful scaffolding, repeat/QC metrics, and manual/synteny review rather than treating a single assembly run as final. |
| Maize Mo17 T2T | Nature Genetics, 2023 | Deep ultra-long ONT and PacBio HiFi. ONT assembly with NextDenovo; PacBio HiFi assemblies with hifiasm and Canu; ONT assembly polished iteratively with ONT, HiFi, and Illumina using NextPolish; PacBio contigs integrated with minimap2 to close/correct gaps; manual closure of TAG repeat arrays with ultra-long ONT; 45S rDNA closure with HiFi; validation with coverage, Merqury-style k-mers, FISH, telomere checks, and repeat/rDNA copy-number checks. | Our T2T section should explicitly say: do not promise T2T from standard HiFi alone for maize-sized repeat-rich genomes; add an advanced hybrid lane for ONT ultra-long + HiFi + cytogenetic/coverage validation. |
| Cotton T2T, Zhongmian 113 | Nature Genetics, 2025 | PacBio HiFi, ONT ultra-long, Hi-C, MGI short reads, Bionano, RNA-seq, ChIP-seq and BS-seq. The main article emphasizes a T2T assembly resolving all centromeric and telomeric regions, rDNA clusters, and organelles, with Merqury and BUSCO tables in supplementary materials. | Reinforces the T2T lane as a multi-technology validation project, not just an assembler choice. We should track rDNA, centromere, telomere, organelle, and independent-evidence validation explicitly. |
| Cotton T2T, Gossypium raimondii | Nature Genetics, 2024 | ONT, PacBio HiFi, and MGI reads; near-complete/T2T assembly; deposited assembly and annotations; methods reference Verkko and VerityMap, with extensive centromere/TE/small-RNA validation. | Supports adding Verkko as a serious T2T/near-T2T option, especially when HiFi is paired with long ONT data. |
| Modern soybean NDD2 reference plus 547 resequenced accessions | Nature Genetics, 2024 | High-quality reference assembly with large-scale resequencing and SV-GWAS; methods/references include Merqury, NextPolish, Hi-C processing, minimap2, BUSCO, repeat discovery/annotation, homology/transcript annotation, and pangenome SV comparison. | Useful reminder that many crop-genome papers are judged by downstream SV and trait discovery. Our protocol should preserve assembly choices and QC artifacts needed for reliable SV calling, not just release FASTA. |
| Maize drought pangenome | Nature Genetics, 2025 | Built a maize pangenome for drought-resistance genetics; methods visible in article snippets emphasize evidence-based transcript annotation, Mikado, BRAKER2, PASA2, Iso-Seq/EST refinement, RepeatMasker, EDTA, and curated maize TE libraries. | Strong support for the annotation side of our workflow: EDTA/RepeatMasker plus RNA-seq/Iso-Seq/protein evidence and BRAKER/PASA-style refinement is what high-profile crop papers are publishing. |

## Method Choices By Category

### Assemblers

- Default HiFi crop pangenome choice: `hifiasm`.
- For ONT-heavy or T2T work: `NextDenovo`, `NECAT`, `Verkko`, `hifiasm` variants, and sometimes `Canu` appear as alternate or complementary assemblies.
- Practical repo conclusion: keep hifiasm as the primary lane, add a comparison lane for Verkko and ONT-aware approaches, and reserve heavy hybrid workflows for T2T targets.

### Scaffolding and Curation

- `YaHS` plus `Juicebox` is current in the 2025 rice Nature pangenome.
- TRITEX remains important in barley/Triticeae-style workflows.
- 3D-DNA/Juicebox and related Hi-C curation remain common in large plant genome work.
- Reference or map-based ordering is common in pangenome papers where cross-accession comparability matters.

### QC Metrics

- BUSCO remains universal but insufficient alone.
- LAI/LTR_retriever is prominent in plant pangenome publications.
- Merqury is repeatedly used for reference-free QV/completeness, especially HiFi/T2T work.
- Inspector/QUAST appear in the rice pangenome as complementary checks.
- Contact-map review, telomere counts, centromere repeat scans, read-depth uniformity, and rDNA/satellite copy-number validation are used when the assembly claims go beyond chromosome-scale.

### Repeats and Genes

- EDTA plus RepeatMasker is the dominant repeat-annotation pattern in recent crop pangenome work.
- Pan-genome TE libraries are becoming important, not just one-off per-sample repeat libraries.
- Gene annotation is evidence-integrated: RNA-seq, Iso-Seq, protein homology, ab initio callers, PASA/EVM/Mikado/BRAKER-family tools depending on group.

## Recommended Protocol Consequences

1. Promote `hifiasm` from "one supported assembler" to "primary published-method default" for PacBio HiFi crop genomes.
2. Add a separate "T2T escalation lane" requiring ONT ultra-long or equivalent long-range evidence, plus explicit centromere/telomere/rDNA validation.
3. Make `YaHS + Juicebox` a first-class current Hi-C path alongside existing 3D-DNA/JBAT and TRITEX-style notes.
4. Elevate LAI/LTR_retriever and Inspector in the plant assembly QC checklist; keep BUSCO and Merqury.
5. Add a pangenome-comparability decision point: preserve de novo assembly truth, but allow reference/map-guided orientation when the project goal is population-scale pangenome comparison.
6. Strengthen repeat annotation guidance around EDTA, panEDTA-style combined libraries, and RepeatMasker.
7. For annotation, frame Liftoff as useful for transfer/comparison, but use BRAKER/PASA/EVM/Mikado-style evidence integration for a publication-grade gene set.

## Sources

- Rice pangenome: https://www.nature.com/articles/s41586-025-08883-6
- Barley pangenome: https://www.nature.com/articles/s41586-024-08187-1
- Wheat pangenome: https://www.nature.com/articles/s41586-024-08277-0
- Wheat Genome Warehouse example record under PRJCA021345: https://ngdc.cncb.ac.cn/gwh/Assembly/83483/show
- Maize Mo17 T2T: https://www.nature.com/articles/s41588-023-01419-6
- Cotton Zhongmian 113 T2T: https://www.nature.com/articles/s41588-025-02130-4
- Cotton G. raimondii T2T: https://www.nature.com/articles/s41588-024-01877-6
- Soybean NDD2 reference/SV paper: https://www.nature.com/articles/s41588-024-01901-9
- Maize drought pangenome: https://www.nature.com/articles/s41588-025-02378-w
- Plant pangenomes review: https://www.nature.com/articles/s41576-024-00691-4
