# AGP After Splitting or Correcting FASTA

Any FASTA edit that changes sequence IDs or coordinates can invalidate AGP. After splitting contigs or scaffolds, rebuild or review AGP before release.

## What Changes After a Split

If `chr01` is split into:

```text
chr01_part01
chr01_part02
```

then downstream scaffold/chromosome records must refer to the new IDs and coordinate spans. Old AGP component IDs that point to `chr01` are no longer valid unless `chr01` remains as a scaffold object built from the new components.

## Recommended Workflow

1. Validate breakpoints.
2. Split FASTA.
3. Inspect the split map.
4. Decide whether the new pieces are final unplaced contigs or components of a rebuilt scaffold.
5. Rebuild AGP using the new component IDs.
6. Run `scripts/validate_agp.py`.
7. Re-run FASTA/header/release bundle validation.

## Toy Example

```bash
scripts/split_fasta_at_breaks.py \
  --fasta examples/toy/toy_assembly.fa \
  --breaks examples/toy/toy_breaks.tsv \
  -o /tmp/toy_split.fa \
  --map /tmp/toy_split.map.tsv

scripts/validate_fasta.py /tmp/toy_split.fa --min-length 1 -o /tmp/toy_split.validation.tsv
```

The split map is the bridge between old and new coordinates:

```text
source_id	new_id	source_start_1based	source_end_1based	length	split
chr01	chr01_part01	1	16	16	yes
chr01	chr01_part02	17	57	41	yes
```

Summarize accepted edits:

```bash
scripts/summarize_corrections.py \
  --split-map /tmp/toy_split.map.tsv \
  --decision-log examples/toy/toy_correction_decisions.tsv \
  -o /tmp/toy_correction_summary.tsv \
  --markdown /tmp/toy_correction_summary.md
```

## Release Rule

Never submit a FASTA/AGP pair if AGP component IDs refer to pre-split sequence names. Validate the final FASTA and final AGP together after every correction round.
