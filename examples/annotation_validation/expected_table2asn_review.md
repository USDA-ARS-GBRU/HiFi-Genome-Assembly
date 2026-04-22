# Toy table2asn Review Notes

These files are intentionally tiny. They teach the shape of an annotation validation review; they are not a biological annotation.

## Files

```text
toy_genome.fsa
toy_annotation.gff3
toy_problem_annotation.gff3
toy_table2asn_template.sbt
expected_validation_summary.tsv
```

## Example Commands

```bash
mkdir -p /tmp/hifi_table2asn_toy/good
cp examples/annotation_validation/toy_genome.fsa /tmp/hifi_table2asn_toy/good/toy.fsa
cp examples/annotation_validation/toy_annotation.gff3 /tmp/hifi_table2asn_toy/good/toy.gff
cp examples/annotation_validation/toy_table2asn_template.sbt /tmp/hifi_table2asn_toy/good/template.sbt

cd /tmp/hifi_table2asn_toy/good
table2asn -M n -J -c w -euk -t template.sbt -i toy.fsa -f toy.gff -V vb
```

For the problem fixture, replace `toy_annotation.gff3` with `toy_problem_annotation.gff3`.

## Expected Review Logic

The good fixture should have matching FASTA and GFF3 sequence IDs, locus tags, conservative products, and simple parent-child feature relationships.

The problem fixture should draw attention to:

- a gene without a `locus_tag`
- product wording that may be too informal for public records
- a feature on `Toy_missing_scaffold`, which is absent from the FASTA

Real table2asn output file names and wording can vary by version. Review the `.val`, discrepancy report, generated `.sqn`, and any terminal messages. Treat every error as blocking until fixed or intentionally documented.
