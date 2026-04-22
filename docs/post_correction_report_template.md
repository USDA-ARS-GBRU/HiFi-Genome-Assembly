# Post-Correction Report Template

Use this report after any correction round. It should be short enough for a project record but complete enough for manuscript review, NCBI release review, and future reuse.

## Assembly and Version

```text
sample_id:
pre_correction_assembly:
post_correction_assembly:
roadmap_version:
date:
reviewer:
```

## Correction Summary

```text
number_of_candidate_edits:
number_accepted:
number_rejected:
number_of_sequences_split:
number_of_sequences_removed:
number_of_sequences_retained_after_review:
```

Attach:

- correction decision log
- split map
- correction summary TSV/Markdown
- minimum evidence checklist

## Accepted Edits

For each accepted edit:

```text
edit_id:
sequence_id:
final_action:
coordinate_or_interval:
primary_evidence:
secondary_evidence:
IGV_images:
dotplot_images:
downstream_files_regenerated:
remaining_caveats:
```

## Rejected Edits

For each rejected edit:

```text
edit_id:
sequence_id:
proposed_action:
final_action: retain
reason_rejected:
evidence_supporting_retention:
images_or_tracks_reviewed:
```

Rejected edits are not failures. They show that the assembly was reviewed conservatively and that suspicious regions were not fragmented without sufficient evidence.

## Validation Results

```text
corrected_fasta_validation:
header_audit:
breakpoint_validation:
agp_validation:
correction_summary:
post_correction_dotplot:
release_manifest_audit:
```

## Manuscript-Ready Summary

```text
Candidate structural discrepancies were reviewed using [dotplots/reference-to-assembly IGV/minimap2/Hi-C/read-depth/k-mer evidence]. Edits were accepted only when a precise coordinate was supported by independent evidence. [N] candidate edits were reviewed; [A] were accepted and [R] were rejected. Downstream FASTA, AGP, and release validation files were regenerated after accepted corrections.
```

## Release Decision

```text
ready_for_release: yes/no
blocking_items:
nonblocking_caveats:
next_review_date:
```

Generate a draft report from project TSV outputs:

```bash
scripts/make_correction_report.py \
  --sample sample \
  --decision-log sample.correction_decisions.tsv \
  --decision-audit sample.correction_decision_audit.tsv \
  --correction-summary sample.correction_summary.tsv \
  --split-map sample.split_map.tsv \
  --fasta-comparison sample.fasta_comparison.tsv \
  --break-validation sample.breaks.validation.tsv \
  -o sample.post_correction_report.md
```
