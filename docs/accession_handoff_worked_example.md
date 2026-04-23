# Accession Handoff Worked Example

This worked example shows how accession tracking, release decisions, methods text, and submission notes should agree before a public crop genome release.

## Scenario

Sample:

- `maize_line_a`
- PacBio HiFi assembly with Hi-C scaffolding
- first public release is assembly-only
- annotation remains in internal review

The accession tracker should make that immediately obvious.

## Example Tracking Table

Start from the project-wide tracking shape in:

```text
examples/accession_tracking.tsv
```

A release-ready version might look like this:

```text
object	local_name	accession	status	release_date	parent_or_linked_object	notes
BioProject	maize_line_a_project	PRJNA123456	submitted	2026-05-10	none	Study umbrella for all release objects.
BioSample	maize_line_a_leaf	SAMN12345678	submitted	2026-05-10	maize_line_a_project	Leaf tissue used for HiFi and Hi-C.
SRA	maize_line_a_hifi	SRR12345678	submitted	2026-05-10	maize_line_a_leaf	PacBio HiFi reads for primary assembly.
SRA	maize_line_a_hic	SRR12345679	submitted	2026-05-10	maize_line_a_leaf	Hi-C reads for scaffolding.
Assembly	maize_line_a_v1	GCA_123456789.1	submitted	2026-05-12	maize_line_a_leaf	First public chromosome-scale assembly release.
Annotation	maize_line_a_v1_genes	pending	internal_review		maize_line_a_v1	Held until table2asn discrepancy cleanup is complete.
```

## What The Table Should Tell A Reader

Without extra explanation, another team member should be able to tell:

- which biological sample was sequenced
- which read sets support the release
- which assembly accession corresponds to the public package
- whether annotation was submitted or intentionally deferred

If the table does not answer those questions, it is not ready.

## Match The Release Decision

The accession handoff should agree with:

```text
examples/release_submission_decisions.tsv
```

If the release decision says `assembly_only`, the accession tracker should not imply that annotation has already been submitted.

## Match The Methods Text

Short methods wording:

> The first public release for maize_line_a consisted of the chromosome-scale assembly package linked to BioProject PRJNA123456, BioSample SAMN12345678, and PacBio HiFi and Hi-C read submissions. The annotation package was retained for later submission pending completion of `table2asn` discrepancy review.

## Match The Submission Note

Short internal handoff note:

```text
Release object submitted: maize_line_a_v1 assembly-only package
Assembly accession: GCA_123456789.1
Linked BioProject: PRJNA123456
Linked BioSample: SAMN12345678
Linked SRA runs: SRR12345678, SRR12345679
Annotation status: internal_review, not yet submitted
Reason annotation held: discrepancy cleanup still in progress
```

## Common Failure Modes

### Assembly accession updated but tracker not updated

Result:

- methods text and README still point to an outdated assembly object

### Annotation submitted later but notes still say pending

Result:

- internal confusion and reviewer-facing inconsistency

### BioSample or SRA links missing

Result:

- release object cannot be traced cleanly back to the biological source and read evidence

## Release Rule

The accession handoff is complete only when the tracking table, the release decision, and the methods text all describe the same public object.

## Related Files

- `docs/release_candidate_worked_case.md`
- `docs/release_package_decision_guide.md`
- `docs/release_methods_and_structured_comments.md`
- `examples/accession_tracking.tsv`
- `examples/release_submission_decisions.tsv`
