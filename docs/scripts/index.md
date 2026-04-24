# Scripts

This section is the catalog of helper scripts in `scripts/`.

Use it when you need to know:

- what a helper script is for
- when in the workflow it belongs
- what a normal first command looks like

These scripts are meant to reduce repetitive manual checking, not replace scientific review.

## Validation and Audit Scripts

| Script | Purpose | Example |
| --- | --- | --- |
| `audit_correction_decisions.py` | Checks correction decision tables for contradictions or missing logic. | `scripts/audit_correction_decisions.py examples/toy/toy_correction_decisions.tsv -o /tmp/correction_audit.tsv` |
| `audit_fasta_headers.py` | Audits release FASTA headers for NCBI-safe naming problems. | `scripts/audit_fasta_headers.py 15_release/sample.fa -o /tmp/fasta_headers.tsv` |
| `audit_gene_annotation_decisions.py` | Audits gene-set decision tables for inconsistent release choices. | `scripts/audit_gene_annotation_decisions.py examples/gene_annotation_decisions.tsv -o /tmp/gene_decisions.tsv` |
| `audit_gff3_fasta_ids.py` | Confirms that GFF3 sequence IDs match the target FASTA. | `scripts/audit_gff3_fasta_ids.py --fasta examples/annotation_validation/toy_genome.fsa --gff3 examples/annotation_validation/toy_annotation.gff3 -o /tmp/gff3_id_audit.tsv` |
| `audit_release_manifest.py` | Checks release manifest rows for missing or inconsistent required fields. | `scripts/audit_release_manifest.py examples/release_manifest.tsv -o /tmp/manifest_audit.tsv` |
| `audit_release_submission_decisions.py` | Audits the release package decision table used to select the final submission bundle. | `scripts/audit_release_submission_decisions.py examples/release_submission_decisions.tsv -o /tmp/release_submission_audit.tsv` |
| `audit_repeat_annotation_decisions.py` | Audits repeat-library or repeat-mask decision tables for contradictions. | `scripts/audit_repeat_annotation_decisions.py examples/repeat_annotation_decisions.tsv -o /tmp/repeat_decisions.tsv` |
| `audit_t2t_evidence_package.py` | Checks completeness-evidence tables for unsupported T2T-style claims. | `scripts/audit_t2t_evidence_package.py examples/t2t_completeness_evidence.tsv -o /tmp/t2t_audit.tsv` |
| `check_docs_coverage.py` | Verifies that the README workflow areas are represented in the docs tree. | `scripts/check_docs_coverage.py -o /tmp/docs_coverage.tsv` |
| `check_markdown_links.py` | Validates local Markdown links across README and docs pages. | `scripts/check_markdown_links.py README.md docs archive -o /tmp/markdown_links.tsv` |
| `check_project_metadata.py` | Verifies that core project metadata files exist and are consistent. | `scripts/check_project_metadata.py -o /tmp/project_metadata.tsv` |
| `check_public_release_metadata.py` | Audits citation, license, version, and release-facing repo metadata. | `scripts/check_public_release_metadata.py -o /tmp/public_release_metadata.tsv` |
| `check_release_bundle.py` | Validates a release bundle by checking FASTA, AGP, manifest, and output structure together. | `scripts/check_release_bundle.py --fasta 15_release/sample.fa --agp 15_release/sample.agp --manifest examples/release_manifest.tsv --out-dir /tmp/release_bundle_check` |
| `check_repo_inventory.py` | Confirms that the README and repository inventory remain aligned. | `scripts/check_repo_inventory.py --readme README.md -o /tmp/repo_inventory.tsv` |
| `validate_agp.py` | Validates AGP syntax and common structural issues. | `scripts/validate_agp.py 15_release/sample.agp -o /tmp/agp_validation.tsv` |
| `validate_breaks.py` | Validates proposed FASTA breakpoints before splitting contigs. | `scripts/validate_breaks.py --fasta examples/toy/toy_assembly.fa --breaks examples/toy/toy_breaks.tsv -o /tmp/break_validation.tsv` |
| `validate_fasta.py` | Validates FASTA formatting and minimum-length rules for release files. | `scripts/validate_fasta.py 15_release/sample.fa --min-length 200 -o /tmp/fasta_validation.tsv` |

## Comparison and Summary Scripts

