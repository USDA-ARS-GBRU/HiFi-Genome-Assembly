# NCBI Submission and Annotation Validation

NCBI submission is a validation workflow, not just a file upload. Run these checks before submitting a crop plant assembly or annotation package.

## Assembly-Only Submission

Required evidence:

- final FASTA
- FASTA header audit
- FASTA sequence validation
- contamination review, including FCS-adaptor and FCS-GX
- BioProject and BioSample metadata
- SRA accessions or read submission plan
- AGP if the assembly contains scaffold/chromosome objects built from components

Recommended release order:

1. Freeze the assembly FASTA and do not rename sequences again unless a validation error requires it.
2. Run contamination screens and decide whether each flagged sequence should be kept, removed, masked, split, or submitted separately.
3. Run local FASTA/header/manifest checks.
4. Prepare BioProject, BioSample, and SRA records.
5. Submit the assembly package.
6. Submit annotation only after the assembly accession and sequence names are stable.

Recommended local checks:

```bash
scripts/validate_fasta.py \
  15_release/sample.genome.fa \
  --min-length 200 \
  -o 15_release/validation/fasta_validation.tsv

scripts/audit_fasta_headers.py \
  15_release/sample.genome.fa \
  -o 15_release/validation/fasta_header_audit.tsv

scripts/audit_release_manifest.py \
  examples/release_manifest.tsv \
  -o 15_release/validation/manifest_audit.tsv
```

## Annotation Submission

If submitting gene annotation to GenBank, validate with `table2asn` and review the `.val` and discrepancy outputs.

```bash
sbatch \
  --export fasta=15_release/sample.genome.fa,gff=15_release/sample.annotation.gff3,template=00_metadata/template.sbt,sample=sample \
  01_sbatch/table2asn_validate.sbatch
```

Review:

- internal stop codons
- invalid product names
- missing locus tags
- genes crossing gaps
- features on missing sequence IDs
- inconsistent IDs between FASTA, AGP, and GFF3
- partial features not marked correctly
- pseudogene and transposable-element-derived gene calls

For crop plant submissions, treat the validation reports as a curation queue. Fix structural problems first, then product names and locus tags, then warning categories that reflect biological edge cases such as pseudogenes, partial genes near scaffold ends, or repeat-derived gene models.

Do not use annotation coordinates from an older FASTA after scaffold renaming, masking changes, contaminant removal, or sequence splitting. Regenerate or lift the GFF3 and rerun table2asn after any final FASTA change.

## Metadata Checklist

Prepare:

- organism name and taxonomy ID
- cultivar/accession/isolate
- BioProject accession
- BioSample accession
- sequencing platform and library strategy
- assembly method and version
- annotation method and version, if annotation is submitted
- submitter template (`.sbt`) for table2asn
- evidence data accessions or file provenance for RNA-seq/protein evidence
- repeat masking method and library provenance if a soft-masked genome was used for annotation

For package-selection logic and annotation freeze notes, also see:

- `docs/release_package_decision_guide.md`
- `docs/annotation_submission_handoff.md`

## Files to Archive Beside the Submission

Keep these files even when they are not all uploaded to NCBI:

```text
15_release/validation/fasta_header_audit.tsv
15_release/validation/fasta_validation.tsv
15_release/validation/manifest_audit.tsv
15_release/ncbi_validation/sample/*.val
15_release/ncbi_validation/sample/*.dr
15_release/sample.assembly_methods.md
15_release/sample.contamination_decisions.tsv
15_release/sample.id_map.tsv
```

## Rule of Thumb

Do not submit until every table2asn error is fixed or understood. Warnings may be acceptable, but release notes should document any warning category that affects interpretation.
