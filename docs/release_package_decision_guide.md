# Release Package Decision Guide

Use this guide when multiple candidate release packages exist and you need to decide what should actually be submitted.

Typical candidates:

- assembly-only FASTA for an early genome release
- assembly plus AGP for scaffolded or chromosome-scale submission
- assembly plus annotation package for a combined annotated release
- assembly release now, annotation release later
- NCBI submission now, community database package later

The right choice is the package with the strongest end-to-end consistency, not the package with the most files or the most ambitious label.

## Decision Questions

Ask these in order:

1. Is the assembly frozen?
2. Are sequence names stable across FASTA, AGP, and GFF3?
3. Does the chosen submission target require AGP?
4. Does the chosen submission target require a completed annotation package?
5. Are BioProject and BioSample ready?
6. Are SRA accessions available, or at minimum clearly tracked as pending?
7. Does the methods text match what will actually be submitted?

If any answer is "no", the honest action is usually `hold` or `needs_review`, not `use_for_submission`.

## Recommended Package Classes

### Assembly-Only

Choose this when:

- the assembly is frozen
- contamination and structural review are complete
- annotation is still being revised
- you want the assembly public without overclaiming annotation readiness

Usually required:

- FASTA
- FASTA header audit
- FASTA validation
- AGP if scaffold/chromosome objects are built from contigs
- release manifest
- BioProject/BioSample metadata

### Annotated Genome

Choose this when:

- the assembly is frozen
- annotation sequence IDs match the final FASTA
- locus-tag planning is complete
- `table2asn` validation has been reviewed
- discrepancy outputs have been triaged

Usually required:

- final FASTA
- AGP when applicable
- GFF3 or feature input used to build the submission package
- `.sqn` or equivalent annotated submission package
- `.val`, `.dr`, and supporting notes

### Split Release

Choose this when:

- the assembly is ready now
- annotation is biologically useful but still changing
- release timing matters more than keeping assembly and annotation bundled together

This is often the cleanest option for crop projects under review pressure.

## Use the Decision Table

Track candidate packages in:

```text
examples/release_submission_decisions.tsv
```

Audit with:

```bash
scripts/audit_release_submission_decisions.py \
  examples/release_submission_decisions.tsv \
  -o /tmp/release_submission_decision_audit.tsv
```

## Decision Rules

- A scaffold- or chromosome-level package marked `use_for_submission` should include AGP.
- An `annotated_genome` or `combined_release` package marked `use_for_submission` should include an annotation package.
- A package marked `use_for_submission` should have BioProject and BioSample ready.
- SRA can still be pending during package review, but it should not be `not_applicable` for a PacBio HiFi crop genome project.
- Only one release package per sample, assembly version, and submission target should be marked `use_for_submission`.

## Worked Logic

Good release decisions often look like this:

- `assembly_only` package: ready now, stable assembly, AGP included, metadata ready
- `combined_release` package: comparison only, because table2asn cleanup is still in progress

That is a strong decision, not a compromise. It avoids delaying a solid assembly release for annotation issues that are still being corrected.

## Reviewer-Ready Language

Methods:

> The assembly release package was frozen before annotation submission review. Because feature validation and discrepancy review were still being resolved, we submitted the assembly package first and retained the annotation package as a later release candidate.

Reviewer response:

> We did not bundle the annotation with the first public assembly release because the annotated package had not yet completed final validation against the frozen assembly identifiers. We favored consistency between release objects over simultaneous release.

## Related Files

- `docs/v0.9_ncbi_release_kickoff.md`
- `docs/annotation_submission_handoff.md`
- `docs/release/ncbi_submission.md`
- `docs/release/ncbi_submission.md`
- `docs/ncbi_metadata_templates.md`
- `examples/accession_tracking.tsv`
