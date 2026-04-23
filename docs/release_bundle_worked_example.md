# Release Bundle Worked Example

This page walks through a small release bundle using the toy files in:

```text
examples/release_bundle/
```

The goal is to show what a release package looks like when all the parts are gathered in one place.

## Bundle Inventory

The manifest for this toy bundle is:

```text
examples/release_manifest.tsv
```

It points to these example files:

- `sample.genome.fa`
- `sample.genome.fa.fai`
- `sample.agp`
- `sample.annotation.gff3`
- `sample.proteins.fa`
- `sample.transcripts.fa`
- `sample.repeats.gff3`
- `sample.repeat_library.fa`
- `sample.assembly_qc_dashboard.tsv`
- `sample.qc_report.md`
- `sample.contamination_reports/README.md`
- `sample.methods.md`

This toy bundle is meant to teach structure, not to represent a real submission.

## What Each File Does

### Assembly files

- `sample.genome.fa`: frozen release FASTA
- `sample.genome.fa.fai`: FASTA index for local validation and browsing
- `sample.agp`: contig-to-scaffold or contig-to-chromosome map

### Annotation files

- `sample.annotation.gff3`: structural feature annotation
- `sample.proteins.fa`: translated proteins from the chosen gene set
- `sample.transcripts.fa`: transcript sequences from the chosen gene set

### Repeat files

- `sample.repeats.gff3`: repeat coordinates
- `sample.repeat_library.fa`: project repeat library used for masking or reporting

### QC and documentation files

- `sample.assembly_qc_dashboard.tsv`: compact metrics dashboard
- `sample.qc_report.md`: human-readable QC interpretation
- `sample.contamination_reports/README.md`: placeholder for contamination evidence
- `sample.methods.md`: release-facing methods and tool versions

## Run The Bundle Check

Use the helper:

```bash
scripts/check_release_bundle.py \
  --fasta examples/release_bundle/sample.genome.fa \
  --agp examples/release_bundle/sample.agp \
  --manifest examples/release_manifest.tsv \
  --out-dir /tmp/release_bundle_validation
```

Expected outputs:

- `/tmp/release_bundle_validation/fasta_validation.tsv`
- `/tmp/release_bundle_validation/fasta_header_audit.tsv`
- `/tmp/release_bundle_validation/manifest_audit.tsv`
- `/tmp/release_bundle_validation/agp_validation.tsv`

## Interpret The Results

You want these outcomes:

- FASTA passes minimum-length and sequence checks
- FASTA headers are stable and safe
- manifest required files all exist
- AGP passes validation when AGP is part of the bundle

If those conditions hold, the bundle is internally coherent enough for the next review stage.

## What This Example Still Does Not Cover

A real release usually adds:

- BioProject, BioSample, and SRA accession state
- `.sbt` template for annotation submission
- `.sqn`, `.val`, `.stats`, and `.dr` files when annotation is submitted
- optional `.cmt` file such as:

```text
examples/genome_assembly_data.cmt
```

The toy example is deliberately smaller so the file roles are easy to understand.

## Recommended Real-World Directory Shape

For a real submission bundle, keeping one release directory works well:

```text
15_release/
  sample.genome.fa.gz
  sample.agp
  sample.annotation.gff3.gz
  sample.proteins.fa.gz
  sample.transcripts.fa.gz
  sample.repeats.gff3.gz
  sample.repeat_library.fa.gz
  sample.methods.md
  sample.release_manifest.tsv
  validation/
  ncbi_validation/
```

That layout makes it much easier to hand the package to another person or revisit it months later.

## Release Rule

The release bundle is ready for submission review only when the manifest, the actual files, and the chosen release decision all describe the same package.

## Related Files

- `docs/release_package_decision_guide.md`
- `docs/release_candidate_worked_case.md`
- `docs/annotation_submission_handoff.md`
- `examples/release_manifest.tsv`
- `examples/release_bundle/`
- `scripts/check_release_bundle.py`
