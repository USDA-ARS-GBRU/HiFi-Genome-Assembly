# Release Internal Handoff Example

This worked example shows what a practical internal handoff can look like when one lab member finishes assembly and annotation packaging and another person is responsible for the final NCBI submission.

## Scenario

The assembler has frozen:

- final nuclear assembly FASTA
- AGP for chromosome-scale scaffolds
- annotation GFF3 and sequence files
- release manifest
- Genome-Assembly-Data structured comment file
- accession-tracking sheet

The submitter did not generate the assembly and needs a short, trustworthy packet that explains what is final, what is comparison-only, and what should never be uploaded.

## Suggested Handoff Folder

```text
release_handoff/
  README.submitter_notes.md
  final/
    sample.primary.fasta.gz
    sample.primary.agp
    sample.annotation.gff3.gz
    sample.proteins.fa.gz
    sample.transcripts.fa.gz
    submission.manifest.tsv
    Genome-Assembly-Data.cmt
  qc/
    assembly_metrics.tsv
    contamination_summary.tsv
    annotation_summary.tsv
    table2asn_discrepancy_summary.tsv
  tracking/
    accession_tracking.tsv
    identifier_crosswalk.tsv
  comparison_only/
    rejected_annotation_candidates.tsv
    alternate_repeat_mask_summary.tsv
```

## Submitter Notes Example

Recommended `README.submitter_notes.md` content:

```text
Release object: combined nuclear assembly plus annotation
Assembly version: cultivarX_v1.2
Annotation version: cultivarX_v1.2.genesetA
Files in final/ are the only files intended for submission.
Files in comparison_only/ are included for internal provenance and should not be uploaded.
Annotation sequence IDs already match the final FASTA.
Structured comments and manifest rows were checked against the final bundle on 2026-04-24.
Outstanding discrepancy status: no blocker-level discrepancies remain; see qc/table2asn_discrepancy_summary.tsv.
```

## What Makes a Good Handoff

A good internal handoff should let the submitter answer these questions without calling the assembler:

- What exactly is the release object?
- Which files are final?
- Which files are only supporting context?
- Do annotation IDs and FASTA IDs already match?
- Are there known discrepancy warnings?
- Is there a crosswalk for IDs and accessions?

## Minimum Internal Checklist

Before handoff, confirm:

- one folder is clearly marked as final
- one short notes file explains the release object
- comparison-only files are separated from release files
- audit outputs exist for the manifest and bundle
- accession and identifier tracking tables are present

## Handoff Language

```text
The release handoff package contains one frozen submission-ready bundle and a separate comparison-only record for provenance. Final FASTA, AGP, annotation, manifest, and structured-comment files have already been aligned by sequence identifiers and reviewed through internal audit helpers. Supporting summaries are included for submitter confidence but are not part of the upload set unless explicitly noted.
```
