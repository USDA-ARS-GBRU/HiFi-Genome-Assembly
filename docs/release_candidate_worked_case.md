# Release Candidate Worked Case

This worked case shows how to choose a first public release package when the assembly is frozen but the annotation package is still under review.

The point is not to maximize ambition. The point is to submit the strongest package that can be defended end to end.

## Scenario

Sample:

- `maize_line_a`
- PacBio HiFi primary assembly with Hi-C scaffolding
- chromosome-scale release object with AGP
- repeat annotation complete
- gene annotation biologically useful but still in `table2asn` discrepancy cleanup

Candidate packages:

1. `assembly_only`
2. `combined_release`

Decision table:

```text
examples/release_submission_decisions.tsv
```

Audit:

```bash
scripts/audit_release_submission_decisions.py \
  examples/release_submission_decisions.tsv \
  -o /tmp/release_submission_decision_audit.tsv
```

## Evidence Review

### Candidate 1: Assembly-Only

Strengths:

- frozen FASTA
- AGP present
- BioProject ready
- BioSample ready
- SRA path tracked as pending
- no dependency on unresolved annotation discrepancy cleanup

Limitation:

- gene models are not part of the first release object

### Candidate 2: Combined Release

Strengths:

- would provide assembly and annotation together
- annotation is already far enough along to support internal review

Limitation:

- discrepancy review is not finished
- release identifiers are stable, but the annotation package is not yet defensible as final

## Final Decision

Choose:

- `assembly_only` as `use_for_submission`
- `combined_release` as `comparison_only`

Why:

- the assembly package is already coherent across FASTA, AGP, metadata, and release manifest
- the annotation package still has open cleanup tasks
- delaying the assembly release would not improve the assembly itself

This is a conservative release strategy, not a partial success.

## Accession Tracking Example

The release decision should agree with the accession table. A toy example:

```text
object	local_name	accession	status	release_date	parent_or_linked_object	notes
BioProject	maize_line_a_project	PRJNA_pending	draft		none	Study umbrella for genome and reads.
BioSample	maize_line_a_leaf	SAMN_pending	draft		maize_line_a_project	Leaf tissue used for PacBio HiFi and Hi-C.
SRA	maize_line_a_hifi	SRR_pending	draft		maize_line_a_leaf	PacBio HiFi WGS reads.
SRA	maize_line_a_hic	SRR_pending	draft		maize_line_a_leaf	Hi-C scaffolding reads.
Assembly	maize_line_a_v1	GCA_pending	draft		maize_line_a_leaf	Chosen first public release object.
Annotation	maize_line_a_v1_genes	pending	internal_review		maize_line_a_v1	Retained for later annotated release after discrepancy cleanup.
```

## Methods Text

Short methods wording:

> The public release package was prepared from the frozen chromosome-scale assembly version maize_line_a_v1. Because annotation discrepancy review was still ongoing, the first public submission consisted of the assembly package with AGP, while the annotation package was retained as a later release candidate.

## Reviewer Response

Short reviewer-response wording:

> We intentionally separated the first public assembly release from the annotation release candidate. The assembly package had completed structural review and metadata checks, whereas the annotation package still required discrepancy cleanup against the frozen identifiers. We prioritized a consistent first public assembly object over simultaneous release.

## What Would Change The Decision

The `combined_release` package becomes the better choice only after:

- discrepancy outputs are triaged
- locus-tag handling is fixed and recorded
- GFF3 and FASTA IDs are confirmed against the frozen assembly
- `.sqn`, `.val`, and `.dr` outputs are archived with the release package

## Related Files

- `docs/release_package_decision_guide.md`
- `docs/annotation_submission_handoff.md`
- `docs/release_methods_and_structured_comments.md`
- `examples/release_submission_decisions.tsv`
- `examples/accession_tracking.tsv`
