# Repeat Library Decision Guide

Use this guide to choose and document the repeat annotation and masking set used for release and gene annotation. The right answer is not always the run with the highest masked percentage.

## Candidate Inputs

Common candidates include:

- EDTA repeat annotation
- RepeatModeler2 library plus RepeatMasker output
- a curated species or genus library
- a combined EDTA plus curated library
- a pan-genome project library used consistently across accessions

Run candidates against the same final FASTA whenever possible.

Recent crop pangenome papers make the case for explicit repeat-library provenance. A project-wide library can improve consistency across accessions, but it can also mask accession-specific novelty if it is applied without review.

## Decision Table

Record decisions in:

```text
examples/repeat_annotation_decisions.tsv
```

Recommended columns:

| Column | Meaning |
| --- | --- |
| `decision_id` | stable decision identifier |
| `sample_id` | project or accession |
| `assembly_version` | assembly version reviewed |
| `candidate_method` | EDTA, RepeatModeler2/RepeatMasker, curated library, combined library |
| `candidate_outputs` | key output files |
| `masked_percent` | total masked percent |
| `unclassified_percent` | unclassified repeat percent |
| `primary_strength` | strongest reason to use this candidate |
| `primary_concern` | strongest reason to reject or review |
| `final_action` | use_for_release, comparison_only, reject, needs_review |
| `gene_annotation_input` | yes/no |
| `reviewer` | reviewer name or initials |
| `notes` | short rationale |

## Choosing the Release Mask

Prefer the candidate that is:

- biologically plausible for the crop
- compatible with gene annotation
- reproducible from documented commands
- based on final sequence IDs
- not inflated by contamination, organelles, haplotig duplication, or unreviewed alternate haplotypes
- clear about unclassified repeat burden

Compare repeat summaries before choosing the release mask:

```bash
scripts/compare_repeat_summaries.py \
  --candidate edta=examples/repeat_summary_edta.tsv \
  --candidate repeatmodeler=examples/repeat_summary_repeatmodeler.tsv \
  -o /tmp/repeat_summary_comparison.tsv
```

Audit the final decision log before release:

```bash
scripts/audit_repeat_annotation_decisions.py \
  examples/repeat_annotation_decisions.tsv \
  -o /tmp/repeat_annotation_decision_audit.tsv
```

## Common Decision Cases

| Observation | Interpretation | Action |
| --- | --- | --- |
| EDTA and RepeatModeler agree on total masked percent | strong support for overall repeat burden | choose based on classification quality and downstream compatibility |
| EDTA has better TE classification | common for plant genomes | use EDTA for release if outputs are reproducible |
| RepeatModeler finds many unclassified repeats | useful comparison but may need curation | comparison only or curate before release |
| masked percent is much higher than related cultivars | may be biology, haplotigs, contamination, or repeats in unplaced contigs | review before release |
| soft-masked FASTA differs from gene annotation input | provenance problem | rerun gene annotation or regenerate handoff files |
| repeat tracks use old sequence names | release mismatch | remap or rerun repeat annotation |
| pangenome project uses per-accession libraries only | annotation differences may reflect library differences | consider shared curated or panEDTA-style library comparison |

## Handoff to Gene Annotation

The gene annotation team should receive:

```text
13_repeats/sample.softmasked.fa
13_repeats/sample.repeatmasker.gff
13_repeats/sample.repeat_library.fa
13_repeats/sample.repeat_summary.tsv
13_repeats/sample.repeat_decisions.tsv
```

Do not change the repeat library after gene annotation starts unless the gene annotation is rerun or explicitly validated.

## Manuscript Language

```text
Repeats were annotated using [EDTA/RepeatModeler2 + RepeatMasker/curated library] on the final assembly sequence set. Candidate repeat annotations were compared by total masked fraction, major repeat classes, unclassified repeat burden, library provenance, and compatibility with downstream gene annotation. The selected release mask was used to generate a soft-masked genome for gene prediction.
```

## Reviewer Response Language

```text
We have clarified how the repeat library was selected. Candidate repeat annotations were reviewed for masked fraction, TE classification, unclassified repeat burden, library provenance, and compatibility with the gene annotation input. The selected soft-masked FASTA and repeat GFF were regenerated from the final release sequence IDs.
```
