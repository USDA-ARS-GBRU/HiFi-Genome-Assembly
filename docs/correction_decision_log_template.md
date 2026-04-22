# Correction Decision Log Template

Use this template whenever you propose changing the assembly FASTA after the initial assembler output. Every edit should be understandable months later by someone who was not in the room when the decision was made.

## TSV Columns

```text
edit_id
sample_id
assembly_version
sequence_id
start_1based
end_1based
proposed_action
final_action
primary_evidence
secondary_evidence
tools_and_versions
reviewer
review_date
downstream_files_regenerated
notes
```

## Allowed Actions

Use controlled terms when possible:

- `retain`
- `break`
- `reverse_complement`
- `reorder`
- `remove`
- `mask`
- `submit_separately`
- `rename_only`

## Example Rows

```text
edit_id	sample_id	assembly_version	sequence_id	start_1based	end_1based	proposed_action	final_action	primary_evidence	secondary_evidence	tools_and_versions	reviewer	review_date	downstream_files_regenerated	notes
edit_0001	SampleID	v0.3.0-dev	chr03	14500001	14500002	break	break	Hi-C contact map break	HiFi read alignments stop at same position	minimap2 2.28; samtools 1.20	ReviewerName	2026-04-22	yes	Break introduced between bases 14500001 and 14500002.
edit_0002	SampleID	v0.3.0-dev	chr07	1	9800000	reverse_complement	retain	dotplot orientation conflict	alternate cultivar agrees with current orientation	MUMmer 4.0.0rc1	ReviewerName	2026-04-22	no	Retained because only one reference supported flipping.
```

## Evidence Standard

For destructive edits such as breaking or removing sequence, require at least two independent evidence types when possible. Dotplots are excellent triage tools, but a dotplot alone is usually not enough for a crop genome correction.

## Coordinate Rule

For breakpoints used with `scripts/split_fasta_at_breaks.py`, record `break_after_1based`. A value of `1000` means the first output segment ends at base 1000 and the next begins at base 1001.

## Release Rule

After any edit that changes sequence IDs, coordinates, or sequence content, regenerate or revalidate:

- FASTA index
- AGP
- repeat annotation coordinates
- gene annotation coordinates
- telomere/centromere summaries
- contamination decisions
- release manifest
- NCBI/table2asn validation outputs
