# Rejected Corrections

Rejected corrections are a strength of an evidence-first workflow. They show that a suspicious signal was reviewed and that the assembly was not edited without enough support.

## When to Reject a Proposed Break

Reject a break when:

- the dotplot is ambiguous
- the reference-to-assembly alignment does not define a precise coordinate
- HiFi read support continues across the candidate breakpoint
- Hi-C contacts support the existing structure
- k-mer or depth evidence does not change at the candidate coordinate
- the pattern is consistent with cultivar-specific structural variation
- only one distant reference supports the edit
- an automated tool proposes many breaks without independent support

## How to Record Rejection

Use `final_action=retain` in the correction decision log:

```text
edit_id	sample_id	assembly_version	sequence_id	start_1based	end_1based	proposed_action	final_action	primary_evidence	secondary_evidence	tools_and_versions	reviewer	review_date	downstream_files_regenerated	notes
edit_0002	toy	v0.4.0-dev	unplaced_000001	1	47	break	retain	dotplot ambiguity	continuous HiFi support and no clear reference-to-assembly breakpoint	minimap2; IGV	ExampleReviewer	2026-04-22	no	Reviewed but retained because evidence did not support a defensible break.
```

## Report Language

```text
A candidate breakpoint on [sequence_id] was reviewed because [dotplot/tool/evidence] suggested [pattern]. Reference-to-assembly alignments in IGV did not reveal a defensible breakpoint, and [HiFi/Hi-C/k-mer/alternate reference] evidence supported retaining the original sequence. No edit was made, and the region was recorded as reviewed in the correction decision log.
```

## Review Rule

A rejected correction should include enough evidence that a future reviewer can understand why the region was retained. Do not leave serious candidate edits as undocumented memory.
