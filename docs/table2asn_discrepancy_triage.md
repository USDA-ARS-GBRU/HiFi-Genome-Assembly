# table2asn and Discrepancy Triage

Use this guide after running `table2asn` on a candidate crop plant annotation package.

The goal is not to make every warning disappear. The goal is to separate:

- true blocking submission errors
- annotation problems that should be fixed before release
- acceptable biological edge cases that should be documented

## Start With The Smallest Reliable Questions

Review in this order:

1. Do FASTA and GFF3 sequence IDs match?
2. Did any sequence names change after annotation was generated?
3. Are there missing locus tags?
4. Are there internal stops or obviously broken CDS models?
5. Are features crossing gaps or broken assembly edges?
6. Are product names too informal, repetitive, or misleading?
7. Which remaining warnings are biological edge cases rather than formatting failures?

That order matters. It keeps you from wasting time renaming proteins in an annotation that is still attached to the wrong FASTA.

## Official NCBI Points

Current official guidance checked during drafting:

- NCBI's GFF3 submission guide says features should not begin or end inside a gap and that `table2asn` validation and discrepancy outputs should be reviewed and fixed before submission: [Annotating Genomes with GFF3 or GTF files](https://www.ncbi.nlm.nih.gov/genbank/genomes_gff/)
- NCBI's genome submission guidance says annotated genome submissions require locus-tag-aware annotation packaging: [About Genome (WGS) Submission](https://submit.ncbi.nlm.nih.gov/about/genome/)

Inference from those sources: for eukaryotic crop genomes, missing IDs, locus-tag failures, and gap-crossing features should be treated as structural issues first, not as cosmetic cleanup.

## Common Issue Classes

### Missing or inconsistent sequence IDs

Typical symptoms:

- features on missing sequence IDs
- `.val` errors that point to scaffolds absent from the FASTA
- GFF3 still using pre-rename or pre-split sequence names

What it usually means:

- the annotation is tied to an older release object

Action:

- regenerate or liftover annotation against the frozen FASTA
- rerun local ID audit
- rerun `table2asn`

Related local check:

```bash
scripts/audit_gff3_fasta_ids.py \
  --fasta examples/annotation_validation/toy_genome.fsa \
  --gff3 examples/annotation_validation/toy_problem_annotation.gff3 \
  -o /tmp/toy_annotation_id_audit.tsv
```

### Missing locus tags

Typical symptoms:

- validator complains about absent locus tags
- some genes have tags while others do not

What it usually means:

- locus-tag injection strategy was not finalized
- mixed files from multiple annotation rounds were combined

Action:

- choose one strategy and record it clearly:
  - tags already present in GFF3
  - tags added consistently during submission packaging
- rerun validation

### Internal stops and broken CDS models

Typical symptoms:

- CDS with premature stop codons
- protein translation discrepancies

What it usually means:

- pseudogene-like models
- frame problems from aligner/modeler output
- annotation tied to a stale assembly version

Action:

- confirm the genomic sequence first
- inspect the offending gene model
- decide whether to repair, mark partial, or remove from the release gene set

### Features crossing gaps

Typical symptoms:

- genes, mRNAs, or CDS features spanning Ns or assembly gaps

What it usually means:

- a model was projected across an unresolved region
- gap handling was ignored during gene-set selection

Action:

- split or trim the model
- mark partial where appropriate
- avoid submitting a feature that begins or ends inside a gap

### Product names and naming style

Typical symptoms:

- overly casual product names
- all proteins called the same thing without justification
- transposon-related proteins named as canonical genes

What it usually means:

- raw functional annotation was passed through without curation

Action:

- use conservative, database-friendly naming
- distinguish TE-derived models from confident genes
- prefer no claim over an overclaim

## Triage Table

Use a simple decision table during review:

| Issue class | Release blocker | Fix now | Can document and proceed |
| --- | --- | --- | --- |
| FASTA/GFF3 ID mismatch | yes | yes | no |
| Missing locus tags | yes | yes | no |
| Genes crossing gaps | usually yes | yes | rarely |
| Internal stop in key release model | often yes | yes | sometimes, with rationale |
| Informal product names | usually no | yes | sometimes |
| Repeat-derived questionable models | often | yes | sometimes, after filtering |

## Worked Toy Review

The tiny fixtures in:

```text
examples/annotation_validation/
```

are useful for practicing the logic before you touch a real annotation package.

Expected review notes:

- `toy_annotation.gff3`: should pass local ID review and mainly teach the structure of a clean handoff
- `toy_problem_annotation.gff3`: should trigger attention for a missing locus tag, informal naming, and a feature on a scaffold absent from the FASTA

See:

- `docs/annotation_validation_examples.md`
- `examples/annotation_validation/expected_table2asn_review.md`

## Suggested Review Order In Practice

1. Run local FASTA/GFF3 ID audit.
2. Review sequence renaming or splitting history.
3. Review locus-tag strategy.
4. Review `.val` errors.
5. Review discrepancy report categories.
6. Fix structural issues.
7. Fix naming and product issues.
8. Archive the final `.sqn`, `.val`, `.stats`, and `.dr` together.

## Reviewer-Ready Language

Methods:

> Candidate annotation releases were validated against the frozen assembly identifiers using local FASTA/GFF3 audits and `table2asn`. Structural validation issues, including identifier mismatches, missing locus tags, and gap-crossing models, were resolved before product-name cleanup and release packaging.

Reviewer response:

> We triaged annotation validation issues by first resolving structural inconsistencies between the frozen assembly and the submitted annotation package. Only after identifier, locus-tag, and gap-related issues were addressed did we curate product-name and discrepancy categories that reflected biological edge cases.

## Related Files

- `docs/annotation_validation_examples.md`
- `docs/annotation_submission_handoff.md`
- `docs/release_candidate_worked_case.md`
- `examples/annotation_validation/expected_table2asn_review.md`
