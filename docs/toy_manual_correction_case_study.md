# Toy Manual Correction Case Study

This miniature example shows the logic of an evidence-first correction round. The data are toy-sized and not biologically meaningful.

## Scenario

Two candidate edits were reviewed:

- `edit_0001`: accepted break on `chr01`
- `edit_0002`: rejected break on `unplaced_000001`

The accepted edit represents a region where dotplot review and reference-to-assembly IGV inspection agree. The rejected edit represents a suspicious region where evidence did not support a defensible breakpoint.

## Inputs

```text
examples/toy/toy_assembly.fa
examples/toy/toy_breaks.tsv
examples/toy/toy_correction_decisions.tsv
```

## Commands

Validate breakpoints:

```bash
scripts/validate_breaks.py \
  --fasta examples/toy/toy_assembly.fa \
  --breaks examples/toy/toy_breaks.tsv \
  -o /tmp/toy_breaks_validation.tsv
```

Split the accepted breakpoint:

```bash
scripts/split_fasta_at_breaks.py \
  --fasta examples/toy/toy_assembly.fa \
  --breaks examples/toy/toy_breaks.tsv \
  -o /tmp/toy_split.fa \
  --map /tmp/toy_split.map.tsv
```

Summarize accepted correction products:

```bash
scripts/summarize_corrections.py \
  --split-map /tmp/toy_split.map.tsv \
  --decision-log examples/toy/toy_correction_decisions.tsv \
  -o /tmp/toy_correction_summary.tsv \
  --markdown /tmp/toy_correction_summary.md
```

Audit accepted and rejected decisions:

```bash
scripts/audit_correction_decisions.py \
  examples/toy/toy_correction_decisions.tsv \
  -o /tmp/toy_correction_decision_audit.tsv
```

Create a report:

```bash
scripts/make_correction_report.py \
  --sample toy \
  --version 0.4.0-dev \
  --decision-log examples/toy/toy_correction_decisions.tsv \
  --decision-audit /tmp/toy_correction_decision_audit.tsv \
  --correction-summary /tmp/toy_correction_summary.tsv \
  --split-map /tmp/toy_split.map.tsv \
  --break-validation /tmp/toy_breaks_validation.tsv \
  --fasta-validation /tmp/toy_split_validation.tsv \
  -o /tmp/toy_post_correction_report.md
```

## Expected Outcome

- `chr01` is split into `chr01_part01` and `chr01_part02`.
- `unplaced_000001` is retained.
- The correction decision audit passes both rows.
- The report contains both accepted and rejected decisions.

## Lesson

The rejected edit is not wasted effort. It documents that the suspicious region was reviewed and retained because evidence did not support a confident break.
