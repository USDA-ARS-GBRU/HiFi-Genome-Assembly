# Methods Text Template

Use this template as the starting point for a manuscript, technical report, or NCBI structured methods description. Replace bracketed text with project-specific values and remove statements that do not apply.

## Genome Sequencing

High-molecular-weight DNA was extracted from [tissue] of [cultivar/accession, species]. PacBio HiFi sequencing was performed using [instrument/chemistry] to generate [number] reads totaling [yield] Gb. The expected haploid genome size was [size] based on [flow cytometry/k-mer estimate/literature/reference].

If Hi-C was used:

Hi-C libraries were prepared from [tissue] of the same genotype using [protocol/provider] and sequenced as paired-end reads, generating [yield] read pairs.

## Read Quality Control and Genome Profiling

PacBio HiFi read statistics were summarized with [seqkit version/tool version]. Adapter and vector contamination were evaluated with [tool/version]. K-mer spectra were generated with [meryl/jellyfish version] using k=[k] and interpreted with [GenomeScope/Smudgeplot version]. Estimated genome size, heterozygosity, and repeat content were recorded before assembly.

## Genome Assembly

HiFi reads were assembled with hifiasm [version] using [default parameters/list non-default parameters]. For HiFi-only assembly, the command was:

```bash
hifiasm [parameters] -o [prefix] [reads]
```

For Hi-C integrated phasing, Hi-C read pairs were provided using `--h1` and `--h2`. hifiasm GFA outputs were converted to FASTA from segment records. The [primary/haplotype/scaffolded] assembly was selected for downstream analysis based on contiguity, completeness, base accuracy, duplication, and structural review.

If alternate assemblers were compared:

Additional assembly candidates were generated with [HiCanu/Flye/IPA/Verkko/other version] as diagnostic comparisons. Candidates were evaluated with the same QC package and were not merged unless a targeted correction had independent read and structural support.

## Scaffolding and Structural Curation

If Hi-C scaffolding was used:

Hi-C reads were aligned to the assembly with [BWA/minimap2 version], and scaffolding was performed with [YaHS/3D-DNA/SALSA2 version]. Contact maps were reviewed with [Juicebox/JBAT/other]. Candidate misjoins were evaluated using Hi-C signal, whole-genome alignments, and HiFi read support.

If reference-guided scaffolding was used:

Reference-guided scaffolding was performed with [RagTag version] using [reference accession]. Structural differences from the reference were not automatically corrected; candidate changes were accepted only when supported by independent evidence.

## Assembly Quality Assessment

Assembly contiguity was summarized with [seqkit/BBTools/QUAST versions]. Gene-space completeness was evaluated with BUSCO [version] using [lineage dataset]. Base-level quality and k-mer completeness were estimated with Merqury [version] using read k-mers. Plant repeat-space quality was evaluated with [LAI/LTR_retriever/other, if used]. Whole-genome collinearity was inspected using [MUMmer/minimap2/plotsr versions]. HiFi reads were mapped back to the assembly with minimap2 [version] to evaluate coverage and breakpoint support.

## Contamination Screening

Assembly contamination was evaluated with NCBI FCS-adaptor and FCS-GX [versions/database dates], and [BlobToolKit/sourmash/Kraken2/other] was used to review GC, coverage, and taxonomic signals. Organelle-derived contigs were identified by [BLAST/minimap/sourmash/reference mapping] against chloroplast and mitochondrial references and were [removed/retained/submitted separately] according to the release plan.

## Telomere, Centromere, and Gap Annotation

Telomeric repeats were identified using [tidk/quarTeT/seqkit] with motif [motif or de novo result]. Putative centromeric regions were annotated using [quarTeT/Tandem Repeat Finder/repeat enrichment/Hi-C/CENH3 ChIP-seq]. Gap counts and gap lengths were summarized from the final FASTA/AGP files.

If near-T2T or T2T claims were made:

Candidate T2T chromosomes were classified using a per-chromosome evidence table including FASTA gap status, terminal and internal telomere signals, centromere candidates, difficult-repeat review, read-spanning evidence, Hi-C/contact-map support, and contamination review. The assembly was described as [chromosome-scale/near-gapless/candidate T2T/T2T-quality] according to the weakest unresolved evidence category.

## Repeat Annotation

Repeats were annotated using [EDTA/RepeatModeler2/RepeatMasker versions]. A de novo or curated repeat library was generated from the final assembly or project-wide pangenome set, classified, and used to soft-mask the genome for gene annotation. Repeat summaries were reported as the percentage of assembly sequence assigned to major repeat classes.

## Gene Annotation

Gene annotation was performed using [BRAKER3/MAKER/Liftoff/Helixer/other] with evidence from [RNA-seq/Iso-Seq/proteins/liftover reference]. Predicted proteins were functionally annotated with [InterProScan/eggNOG-mapper/DIAMOND/other]. Annotation quality was evaluated with BUSCO in protein mode using [lineage dataset] and by screening for internal stop codons, short/fragmented genes, and transposable-element-derived overprediction.

## Data Availability

Raw sequencing reads were deposited in the NCBI SRA under [accession]. The genome assembly was deposited in GenBank under [accession] and associated with BioProject [accession] and BioSample [accession]. Annotation files, repeat libraries, quality reports, and auxiliary tracks are available at [repository/DOI/community database].
