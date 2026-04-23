# Documentation Status and Roadmap

Current version: `0.5.0-dev`

The root `README.md` remains the canonical longform protocol while the focused documentation tree is built. The goal before v1.0 is to keep the README as a concise landing page and move detailed procedures into `docs/`.

## Current Phase

| Version | Status | Focus |
| --- | --- | --- |
| v0.1 | complete baseline | HiFi assembly core |
| v0.2 | complete baseline | QC dashboard and reports |
| v0.3 | maintained baseline | validation, contamination, release readiness |
| v0.4 | maintained baseline | dotplot review and manual curation |
| v0.5 | content review | scaffolding, gap filling, T2T readiness, docs-site migration |
| v0.6 | active drafting | telomere, centromere, and T2T refinement |
| v0.7 | planned | repeat annotation refinement |
| v0.8 | planned | gene annotation refinement |
| v0.9 | planned | NCBI release candidate polish |
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
| Annotation | active draft | repeat and gene pages exist as first-pass web docs |
| Release | active draft | NCBI submission path exists; release examples will continue to grow |

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

Current v0.5 assessment: feature-complete for scaffolding and README-migration content review, but not stable-release taggable yet. See [v0.5 Review Checklist](release/v0.5_review_checklist.md).

## v0.6 Drafting Goals

- [x] v0.6 kickoff guide exists.
- [x] T2T completeness evidence package exists.
- [x] Example completeness evidence table exists.
- [x] Add tidk sbatch examples for known and de novo telomere motifs.
- [x] Add quarTeT telomere and centromere sbatch examples.
- [x] Add completeness evidence audit helper and toy validation.
- [ ] Refine manuscript language for chromosome-scale, near-gapless, candidate T2T, and unresolved claims.

## v1.0 Gates

- README is shortened into a landing page.
- Focused docs pages carry the detailed protocol.
- All helper scripts have usage examples and validation coverage.
- sbatch templates pass shell syntax checks.
- Public examples are small, safe, and reproducible.
- NCBI release path includes assembly, annotation, metadata, and manifest checks.
- `LICENSE`, `CITATION.cff`, and `CONTRIBUTING.md` are present.
- Changelog and version are current.
