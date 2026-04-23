# T2T Completeness Evidence Package

Use this package when a project wants to describe chromosome completeness, near-gapless status, candidate T2T chromosomes, or a T2T-quality assembly. The package is meant to keep claims conservative and reproducible.

## Core Table

Create one row per chromosome-scale scaffold:

```text
examples/t2t_completeness_evidence.tsv
```

Recommended columns:

| Column | Meaning |
| --- | --- |
| `sample_id` | project or accession identifier |
| `assembly_version` | assembly version being reviewed |
| `sequence_id` | final chromosome/scaffold ID |
| `length_bp` | sequence length |
| `gap_count` | number of N runs in FASTA |
| `agp_gap_count` | number of AGP gap records |
| `left_telomere_status` | terminal motif evidence at left end |
| `right_telomere_status` | terminal motif evidence at right end |
| `internal_telomere_status` | whether internal telomere motifs need review |
| `centromere_status` | centromere candidate confidence |
| `centromere_evidence` | repeat, Hi-C, CENH3, quarTeT, or other support |
| `hic_status` | contact-map support |
| `dotplot_status` | whole-genome alignment support |
| `difficult_repeat_status` | rDNA, satellite, knob, introgression, B chromosome, or other special case |
| `claim_class` | chromosome-scale, near-gapless, candidate T2T chromosome, or unresolved |
| `review_notes` | short rationale |

## Evidence Classes

Use controlled language where possible.

### Telomere Status

- `terminal_supported`
- `terminal_missing`
- `terminal_ambiguous`
- `wrong_motif_possible`
- `not_reviewed`

### Internal Telomere Status

- `none_detected`
- `candidate_interstitial_repeat`
- `possible_misjoin`
- `needs_review`
- `not_reviewed`

### Centromere Status

- `high_confidence`
- `moderate_confidence`
- `low_confidence`
- `not_detected`
- `not_reviewed`

High-confidence centromere calls should have more than one support type whenever possible, such as tandem-repeat enrichment plus Hi-C behavior, CENH3 ChIP-seq, or a lineage-aware centromere repeat model.

### Claim Class

- `chromosome_scale`
- `near_gapless`
- `candidate_t2t_chromosome`
- `unresolved`

Do not use `candidate_t2t_chromosome` unless the row has no gaps, terminal telomere support at both ends, plausible centromere evidence, and no unresolved contact-map or dotplot concerns.

## Review Logic

Use this package together with:

- `docs/telomere_summary_workflow.md`
- `docs/t2t_readiness_checklist.md`
- `docs/t2t_claim_language_guide.md`
- `docs/hic_contact_map_qc.md`
- `docs/scaffolding_worked_decision_case.md`
- `docs/release_checklist.md`

When evidence conflicts, downgrade the claim. A conservative chromosome-scale claim is stronger than an unsupported T2T claim.

Audit the evidence table before using it in release text:

```bash
scripts/audit_t2t_evidence_package.py \
  examples/t2t_completeness_evidence.tsv \
  -o /tmp/t2t_evidence_audit.tsv
```

## Methods Language

```text
Chromosome completeness was reviewed using a structured evidence table combining FASTA gap status, AGP gap records, terminal and internal telomeric repeat calls, centromere candidate evidence, Hi-C contact-map review, dotplot review, and difficult-repeat annotations. Chromosomes were classified conservatively as chromosome-scale, near-gapless, candidate T2T, or unresolved according to the weakest unresolved evidence category.
```

For more claim-specific manuscript and reviewer-response text, see `docs/t2t_claim_language_guide.md`.

## Reviewer Response Language

```text
We have revised the completeness language to avoid overclaiming T2T status. The assembly is described as [chromosome-scale/near-gapless/candidate T2T for N chromosomes] because [specific remaining evidence limitation]. We now provide a per-chromosome evidence table summarizing gap status, telomere calls, centromere candidates, Hi-C support, dotplot support, and difficult-repeat review.
```
