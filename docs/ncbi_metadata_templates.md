# NCBI Metadata Templates

Use this guide before creating BioProject, BioSample, SRA, genome assembly, and annotation submissions. NCBI forms change over time, so treat these as working templates rather than a replacement for the current portal.

## Submission Order

Recommended order for crop genome projects:

1. Create or identify the BioProject.
2. Create the BioSample for the exact biological material used for sequencing.
3. Submit raw reads to SRA, including PacBio HiFi and any Hi-C, Illumina, RNA-seq, or Iso-Seq evidence intended for public reuse.
4. Submit the unannotated genome assembly or the annotated `.sqn` package.
5. Submit or link annotation evidence and community database records.

For annotated genome submissions, NCBI notes that BioProject and BioSample may need to exist before the annotated genome is submitted.

## BioProject Working Template

```text
project_title:
public_description:
organism:
taxon_id:
project_data_type: Genome sequencing and assembly
sample_scope: Monoisolate or multiisolate
relevance: Agricultural, breeding, comparative genomics, or functional genomics
submitter_group:
release_plan:
linked_publications:
```

Write the BioProject description at the study level. Do not bury cultivar-specific details here if multiple cultivars or accessions will share the same project.

## BioSample Working Template

```text
sample_name:
organism:
taxon_id:
cultivar:
isolate_or_accession:
breed:
bioproject:
geographic_origin:
collection_date:
tissue:
developmental_stage:
sex:
ploidy:
estimated_genome_size:
material_source:
voucher_or_germplasm_id:
collector:
identifier_authority:
```

For crop plants, the BioSample should make the biological source reusable. Include cultivar, accession, germplasm, or breeding-line identifiers when they are public and appropriate.

## SRA Working Template

```text
library_id:
title:
bioproject:
biosample:
platform: PacBio Sequel II, PacBio Revio, Illumina, or other
instrument_model:
library_strategy: WGS, Hi-C, RNA-Seq, Iso-Seq
library_source: GENOMIC, TRANSCRIPTOMIC, or METAGENOMIC
library_selection:
library_layout:
filetype:
filename:
estimated_insert_size:
read_processing_notes:
```

SRA metadata describes the sequencing experiment and run files. Use clear experiment titles because they appear in public records.

## Genome Assembly Working Template

```text
assembly_name:
assembly_type: haploid, diploid, haplotype, alternate-pseudohaplotype, or other project-specific term
organism:
taxon_id:
biosample:
bioproject:
sra_accessions:
sequencing_technology:
genome_coverage:
assembly_method:
assembly_method_version:
polishing_method:
scaffolding_method:
contamination_screening:
assembly_level:
genome_representation:
expected_genome_size:
release_fasta:
agp_file:
```

NCBI genome submission metadata asks for assembly method, method version or date, genome coverage, sequencing technologies, whether the genome is full or partial, and any reference genome used for non-de-novo assembly.

## Annotation Working Template

```text
annotation_name:
assembly_accession:
annotation_method:
annotation_method_version:
repeat_masking_method:
repeat_library:
evidence_rna_seq:
evidence_iso_seq:
evidence_proteins:
locus_tag_prefix:
gff3_file:
table2asn_template:
sqn_file:
validation_report:
discrepancy_report:
```

For NCBI annotation submission from GFF3, validate with table2asn and review both validation and discrepancy reports. Keep the exact FASTA, GFF3, `.sbt`, `.sqn`, `.val`, and discrepancy outputs together.

## Local Tracking Table

Maintain a small TSV during the project:

```text
object	local_name	accession	status	release_date	notes
BioProject	sample_project	PRJNA_pending	draft		not submitted
BioSample	sample_biosample	SAMN_pending	draft		not submitted
SRA	PacBio_HiFi_reads	SRR_pending	draft		not submitted
Assembly	sample_v1	GCA_pending	draft		awaiting FCS review
Annotation	sample_v1_annotation	pending	draft		awaiting table2asn
```

## Sources to Check

- NCBI Genome submission portal guidance: https://submit.ncbi.nlm.nih.gov/about/genome/
- NCBI BioProject and BioSample submission guidance: https://submit.ncbi.nlm.nih.gov/about/bioproject-biosample/
- NCBI SRA submission overview: https://submit.ncbi.nlm.nih.gov/about/sra/
- NCBI SRA metadata guidance: https://www.ncbi.nlm.nih.gov/sra/docs/submitmeta
- NCBI GFF3 annotation submission guidance: https://www.ncbi.nlm.nih.gov/genbank/genomes_gff/
- NCBI FCS documentation: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/data-processing/policies-annotation/quality/contamination/fcs-contamination/
- NCBI FCS GitHub repository: https://github.com/ncbi/fcs
