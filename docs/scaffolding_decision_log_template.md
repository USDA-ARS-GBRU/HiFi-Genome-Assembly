# Scaffolding Decision Log Template

Use this template to record scaffold ordering, orientation, placement, and manual curation decisions.

## TSV Columns

```text
decision_id
sample_id
assembly_version
scaffold_id
component_ids
proposed_action
final_action
primary_evidence
secondary_evidence
tools_and_versions
reviewer
review_date
agp_updated
downstream_files_regenerated
notes
```

## Allowed Actions

- `accept_scaffold`
- `reject_scaffold`
- `reorder`
- `reverse_orient`
- `split_scaffold`
- `leave_unplaced`
- `rename`
- `submit_separately`

## Example Rows

```text
decision_id	sample_id	assembly_version	scaffold_id	component_ids	proposed_action	final_action	primary_evidence	secondary_evidence	tools_and_versions	reviewer	review_date	agp_updated	downstream_files_regenerated	notes
scaf_0001	SampleID	0.5.0-dev	chr01	contigA,contigB	accept_scaffold	accept_scaffold	strong Hi-C diagonal	dotplot collinearity	YaHS; Juicebox	ReviewerName	2026-04-22	yes	yes	Accepted chromosome-scale scaffold.
scaf_0002	SampleID	0.5.0-dev	unplaced_001	contigX	accept_scaffold	leave_unplaced	weak contact support	repeat-rich contig	YaHS; Juicebox	ReviewerName	2026-04-22	no	no	Left unplaced due to weak support.
```

## Evidence Standard

Accept scaffold joins only when the contact map supports them. Use dotplots, read-depth evidence, telomere/centromere evidence, and reference comparisons as supporting information, not as replacements for Hi-C signal.

## Release Rule

Every manual scaffold curation decision should be reflected in the final AGP, final FASTA, and release report.
