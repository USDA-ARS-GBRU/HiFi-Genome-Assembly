# Post-Correction Validation Mini-Workflow

Run this workflow after any accepted split, removal, orientation change, or scaffold rebuild. The goal is to prove that the corrected FASTA is internally valid and that downstream release files were regenerated or intentionally deferred.

## Required Inputs

```text
corrected FASTA
breakpoint TSV or correction decision log
split map, if FASTA was split
AGP, if scaffold/chromosome objects are present
reference FASTA for regenerated dotplots
release manifest
```

## Minimal Checks

```bash
scripts/validate_fasta.py corrected.fa --min-length 200 -o corrected.fasta_validation.tsv
scripts/audit_fasta_headers.py corrected.fa -o corrected.header_audit.tsv
scripts/validate_breaks.py --fasta original.fa --breaks sample.breaks.tsv -o sample.breaks.validation.tsv
scripts/summarize_corrections.py --split-map sample.split_map.tsv --decision-log sample.correction_decisions.tsv -o sample.correction_summary.tsv --markdown sample.correction_summary.md
```

If AGP exists:

```bash
scripts/validate_agp.py corrected.agp -o corrected.agp_validation.tsv
```

If a reference is available:

```bash
sbatch \
  --export target=references/close_reference.fa,query=corrected.fa,sample=corrected_vs_reference,preset=asm20 \
  01_sbatch/minimap_assembly_paf.sbatch
```

## Template Job

The reusable sbatch template is:

```text
01_sbatch_templates/post_correction_validation.sbatch
```

Copy it into a project `01_sbatch/` directory and submit after editing variables for the local cluster.

## Acceptance Criteria

- corrected FASTA has no errors
- corrected FASTA headers are release-safe or reviewed
- breakpoints validate against the original FASTA
- correction summary matches the decision log
- AGP component IDs match the corrected FASTA, when AGP exists
- regenerated dotplots support the final structure
- downstream repeat/gene/release files are marked regenerated or pending

## Release Rule

Do not release a corrected assembly until the corrected FASTA, AGP, correction log, split map, correction summary, dotplots, and release manifest agree.
