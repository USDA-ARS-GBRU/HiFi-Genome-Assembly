# Annotation Submission Handoff

Use this page when the assembly is frozen and the annotation package is being prepared for submission or handoff to another team member.

The goal is simple: the person running the final annotation submission should not have to guess which FASTA, which GFF3, which template, or which discrepancy report is the real one.

## Freeze Set

Before annotation submission, freeze this exact set together:

- final genome FASTA
- AGP, if required for scaffolded or chromosome-scale submission
- final submission GFF3 or feature input
- submitter template (`.sbt`)
- locus-tag plan or assigned prefix
- validation outputs (`.val`, `.stats`, `.dr`)
- accession tracking table
- release manifest

If one of these changes, rerun the annotation submission validation. Do not treat the old `.sqn` file as still valid.

## Official NCBI Points To Remember

Current official guidance checked during drafting:

- NCBI says feature annotation is optional for genome submissions, but annotated submissions must be uploaded as an annotated package rather than only a FASTA file: [About Genome (WGS) Submission](https://submit.ncbi.nlm.nih.gov/about/genome/)
- NCBI's GFF3 guidance says features should not begin or end inside a gap and recommends running `table2asn` with eukaryote-appropriate arguments plus gap handling and locus-tag handling: [Annotating Genomes with GFF3 or GTF files](https://www.ncbi.nlm.nih.gov/genbank/genomes_gff/)

Inference from those sources: the final annotation handoff should explicitly note the gap policy, the locus-tag source, and the exact FASTA/GFF3 pair used to build the package.

## Handoff Checklist

- [ ] FASTA path recorded
- [ ] GFF3 path recorded
- [ ] AGP path recorded or marked not applicable
- [ ] `.sbt` template recorded
- [ ] locus-tag prefix source recorded
- [ ] `table2asn` command or sbatch path recorded
- [ ] validation report reviewed
- [ ] discrepancy report reviewed
- [ ] unresolved warnings listed with rationale
- [ ] accession tracking table updated

## Common Failure Modes

### FASTA/GFF3 drift

Symptoms:

- features on missing sequence IDs
- coordinates no longer match scaffold names
- genes crossing gaps after late sequence edits

Fix:

- regenerate or liftover the annotation against the frozen FASTA
- rerun `table2asn`

### Locus-tag confusion

Symptoms:

- missing locus tags
- inconsistent locus-tag prefixes across files

Fix:

- record whether locus tags are in the GFF3 or injected at submission time
- keep that choice stable across reruns

### Late structural edits after annotation freeze

Symptoms:

- validator failures after a last-minute split, trim, contamination removal, or rename

Fix:

- invalidate the old package
- rerun the annotation handoff from the frozen assembly state

## Suggested Handoff Note

```text
Assembly release object: sample_v1
Frozen FASTA: 15_release/sample_v1.genome.fa.gz
AGP: 15_release/sample_v1.agp
GFF3: 15_release/sample_v1.annotation.gff3.gz
Submitter template: 00_metadata/template.sbt
Locus-tag handling: tags present in GFF3
table2asn path: 01_sbatch_templates/table2asn_validate.sbatch
Latest validation outputs: 15_release/ncbi_validation/sample_v1/
Open warnings: partial genes adjacent to terminal gaps reviewed and retained
Accession tracker updated: examples/accession_tracking.tsv
```

## Release Rule

The annotation package is ready for handoff only when a new team member can identify the exact FASTA, GFF3, template, and validation outputs without asking for clarification.
