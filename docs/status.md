# Documentation Status and Roadmap

Current version: `0.6.0-dev`

The root `README.md` now serves as a concise landing page while the focused documentation tree carries the detailed protocol. The goal before v1.0 is to keep the repo front page short and keep detailed procedures in `docs/`.

## Current Phase

| Version | Status | Focus |
| --- | --- | --- |
| v0.1 | complete baseline | HiFi assembly core |
| v0.2 | complete baseline | QC dashboard and reports |
| v0.3 | maintained baseline | validation, contamination, release readiness |
| v0.4 | maintained baseline | dotplot review and manual curation |
| v0.5 | signed off | stable baseline for scaffolding, gap filling, T2T readiness, docs-site migration |
| v0.6 | active development | telomere, centromere, and T2T refinement |
| v0.7 | active draft baseline | repeat annotation refinement |
| v0.8 | active draft baseline | gene annotation refinement |
| v0.9 | active drafting | NCBI release candidate polish |
| v1.0 | planned | stable public protocol |

## Documentation Maturity

| Area | Status | Notes |
| --- | --- | --- |
| Setup | draft | tool policy exists; environment pages need expansion |
| Assembly | active draft | read prep, genome profiling, hifiasm, and parameters are split out |
| QC | active draft | metrics, contamination, and dotplots are split out |
| Curation | maintained draft | v0.4 workflow is usable and linked |
| Scaffolding | active draft | Hi-C, AGP, gap filling, and T2T paths are underway |
| Telomere/T2T | active draft | v0.6 kickoff and completeness evidence package started |
| Annotation | active draft | repeat and gene refinement lanes started; gene pages exist as first-pass web docs |
| Release | active draft | NCBI submission path exists and v0.9 is expanding package-level release decisions |
| Docs site | active draft | MkDocs site is live, local strict builds work, and navigation cleanup is in progress |

## v0.5 Exit Goals

- [x] Hi-C scaffolding reader path is usable.
- [x] AGP is defined and validated in docs and helper scripts.
- [x] Gap filling is documented as conservative and evidence-based.
- [x] T2T readiness reports combine gap, telomere, and centromere evidence.
- [x] README workflow steps have focused docs coverage.
- [x] Markdown links and docs coverage are checked in CI.
- [x] Public metadata and contribution templates exist.
- [x] One worked scaffolding decision case links candidate comparison to final decision text.
- [x] README-shortening order is defined for the docs-site migration.
- [x] Public release metadata audit and citation/license review guide exist.
- [x] Beginner usability review template exists.
- [x] v0.5 release-candidate notes exist.
- [x] v0.5 tagging-readiness summary exists.
- [x] v0.5 human-review runbook exists.
- [x] v0.5 maintainer precheck exists.

Current v0.5 assessment: signed off as the stable `v0.5.0` baseline. Current development focus has moved to `v0.6.0-dev`, while future human validation before `v1.0` should focus on the broader full-protocol experience, active-draft lanes, and contributor feedback rather than reopening the v0.5 release decision itself.

## v0.6 Drafting Goals

- [x] v0.6 kickoff guide exists.
- [x] T2T completeness evidence package exists.
- [x] Example completeness evidence table exists.
- [x] Add tidk sbatch examples for known and de novo telomere motifs.
- [x] Add quarTeT telomere and centromere sbatch examples.
- [x] Add completeness evidence audit helper and toy validation.
- [x] Refine manuscript language for chromosome-scale, near-gapless, candidate T2T, and unresolved claims.
- [x] Worked completeness claim case exists.

## v0.7 Drafting Goals

- [x] v0.7 repeat annotation kickoff guide exists.
- [x] Repeat library decision guide exists.
- [x] Example repeat annotation decision table exists.
- [x] EDTA and RepeatModeler2/RepeatMasker sbatch templates exist.
- [x] Add repeat summary comparison helper.
- [x] Add repeat annotation decision audit helper and toy validation.
- [x] Add repeat landscape interpretation guidance.
- [x] Add repeat-to-gene-annotation handoff checklist.

## v0.8 Drafting Goals

- [x] v0.8 gene annotation kickoff guide exists.
- [x] Gene set decision guide exists.
- [x] Example gene annotation decision table exists.
- [x] Liftoff, BRAKER3, and MAKER sbatch templates exist.
- [x] Add annotation summary comparison helper.
- [x] Add gene annotation decision audit helper and toy validation.
- [x] Add functional annotation guide.
- [x] Add annotation QC dashboard guide.

## v0.9 Drafting Goals

- [x] v0.9 NCBI release kickoff guide exists.
- [x] Release package decision guide exists.
- [x] Example release submission decision table exists.
- [x] Add release submission decision audit helper and toy validation.
- [x] Add annotation submission handoff guide.
- [x] Add methods text template for manuscripts and NCBI structured comments.
- [x] Add worked release candidate case.
- [x] Add release bundle worked example.
- [x] Add table2asn and discrepancy triage guide.
- [x] Add identifier crosswalk example.
- [x] Add table2asn reviewer-response examples.
- [x] Add accession handoff worked example.
- [x] Add community database release companion guide.

## v1.0 Gates

- README is shortened into a landing page.
- Focused docs pages carry the detailed protocol.
- All helper scripts have usage examples and validation coverage.
- sbatch templates pass shell syntax checks.
- Public examples are small, safe, and reproducible.
- NCBI release path includes assembly, annotation, metadata, and manifest checks.
- `LICENSE`, `CITATION.cff`, and `CONTRIBUTING.md` are present.
- Changelog and version are current.
- At least one broader human validation pass is completed across the full docs site, not only the v0.5 stable baseline.
