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
| v0.5 | active development | scaffolding, gap filling, T2T readiness, docs-site migration |
| v0.6 | planned | telomere, centromere, and T2T refinement |
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
| Annotation | active draft | repeat and gene pages exist as first-pass web docs |
| Release | active draft | NCBI submission path exists; release examples will continue to grow |

## v0.5 Exit Goals

- Hi-C scaffolding reader path is usable.
- AGP is defined and validated in docs and helper scripts.
- Gap filling is documented as conservative and evidence-based.
- T2T readiness reports combine gap, telomere, and centromere evidence.
- README workflow steps have focused docs coverage.
- Markdown links and docs coverage are checked in CI.

## v1.0 Gates

- README is shortened into a landing page.
- Focused docs pages carry the detailed protocol.
- All helper scripts have usage examples and validation coverage.
- sbatch templates pass shell syntax checks.
- Public examples are small, safe, and reproducible.
- NCBI release path includes assembly, annotation, metadata, and manifest checks.
- `LICENSE`, `CITATION.cff`, and `CONTRIBUTING.md` are present.
- Changelog and version are current.