| Script | Purpose | Example |
| --- | --- | --- |
| `collect_qc_dashboard.py` | Aggregates assembly QC outputs into one summary table. | `scripts/collect_qc_dashboard.py --seqkit 08_stats/seqkit.tsv --busco 08_stats/busco/*/short_summary*.txt -o /tmp/qc_dashboard.tsv` |
| `compare_annotation_summaries.py` | Compares candidate annotation summary tables side by side. | `scripts/compare_annotation_summaries.py --candidate liftoff=examples/annotation_summary_liftoff.tsv --candidate hybrid=examples/annotation_summary_hybrid.tsv -o /tmp/annotation_compare.tsv` |
| `compare_fasta_stats.py` | Compares assembly statistics before and after curation or gap filling. | `scripts/compare_fasta_stats.py --before examples/toy/toy_assembly.fa --after examples/toy/toy_gapfilled.fa -o /tmp/fasta_compare.tsv` |
| `compare_repeat_summaries.py` | Compares repeat summary tables from different repeat workflows. | `scripts/compare_repeat_summaries.py --candidate edta=examples/repeat_summary_edta.tsv --candidate repeatmodeler=examples/repeat_summary_repeatmodeler.tsv -o /tmp/repeat_compare.tsv` |
| `compare_scaffolding_candidates.py` | Compares candidate scaffold sets or FASTA files using shared metrics. | `scripts/compare_scaffolding_candidates.py --candidate draft=examples/toy/toy_assembly.fa --candidate gapfilled=examples/toy/toy_gapfilled.fa -o /tmp/scaffold_compare.tsv` |
| `extract_hifiasm_log_metrics.py` | Pulls key run metrics from hifiasm stderr logs. | `scripts/extract_hifiasm_log_metrics.py 00_log/*.err -o /tmp/hifiasm_log_metrics.tsv` |
| `summarize_agp.py` | Summarizes AGP content, component counts, and gap structure. | `scripts/summarize_agp.py examples/toy/toy.agp -o /tmp/agp_summary.tsv` |
| `summarize_corrections.py` | Summarizes accepted FASTA splits or corrections from logs and maps. | `scripts/summarize_corrections.py --split-map /tmp/toy_split.map.tsv --decision-log examples/toy/toy_correction_decisions.tsv -o /tmp/correction_summary.tsv` |
| `summarize_fasta_gaps.py` | Summarizes gap structure in FASTA files with Ns. | `scripts/summarize_fasta_gaps.py examples/toy/toy_gapfilled.fa -o /tmp/gaps.tsv --summary /tmp/gap_summary.tsv` |
| `summarize_organelle_hits.py` | Summarizes organelle-screen hits across contigs or scaffolds. | `scripts/summarize_organelle_hits.py --input examples/organelle_hits.tsv -o /tmp/organelle_summary.tsv` |
| `summarize_telomeres.py` | Summarizes terminal telomere motif hits for a candidate assembly. | `scripts/summarize_telomeres.py examples/toy/toy_assembly.fa --motif TTTAGGG --window 30 --min-hits 2 -o /tmp/telomeres.tsv` |

## Reporting and Plotting Scripts

| Script | Purpose | Example |
| --- | --- | --- |
| `make_correction_report.py` | Builds a markdown-ready curation report from validation tables and decision logs. | `scripts/make_correction_report.py --sample toy --version 0.5.0-dev --decision-log examples/toy/toy_correction_decisions.tsv --decision-audit /tmp/correction_audit.tsv --correction-summary /tmp/correction_summary.tsv --split-map /tmp/toy_split.map.tsv --fasta-comparison /tmp/fasta_compare.tsv --break-validation /tmp/break_validation.tsv --fasta-validation /tmp/fasta_validation.tsv -o /tmp/correction_report.md` |
| `make_gap_filling_report.py` | Summarizes gap-filling changes and writes a report table or markdown file. | `scripts/make_gap_filling_report.py --before examples/toy/toy_assembly.fa --after examples/toy/toy_gapfilled.fa --decision-log examples/gap_filling_decisions.tsv --sample toy --version 0.5.0-dev -o /tmp/gap_report.tsv --markdown /tmp/gap_report.md` |
| `make_t2t_readiness_report.py` | Combines gap, telomere, and centromere evidence into a completeness-readiness report. | `scripts/make_t2t_readiness_report.py --fasta examples/toy/toy_assembly.fa --telomere-summary /tmp/telomeres.tsv --centromere-table examples/centromere_candidates.tsv --sample toy --version 0.5.0-dev -o /tmp/t2t_readiness.tsv --markdown /tmp/t2t_readiness.md` |
| `plot_qc_dashboard.py` | Plots summary QC tables into quick dashboard figures. | `scripts/plot_qc_dashboard.py -i /tmp/qc_dashboard.tsv -o /tmp/qc_plots` |

## Sequence Editing and Renaming Scripts

| Script | Purpose | Example |
| --- | --- | --- |
| `filter_rename_fasta.py` | Filters short sequences and renames release FASTA headers while writing an ID map. | `scripts/filter_rename_fasta.py -i 07_assemblies/sample.primary.fa -o 15_release/sample.filtered.fa --min-length 200 --prefix SampleID --map 15_release/sample.id_map.tsv` |
| `split_fasta_at_breaks.py` | Splits sequences at user-defined breakpoint positions. | `scripts/split_fasta_at_breaks.py --fasta examples/toy/toy_assembly.fa --breaks examples/toy/toy_breaks.tsv -o /tmp/toy_split.fa --map /tmp/toy_split.map.tsv` |

## Choosing The Right Script

Use these rules of thumb:

- choose `validate_*` or `audit_*` scripts when checking whether something is safe to keep or submit
- choose `compare_*` scripts when selecting among candidate outputs
- choose `summarize_*` or `make_*` scripts when turning raw outputs into review-ready tables or reports
- choose `filter_rename_fasta.py` or `split_fasta_at_breaks.py` only when sequence changes are already justified by evidence

## Related Pages

- [Project starter kit](../project_starter_kit.md)
- [workflow templates and checklists](../workflow_templates/index.md)
- [Release submission packet](../release_submission_packet.md)
