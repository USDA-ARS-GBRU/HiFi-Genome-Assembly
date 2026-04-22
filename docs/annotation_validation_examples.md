# Annotation Validation Examples

This guide explains the tiny annotation validation fixtures in `examples/annotation_validation/`. They are designed for teaching table2asn-style review before students work with large crop genome annotations.

## Why These Fixtures Exist

Full annotation validation requires NCBI tools and project metadata that may not be available in every teaching or CI environment. These files provide a small, readable example of the relationships that table2asn checks:

- FASTA sequence IDs must match GFF3 sequence IDs.
- Gene, mRNA, exon, and CDS features must have consistent parent-child relationships.
- Public annotation should use stable locus tags.
- Product names should be conservative and database-friendly.
- Features must not point to scaffolds absent from the submitted FASTA.

## Fixture Set

```text
examples/annotation_validation/toy_genome.fsa
examples/annotation_validation/toy_annotation.gff3
examples/annotation_validation/toy_problem_annotation.gff3
examples/annotation_validation/toy_table2asn_template.sbt
examples/annotation_validation/expected_validation_summary.tsv
examples/annotation_validation/expected_table2asn_review.md
```

## Suggested Review Exercise

1. Open `toy_genome.fsa` and write down the sequence IDs.
2. Open `toy_annotation.gff3` and confirm every feature uses one of those sequence IDs.
3. Check that each mRNA has a parent gene and that each exon/CDS has a parent mRNA.
4. Check that genes have locus tags.
5. Repeat the exercise for `toy_problem_annotation.gff3`.
6. Compare your findings with `expected_validation_summary.tsv`.

Run the lightweight local ID audit:

```bash
scripts/audit_gff3_fasta_ids.py \
  --fasta examples/annotation_validation/toy_genome.fsa \
  --gff3 examples/annotation_validation/toy_annotation.gff3 \
  -o /tmp/toy_annotation_id_audit.tsv
```

The problem fixture should fail this audit because it contains `Toy_missing_scaffold`, which is not present in the FASTA.

## Optional table2asn Run

If table2asn is installed:

```bash
sbatch \
  --export fasta=examples/annotation_validation/toy_genome.fsa,gff=examples/annotation_validation/toy_annotation.gff3,template=examples/annotation_validation/toy_table2asn_template.sbt,sample=toy_good \
  01_sbatch/table2asn_validate.sbatch
```

Then repeat with `toy_problem_annotation.gff3`. Review `.val`, discrepancy, and `.sqn` outputs in `15_release/ncbi_validation/`.

## Real Project Rule

Any final FASTA change can invalidate annotation coordinates. After renaming, splitting, removing contamination, changing scaffold order, or changing soft masking, rerun annotation validation before release.
