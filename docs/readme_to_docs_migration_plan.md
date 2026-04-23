# README to Docs Migration Plan

The root `README.md` is currently the canonical longform protocol. That is useful during active development because it keeps the workflow visible in one place. Before v1.0, the README should become a concise landing page and the focused `docs/` tree should carry the detailed protocol through MkDocs.

## Goal

Keep the README useful for a first visitor while moving operational detail into focused pages that are easier to review, link, and maintain.

The preserved pre-condensation source copy for this migration phase is:

```text
docs/archive/README.longform.v0.5.0-dev.md
```

An additional pre-assembly-condensation snapshot is preserved at:

```text
docs/archive/README.longform.pre-assembly-condense.v0.5.0-dev.md
```

## Shortening Order

Shorten sections in this order after v0.5 content review:

| Priority | README content to shorten | Destination docs | Reason |
| ---: | --- | --- | --- |
| 1 | HPC environment setup and installation alternatives | `docs/setup/` | setup detail gets long quickly and benefits from tool-specific pages |
| 2 | hifiasm modes, parameters, and genome profiling | `docs/assembly/` | assembly logic is mature enough to split without losing continuity |
| 3 | QC metrics, plots, contamination, and release dashboards | `docs/qc/` | figures and dashboard examples are easier to maintain as focused pages |
| 4 | dotplot, IGV, and manual correction workflows | `docs/curation/` plus existing curation pages | v0.4 is already a coherent maintained baseline |
| 5 | scaffolding, AGP, gap filling, and T2T readiness | `docs/scaffolding/` | v0.5 is now ready for content review before migration |
| 6 | repeat and gene annotation | `docs/annotation/` | these sections will expand during v0.7 and v0.8 |
| 7 | NCBI submission, accession tracking, and release bundles | `docs/release/` | release detail should remain checklist driven and versioned |
| 8 | references and tool watchlists | topic-specific docs plus README citation summary | keeps the landing page readable while preserving provenance |

## Landing Page Shape

After migration, the README should keep:

- project purpose and scope
- current version and status
- high-level workflow diagram or table
- quick-start path for a new crop genome project
- links to focused documentation sections
- citation, license, contribution, and issue-reporting links
- one compact roadmap table

The README should not try to preserve every command block once an equivalent focused page exists.

## Migration Rules

- Move detail only after the destination page has enough context for a beginner to follow it.
- Preserve one short README summary for every major workflow stage.
- Keep command examples in focused docs and sbatch templates, not duplicated in multiple places.
- After each migration pass, run the Markdown link checker and docs coverage checker.
- Update `docs/status.md`, `CHANGELOG.md`, and the roadmap whenever a major section is moved.

## First Migration Pass After v0.5

Recommended first pass:

1. Convert setup and environment detail into `docs/setup/environment.md`.
2. Convert assembly parameter discussion into `docs/assembly/hifiasm_parameters.md` and related assembly pages.
3. Replace the long README sections with compact summaries and links.
4. Run docs coverage and link checks.
5. Ask an outside reader to start from the shortened README and find the full hifiasm workflow without assistance.

This first pass gives the biggest readability improvement with the lowest biological interpretation risk.
