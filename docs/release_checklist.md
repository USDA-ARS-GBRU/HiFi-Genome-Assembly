# Public Release Checklist

Use this checklist before submitting a crop plant genome assembly to NCBI/INSDC or a community database.

## Repository and Reproducibility

- [ ] Assembly workflow commit recorded.
- [ ] Tool versions recorded.
- [ ] HPC job logs retained.
- [ ] Manual edits documented with sequence IDs, coordinates, evidence, and rationale.
- [ ] Final files listed in a release manifest.

## Assembly Files

- [ ] Final FASTA is compressed with `gzip`.
- [ ] FASTA index generated with `samtools faidx`.
- [ ] Sequence IDs are stable, unique, and NCBI-safe.
- [ ] Sequences shorter than 200 bp removed or justified.
- [ ] No random concatenation of unrelated sequences.
- [ ] Chromosome, scaffold, and unplaced naming conventions are documented.
- [ ] AGP produced and validated if scaffolds/chromosomes are built from components.

## Quality Evidence

- [ ] seqkit and/or BBTools stats complete.
- [ ] BUSCO genome assessment complete with appropriate lineage.
- [ ] Merqury QV/completeness complete.
- [ ] Whole-genome dotplots reviewed.
- [ ] Hi-C contact map reviewed if Hi-C scaffolding was used.
- [ ] Read mapping coverage reviewed.
- [ ] Haplotig duplication or polyploid structure assessed.

## Contamination and Organelles

- [ ] FCS-adaptor complete.
- [ ] FCS-GX complete.
- [ ] BlobToolKit or equivalent GC/coverage/taxonomy review complete.
- [ ] Chloroplast contigs identified.
- [ ] Mitochondrial contigs identified.
- [ ] Any removed or retained suspect contigs documented.

## Telomeres, Centromeres, and Gaps

- [ ] Telomere motif confirmed or discovered.
- [ ] Terminal telomere signals summarized.
- [ ] Internal telomere signals reviewed.
- [ ] Putative centromere evidence summarized.
- [ ] Gap counts and gap types summarized.

## Repeat and Gene Annotation

- [ ] Repeat library generated or selected.
- [ ] Soft-masked genome generated for gene annotation.
- [ ] Repeat GFF/BED tracks generated.
- [ ] Gene annotation produced, if part of release.
- [ ] Protein and transcript FASTA files generated, if annotated.
- [ ] Annotation BUSCO complete.
- [ ] Internal stop codons and invalid products reviewed.
- [ ] Functional annotation summarized.

## NCBI/INSDC Submission

- [ ] BioProject created.
- [ ] BioSample created with correct organism, cultivar/accession, tissue, and isolation source metadata.
- [ ] SRA reads submitted or prepared.
- [ ] Genome submission package prepared.
- [ ] Annotation package prepared with table2asn, if submitting annotation.
- [ ] Validation and discrepancy reports reviewed.
- [ ] Submitter contact and release date confirmed.

## Manuscript and Community Release

- [ ] Methods section includes data types, coverage, assembler version, parameters, QC tools, and release accessions.
- [ ] Assembly statistics table prepared.
- [ ] BUSCO/Merqury/contamination results prepared.
- [ ] Browser tracks prepared for community databases, if applicable.
- [ ] DOI or archive prepared for supplementary files not hosted by NCBI.
