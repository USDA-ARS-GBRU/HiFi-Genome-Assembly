# Assembly Decision Log Template

Use this file to record decisions that affect the biological interpretation or public release of an assembly. Reviewers and future users should be able to understand why each non-default choice was made.

## Project

| Field | Value |
| --- | --- |
| Sample ID |  |
| Species |  |
| Cultivar/accession |  |
| Assembly version |  |
| Workflow commit |  |
| Analyst |  |
| Date opened |  |
| Date finalized |  |

## Decision Summary

| Decision ID | Date | Topic | Decision | Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| D001 |  | Read filtering |  |  | open |

## Decision Entry Template

### D001: Short Title

Date:

Status:

Question:

Options considered:

Evidence reviewed:

- Read statistics:
- k-mer profile:
- Assembly statistics:
- BUSCO:
- Merqury:
- Dotplot:
- Hi-C/contact map:
- Contamination screen:
- Other:

Decision:

Rationale:

Files affected:

Commands or scripts:

Follow-up checks:

Reviewer initials/date:

## Common Decisions to Record

- Whether raw or trimmed HiFi reads were used.
- Whether multiple SMRT Cells or barcodes were combined.
- hifiasm mode and non-default parameters.
- Primary, alternate, haplotype, or scaffolded assembly selected for release.
- Whether purge_dups, purge_haplotigs, or hifiasm `-l0` testing was used.
- Any manual contig breaks, joins, or removals.
- RagTag or reference-guided scaffolding choices.
- Hi-C curation decisions.
- Suspected contamination removal or retention.
- Organelle sequence handling.
- Telomere/internal telomere interpretation.
- Repeat library choice.
- Gene annotation evidence choice.
- NCBI submission corrections.

