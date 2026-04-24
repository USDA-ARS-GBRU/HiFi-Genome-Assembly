# NCBI Submission Path

NCBI submission is a validation workflow, not just a file upload. Freeze the assembly, validate the release files, prepare accessions, and submit annotation only after the assembly sequence names are stable.

For new users, the biggest conceptual shift is this: do not wait until the end to think about submission. Good release packages are usually the result of decisions that were made consistently during QC, curation, naming, and annotation.

## Assembly Submission Inputs

Prepare:

- final genome FASTA
- AGP, if chromosome/scaffold objects are built from components
- FASTA header audit
- FASTA validation output
- FCS-adaptor and FCS-GX results
- contamination decision log
- BioProject accession
- BioSample accession
- SRA accessions or read submission plan
- assembly methods text
- release manifest

## Recommended Order

1. Freeze the release FASTA.
2. Run FCS-adaptor and FCS-GX.
3. Resolve contamination, organelle, adapter, and vector decisions.
4. Validate FASTA, headers, AGP, and release manifest locally.
5. Prepare BioProject, BioSample, and SRA records.
6. Submit the assembly package.
7. Submit annotation only after the assembly accession and sequence names are stable.

If the annotation still has active discrepancy cleanup, it is often better to release the assembly first and hold annotation for a second pass than to force a combined release that is not yet coherent.

## Local Checks

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

scripts/check_release_bundle.py \
  --fasta 15_release/sample.genome.fa \
  --agp 15_release/sample.agp \
  --manifest examples/release_manifest.tsv \
  --out-dir 15_release/validation
```

## Annotation Handoff

If submitting annotation, validate with `table2asn` and review the `.val` and discrepancy outputs.

```bash
sbatch \
  --export fasta=15_release/sample.genome.fa,gff=15_release/sample.annotation.gff3,template=00_metadata/template.sbt,sample=sample \
  01_sbatch/table2asn_validate.sbatch
```

Common issues:

- invalid product names
- missing locus tags
- genes crossing gaps
- features on missing sequence IDs
- inconsistent IDs between FASTA, AGP, and GFF3
- internal stop codons
- repeat-derived gene models that need filtering or naming review

Treat these reports as a triage queue, not as a moral judgment on the annotation. Fix coordinate and ID mismatches first, then feature-logic problems, then naming and product cleanup.

## Accession Tracking

Track accessions in a single table:

```text
examples/accession_tracking.tsv
```

Connect BioProject, BioSample, SRA, Assembly, and Annotation records so future users can trace the release.

For package-selection logic and annotation freeze notes, also see:

- `../release_package_decision_guide.md`
- `../annotation_submission_handoff.md`

## Files to Archive

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

## Release Rule

Do not submit until sequence names, FASTA content, AGP, contamination decisions, annotation coordinates, and metadata all describe the same frozen assembly version.

## Read Next

After this page, continue with:

- `../release_package_decision_guide.md`
- `../release_bundle_worked_example.md`
- `../table2asn_discrepancy_triage.md`
